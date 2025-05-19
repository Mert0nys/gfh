from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Response, HTTPException, Depends
from sqlalchemy.orm import Session

from pydantic import EmailStr
from database import get_auth_data, get_db
from schemas import UserLogin
from crud import get_user_by_email

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    auth_data = get_auth_data()
    encoded_jwt = jwt.encode(to_encode, auth_data['secret_key'], algorithm=auth_data['algorithm'])
    return encoded_jwt

def authenticate_user(db: Session, email: EmailStr, password: str):
    user_data = get_user_by_email(db=db, email=email)
    if not user_data:
        return None

    if not verify_password(plain_password=password, hashed_password=user_data.hashed_password):
        return None
    
    return user_data

@router.post("/login")
def aut_user(response: Response, user_data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db=db, email=user_data.email, password=user_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return {"access_token": access_token, "refresh_token": None}
