from fastapi import status, HTTPException, APIRouter, Depends
# from src.books.book_data import books
from src.books.schemas import Book, BookUpdate,BookCreateModel
from typing import List
from src.db.main import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from src.books.service import BookService

book_router = APIRouter()

bookService = BookService()


@book_router.get("/", response_model=List[Book])
async def get_all_books(session: AsyncSession= Depends(get_session)):
    books = await bookService.get_all_books(session=session)
    return books

@book_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Book)
async def create_book(book_data: BookCreateModel, session: AsyncSession = Depends(get_session)) -> Book:
    new_book = await bookService.create_book(book_data=book_data, session=session)
    return new_book

@book_router.get("/{book_id}", response_model=Book)
async def get_book_id(book_id: str,session: AsyncSession= Depends(get_session)):
    # for book in books:
    #     if book["id"] == book_id:
    #         return book

    book = await bookService.get_book(book_uid=book_id,session=session)
    if book:
        return book
    raise HTTPException(status_code=404, detail="Book not found")

@book_router.put("/{book_id}")
async def update_book(book_id: str, book_data: BookUpdate, session: AsyncSession = Depends(get_session)):
    updated_book = await bookService.update_book(book_id=book_id, updateData=book_data, session=session)
    if updated_book:
        return updated_book
    raise HTTPException(status_code=404, detail="Book not found")




@book_router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: str,session: AsyncSession= Depends(get_session)):

    book_to_delete = await bookService.delete_book(book_uid=book_id,session=session)

    if book_to_delete:
        return book_to_delete
    raise HTTPException(status_code=404, detail="Book not found")