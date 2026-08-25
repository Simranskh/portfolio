import sqlite3
from pathlib import Path

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr , Field , field_validator

from pwdlib import PasswordHash

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "exampro.db"

password_hash = PasswordHash.recommended()


class RegisterRequest(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr
    password: str = Field(..., min_length=8)


    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str) -> str:
        if not any(char.isupper() for char in password):
            raise ValueError("Password must contain at least one uppercase letter")

        if not any(char.islower() for char in password):
            raise ValueError("Password must contain at least one lowercase letter")

        if not any(char.isdigit() for char in password):
            raise ValueError("Password must contain at least one digit")

        return password

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user: RegisterRequest):
    connection = sqlite3.connect(DB_PATH)

    existing_user = connection.execute(
        "SELECT id FROM users WHERE email = ?",
        (user.email,),
    ).fetchone()

    if existing_user:
        connection.close()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    hashed_password = password_hash.hash(user.password)

    cursor = connection.execute(
        """
        INSERT INTO users (name, email, password)
        VALUES (?, ?, ?)
        """,
        (
            user.name,
            user.email,
            hashed_password,
        ),
    )

    connection.commit()
    user_id = cursor.lastrowid
    connection.close()

    return {
        "message": "User registered successfully",
        "user_id": user_id,
    }

@router.post("/login")
def login_user(user: LoginRequest):
    connection = sqlite3.connect(DB_PATH)

    stored_user = connection.execute(
        """
        SELECT id, name, email, password, role, is_active
        FROM users
        WHERE email = ?
        """,
        (user.email,),
    ).fetchone()

    connection.close()

    if not stored_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not password_hash.verify(user.password, stored_user[3]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if stored_user[5] != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    return {
        "message": "Login successful",
        "user_id": stored_user[0],
        "name": stored_user[1],
        "role": stored_user[4],
    }