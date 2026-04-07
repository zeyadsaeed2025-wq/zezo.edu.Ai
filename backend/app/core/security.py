from datetime import datetime, timedelta
from typing import Optional
import hashlib
import secrets
from jose import JWTError, jwt
from app.core.config import settings

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password using SHA256"""
    hash_obj = hashlib.sha256(plain_password.encode())
    return hash_obj.hexdigest() == hashed_password

def get_password_hash(password: str) -> str:
    """Hash password using SHA256 (simplified for development)"""
    hash_obj = hashlib.sha256(password.encode())
    return hash_obj.hexdigest()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    return encoded_jwt

def decode_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload
    except JWTError:
        return None
