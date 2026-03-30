import os
import secrets
from datetime import timedelta
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
INSTANCE_DIR = BASE_DIR / "instance"

load_dotenv(BASE_DIR / ".env")


def _build_default_sqlite_uri() -> str:
    INSTANCE_DIR.mkdir(parents=True, exist_ok=True)
    return f"sqlite:///{(INSTANCE_DIR / 'app_narcista.db').as_posix()}"


def _normalize_database_uri(database_url: Optional[str]) -> str:
    if not database_url:
        return _build_default_sqlite_uri()

    if database_url.startswith("sqlite:///") and not database_url.startswith("sqlite:////"):
        raw_path = database_url.removeprefix("sqlite:///")
        looks_like_windows_absolute = len(raw_path) > 1 and raw_path[1] == ":"
        if raw_path and not looks_like_windows_absolute and not raw_path.startswith("/"):
            return f"sqlite:///{(BASE_DIR / raw_path).as_posix()}"

    return database_url


def _as_bool(value: Optional[str], default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY") or secrets.token_urlsafe(32)
    SQLALCHEMY_DATABASE_URI = _normalize_database_uri(os.getenv("DATABASE_URL"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    APP_NAME = "AMFRA SAÚDE MENTAL LTDA"
    APP_BASE_URL = os.getenv("APP_BASE_URL", "http://127.0.0.1:5000").rstrip("/")
    PREFERRED_URL_SCHEME = os.getenv("PREFERRED_URL_SCHEME", "http")

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = _as_bool(os.getenv("SESSION_COOKIE_SECURE"), default=False)
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SECURE = SESSION_COOKIE_SECURE
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)

    AUTO_CREATE_DB = _as_bool(os.getenv("AUTO_CREATE_DB"), default=True)
    AUTO_SEED_ADMIN = _as_bool(os.getenv("AUTO_SEED_ADMIN"), default=False)
    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "doutor")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
    LOG_DIR = INSTANCE_DIR / "logs"

    NOTIFICATION_RECIPIENT_NAME = os.getenv("NOTIFICATION_RECIPIENT_NAME", "Dra. Andrea Franco")
    WHATSAPP_ENABLED = _as_bool(os.getenv("WHATSAPP_ENABLED"), default=False)
    WHATSAPP_API_BASE = os.getenv("WHATSAPP_API_BASE", "https://graph.facebook.com")
    WHATSAPP_API_VERSION = os.getenv("WHATSAPP_API_VERSION", "v21.0")
    WHATSAPP_ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")
    WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
    WHATSAPP_DESTINATION_NUMBER = os.getenv("WHATSAPP_DESTINATION_NUMBER", "5511985879829")
    WHATSAPP_TIMEOUT_SECONDS = int(os.getenv("WHATSAPP_TIMEOUT_SECONDS", "15"))
    WHATSAPP_PROVIDER = "Canal seguro de mensageria"
