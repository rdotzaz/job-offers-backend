import os
import pathlib
from functools import lru_cache
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from typing import Annotated, Union
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin.auth import verify_id_token

basedir = pathlib.Path(__file__).parents[1]
load_dotenv(basedir /"BE/.env")

bearer_scheme = HTTPBearer(auto_error=False)


class Settings(BaseSettings):
    """Main settings"""
    app_name: str = "demofirebase"
    env: str = os.getenv("ENV", "development")
    # Needed for CORS
    frontend_url: str = os.getenv("FRONTEND_URL", "NA")


@lru_cache
def get_settings() -> Settings:
    """Retrieves the fastapi settings"""
    return Settings()


def get_firebase_user_from_token(token: Annotated[Union[HTTPAuthorizationCredentials, None], Depends(bearer_scheme)]):
    try:
        if not token:
            raise ValueError("No token")
        user = verify_id_token(token.credentials)
        return user
    except Exception:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not logged in or Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )