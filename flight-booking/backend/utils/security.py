from datetime import datetime, timedelta, timezone
from pathlib import Path
import secrets

from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import jwt
import os
from sqlmodel import Session, select
from backend.models.users import UserInDb
from sqlalchemy.orm import selectinload
from backend.models.permissions import Group


BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def generate_reset_token() -> str:
    """Generate a cryptographically secure random token for password reset."""
    return secrets.token_urlsafe(32)


def hash_reset_token(token: str) -> str:
    """Hash the reset token before storing in database."""
    return pwd_context.hash(token)

def verify_reset_token(plain_token: str, hashed_token: str) -> bool:
    """Verify a reset token against its hash."""
    return pwd_context.verify(plain_token, hashed_token)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    if not SECRET_KEY:
        raise RuntimeError("SECRET_KEY is not configured")

    data_to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    data_to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def authenticate_user(session: Session, email: str, password: str):
    # Eager load groups and their permissions
    statement = (
        select(UserInDb)
        .where(UserInDb.email == email)
        .options(selectinload(UserInDb.groups).selectinload(Group.permissions))
    )
    user = session.exec(statement).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user
