from pydantic import BaseModel, Field


class User(BaseModel):
    username: str = Field(..., min_length=3, max_length=15)
    password: str = Field(..., min_length=3, max_length=15)

    class Config:
        extra = "forbid"


class Offer(BaseModel):
    position: str
    city: str
    description: str
    phoneNumber: str
    email: str
    ownerKey: str
    company: str

    class Config:
        extra = "forbid"
