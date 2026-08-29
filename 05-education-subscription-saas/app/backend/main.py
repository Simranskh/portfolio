from fastapi import FastAPI

from config import APP_NAME, APP_VERSION

from app.backend.auth import router as auth_router
from app.backend.users import router as users_router
from app.backend.plans import router as plans_router
from app.backend.subscriptions import router as subscriptions_router
from app.backend.payments import router as payments_router
from app.backend.courses import router as courses_router
from app.backend.access_control import router as access_router


app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
)


@app.get("/")
def root():
    return {
        "application": APP_NAME,
        "version": APP_VERSION,
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


app.include_router(auth_router)
app.include_router(users_router)
app.include_router(plans_router)
app.include_router(subscriptions_router)
app.include_router(payments_router)
app.include_router(courses_router)
app.include_router(access_router)