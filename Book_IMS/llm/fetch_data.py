# fetch_data.py
import logging
from typing import List
from sqlalchemy.orm import Session
from app.database.schemas import Book, Author, book_author_association

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_book_authors(db: Session, title: str):
    try:
        book = db.query(Book).filter(Book.title.ilike(f"%{title}%")).first()
        if not book:
            logger.warning(f"No book found with title: {title}")
            return []

        authors = db.query(Author.name).join(book_author_association, Author.id == book_author_association.c.author_id).filter(book_author_association.c.book_id == book.id).all()
        author_names = [author[0] for author in authors]
        return author_names
    except Exception as e:
        logger.error(f"Error fetching authors for book '{title}': {e}")
        return []

def fetch_book_year(db: Session, title: str):
    try:
        book = db.query(Book).filter(Book.title.ilike(f"%{title}%")).first()
        return book.year if book else ""
    except Exception as e:
        logger.error(f"Error fetching year for book '{title}': {e}")
        return ""

def fetch_book_description(db: Session, title: str) -> str:
    try:
        book = db.query(Book).filter(Book.title.ilike(f"%{title}%")).first()
        return book.description if book else ""
    except Exception as e:
        logger.error(f"Error fetching description for book '{title}': {e}")
        return ""

def fetch_book_details(db: Session, title: str) -> dict:
    try:
        book = db.query(Book).filter(Book.title.ilike(f"%{title}%")).first()
        if not book:
            return {}

        authors = db.query(Author.name).join(book_author_association, Author.id == book_author_association.c.author_id).filter(book_author_association.c.book_id == book.id).all()
        author_names = [author[0] for author in authors]

        book_details = {
            "title": book.title,
            "year": book.year,
            "description": book.description,
            "authors": author_names
        }
        return book_details
    except Exception as e:
        logger.error(f"Error fetching details for book '{title}': {e}")
        return {}

def fetch_books_by_author(db: Session, author_name: str) -> List[dict]:
    try:
        author = db.query(Author).filter(Author.name.ilike(f"%{author_name}%")).first()
        if not author:
            logger.warning(f"No author found with name: {author_name}")
            return []

        books = db.query(Book).join(book_author_association, Book.id == book_author_association.c.book_id).filter(book_author_association.c.author_id == author.id).all()
        book_list = [{"title": book.title, "year": book.year, "description": book.description, "genre": book.genre} for book in books]
        return book_list
    except Exception as e:
        logger.error(f"Error fetching books by author '{author_name}': {e}")
        return []

def fetch_books_by_year(db: Session, year: int) -> List[dict]:
    try:
        books = db.query(Book).filter(Book.year == year).all()
        book_list = [{"title": book.title, "year": book.year, "description": book.description, "genre": book.genre} for book in books]
        return book_list
    except Exception as e:
        logger.error(f"Error fetching books for year '{year}': {e}")
        return []
