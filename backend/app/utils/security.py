import os
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()

ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    password_bytes = password.encode("utf-8")
    hash_bytes = password_hash.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hash_bytes)


def create_token(user_id: str) -> str:
    expires = datetime.now(timezone.utc) + timedelta(
        minutes=int(os.getenv("JWT_EXPIRE_MINUTES", "1440"))
    )

    return jwt.encode(
        {
            "sub": user_id,
            "exp": expires
        },
        os.getenv("JWT_SECRET", "dev-secret"),
        algorithm=ALGORITHM,
    )


def decode_token(token: str) -> str:
    try:
        payload = jwt.decode(
            token,
            os.getenv("JWT_SECRET", "dev-secret"),
            algorithms=[ALGORITHM],
        )

        return payload["sub"]

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )