import sys
from pathlib import Path
import sqlite3

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from config import DB_PATH


def init_database():

    schema_path = PROJECT_ROOT / "database" / "schema.sql"
    seed_path = PROJECT_ROOT / "database" / "seed_data.sql"

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_PATH)

    try:
        # --------------------------------------------------------
        # Create database schema
        # --------------------------------------------------------

        schema = schema_path.read_text(encoding="utf-8")
        connection.executescript(schema)

        # --------------------------------------------------------
        # Insert controlled test data
        # --------------------------------------------------------

        seed_data = seed_path.read_text(encoding="utf-8")
        connection.executescript(seed_data)

        connection.commit()

        print("=" * 60)
        print("DATABASE INITIALIZATION")
        print("=" * 60)
        print(f"Database: {DB_PATH}")
        print("Schema:   CREATED")
        print("Seed:     LOADED")
        print("Status:   SUCCESS")
        print("=" * 60)

    finally:
        connection.close()


if __name__ == "__main__":
    init_database()