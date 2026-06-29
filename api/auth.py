from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from config.database import get_db
from database.crud import create_user, authenticate_user
from config.auth import create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


@router.post("/register")
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    try:
        user = create_user(db, payload.name, payload.email, payload.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    token = create_access_token(user.id)
    return {"access_token": token, "token_type": "bearer", "user_id": user.id}


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    token = create_access_token(user.id)
    return {"access_token": token, "token_type": "bearer", "user_id": user.id}