from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import crud, schemas
from database import get_db



router = APIRouter()


@router.post("/register", response_model=schemas.User)
def create_user(email: schemas.UserCreate, db: Session = Depends(get_db)):
     return crud.create_user(db=db, email=email)

