from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from pydantic_settings import BaseSettings

class User(BaseModel):
    id: int
    email: EmailStr
    

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class BookCreate(BaseModel):
    title: str
    author: str
    publication_year: int
    isbn: Optional[str] = None
    available_copies: Optional[int] = 1

class Book(BaseModel):
    id: int
    title: str
    publication_year: int
    isbn: Optional[str] = None
    available_copies: Optional[int] = 1


class ReaderCreate(BaseModel):
    name: str
    email: EmailStr

class Reader(ReaderCreate):
    id: int

class BorrowedBookCreate(BaseModel):
    book_id: int
    reader_id: int

class BorrowedBook(BorrowedBookCreate):
    id: int
    borrow_date: datetime
    return_date: Optional[datetime]

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str


    
