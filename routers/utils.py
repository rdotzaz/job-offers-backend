from fastapi import HTTPException
from firebase_admin import firestore


def get_collection(collection_name):
    db = firestore.client()
    return db.collection(collection_name)


def handle_error(e: Exception):
    raise HTTPException(status_code=500, detail=str(e))