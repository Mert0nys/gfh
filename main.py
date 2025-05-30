from fastapi import FastAPI
from database import engine
from models import Base
from routers import book, auth, tokens, readers

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router, tags=["register"])
app.include_router(tokens.router, tags=["token"])
app.include_router(book.router, tags=["books"])
app.include_router(readers.router, tags=["readers"])
