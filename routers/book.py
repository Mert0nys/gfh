from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import crud, schemas
from database import get_db
router = APIRouter()

@router.post("/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
     return crud.create_book(db=db, book=book)

@router.get("/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
     return crud.get_book(db=db, book_id=book_id)

@router.put("/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)):
     return crud.update_book(db=db, book_id=book_id, book=book)

@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
     crud.delete_book(db=db, book_id=book_id)
     return {"message": "Book deleted successfully."}
