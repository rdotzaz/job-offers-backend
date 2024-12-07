import uvicorn
from routers import offers, auth, filters
from fastapi import FastAPI
from dotenv import load_dotenv
import pathlib
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from firebase_admin import credentials
from config import get_settings

basedir = pathlib.Path(__file__).parents[1]
load_dotenv(basedir / "BE/.env")

def initialize_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate("./service-account.json")  # Update the path
        firebase_admin.initialize_app(cred)

initialize_firebase()

app = FastAPI(
    title="Offers app API",
    description="API for managing offers and users with Firebase backend.",
    version="1.0.0",
)

routers = [auth.router, offers.router, filters.router]
for router in routers:
    app.include_router(router)

settings = get_settings()
# CAN BE USED
# origins = [settings.frontend_url]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        ssl_certfile="./cert.pem",
        ssl_keyfile="./key.pem"
    )
