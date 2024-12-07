import secrets
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Header

from models.models import User
from routers.utils import get_collection, handle_error

router = APIRouter()


def get_auth_collection():
    AUTH_COLLECTION_NAME = 'users'
    return get_collection(AUTH_COLLECTION_NAME)


def validate_api_key(apiKey: str = Header(...)):
    collection = get_auth_collection()
    user_query = collection.where("apiKey", "==", apiKey).stream()
    users = [user.to_dict() for user in user_query]
    if not users:
        raise HTTPException(status_code=401, detail="Invalid API key")


@router.post("/register")
def register_user(user: User):
    try:
        collection = get_auth_collection()
        existing_user = collection.where("username", "==", user.username).stream()
        if list(existing_user):
            raise HTTPException(status_code=400, detail="Username already exists")

        api_key = secrets.token_hex(32)
        user_id = str(uuid4())
        user_data = {
            "username": user.username,
            "password": user.password,
            "apiKey": api_key,
        }
        collection.document(user_id).set(user_data)
        return {"message": "User registered successfully"}
    except Exception as e:
        print(e)
        handle_error(e)


@router.post("/login")
def login_user(user: User):
    try:
        collection = get_auth_collection()
        user_query = collection.where("username", "==", user.username).where("password", "==", user.password).stream()

        user_data = next((doc.to_dict() for doc in user_query), None)

        if not user_data:
            raise HTTPException(status_code=401, detail="Invalid username or password")

        return {"message": "Login successful", "api_key": user_data["apiKey"]}

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        handle_error(e)
