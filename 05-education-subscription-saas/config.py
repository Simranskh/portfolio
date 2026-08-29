from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DATABASE_DIR = BASE_DIR / "database"
DB_PATH = DATABASE_DIR / "saas.db"

API_HOST = "127.0.0.1"
API_PORT = 8000

APP_NAME = "Education Subscription SaaS"
APP_VERSION = "1.0.0"

DATABASE_DIR.mkdir(parents=True, exist_ok=True)