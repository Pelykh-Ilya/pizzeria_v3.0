import logging

import jwt
from datetime import datetime, timedelta

from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette import status

from app.providers.security import get_secret_key

logger = logging.getLogger(__name__)

auth_scheme = HTTPBearer(scheme_name="Pizzeria JWT token", bearerFormat="JWT")


def create_jwt_token(user: str, secret_key: str, life_time: int) -> str:
    expiration = datetime.utcnow() + timedelta(seconds=life_time)
    data = {'exp': expiration, "sub": user}
    token = jwt.encode(payload=data, key=secret_key, algorithm="HS256")
    return token


def verify_token(token: str, secret_key: str) -> dict:
    try:
        payload = jwt.decode(jwt=token, key=secret_key, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        logger.exception("Token has expired")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="JWT token has expired"
        )
    except jwt.PyJWTError:
        logger.exception("Failed to verify JWT token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Failed to verify JWT token"
        )


def check_token(token: HTTPAuthorizationCredentials = Depends(auth_scheme), secret_key: str = Depends(get_secret_key)):
    return verify_token(token=token.credentials, secret_key=secret_key)
