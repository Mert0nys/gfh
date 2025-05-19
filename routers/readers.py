from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List
from datetime import datetime
from database import get_db
from models import Book, BorrowedBook, Reader as ReaderModel
from schemas import Reader, ReaderCreate 

router = APIRouter()

@router.post("/readers/", response_model=Reader)
def create_reader(reader: ReaderCreate, db: Session = Depends(get_db)):
    db_reader = db.query(ReaderModel).filter(ReaderModel.email == reader.email).first()
    if db_reader:
        raise HTTPException(status_code=400, detail="Email уже занят.")
    
    new_reader = ReaderModel(name=reader.name, email=reader.email)
    db.add(new_reader)
    db.commit()
    db.refresh(new_reader)
    
    return new_reader

@router.get("/readers/", response_model=List[Reader])
def read_readers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    readers = db.query(ReaderModel).offset(skip).limit(limit).all()
    return readers

@router.get("/readers/{reader_id}", response_model=Reader)
def read_reader(reader_id: int, db: Session = Depends(get_db)):
    reader = db.query(ReaderModel).filter(ReaderModel.id == reader_id).first()
    if reader is None:
        raise HTTPException(status_code=404, detail="Читатель не найден.")
    
    return reader

@router.post("/borrow")
def borrow_book(book_id: int, reader_id: int, db: Session = Depends(get_db)):
    result = db.execute(select(Book).where(Book.id == book_id))
    book = result.scalar_one_or_none()
    
    if not book or book.available_copies <= 0:
        raise HTTPException(status_code=400, detail="Книга недоступна для выдачи")


    borrowed_count_result = db.execute(
        select(BorrowedBook).where(BorrowedBook.reader_id == reader_id, BorrowedBook.return_date.is_(None))
    )
    borrowed_count = len(borrowed_count_result.all()) 

    if borrowed_count >= 3:
        raise HTTPException(status_code=400, detail="Нельзя взять более 3-х книг одновременно")

    book.available_copies -= 1
    borrowed_record = BorrowedBook(book_id=book_id, reader_id=reader_id)
    
    try:
        db.add(borrowed_record)
        db.commit() 
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Ошибка при выдаче книги")

    return {"message": "Книга успешно выдана", "book_id": book_id, "reader_id": reader_id}

@router.post("/return")
async def return_book(book_id: int, reader_id: int, db: Session = Depends(get_db)):
    borrowed_book = db.query(BorrowedBook).filter(
        BorrowedBook.book_id == book_id,
        BorrowedBook.reader_id == reader_id,
        BorrowedBook.return_date.is_(None)
    ).first()

    if not borrowed_book:
        raise HTTPException(status_code=400, detail="Эта книга не была выдана вам или уже была возвращена.")

    borrowed_book.return_date = datetime.utcnow()
    book = db.query(Book).filter(Book.id == book_id).first()
    if book:
        book.available_copies += 1
    
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Ошибка при возврате книги")

    return {"msg": "Книга успешно возвращена."}
