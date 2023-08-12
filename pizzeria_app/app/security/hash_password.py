import logging

import bcrypt
from fastapi import HTTPException
from starlette import status

logger = logging.getLogger(__name__)


def hash_password(password: str) -> str:
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed_password.decode()


def check_password(password: str, hashed_password: str) -> bool:
    result = bcrypt.checkpw(password.encode(), hashed_password.encode())
    if result:
        return result
    else:
        logger.exception("Incorrect password")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )
