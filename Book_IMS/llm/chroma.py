import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.connector import connect_to_db
from app.database.schemas import Book, Author, book_author_association

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_book_authors(title: str):
    engine, session = connect_to_db()
    if session is None:
        logger.error("Failed to connect to the database.")
        return []

    try:
        # Fetch the book by title
        book = (
            session.query(Book)
            .filter(Book.title.ilike(f"%{title}%"))
            .first()
        )
        if not book:
            logger.warning(f"No book found with title: {title}")
            return []

        logger.info(f"Book found: {book.title}")

        # Fetch the author names associated with the book ID
        authors = (
            session.query(Author.name)
            .join(book_author_association, Author.id == book_author_association.c.author_id)
            .filter(book_author_association.c.book_id == book.id)
            .all()
        )
        author_names = [author.name for author in authors]

        logger.info(f"Fetched authors for {title}: {author_names}")
        return author_names
    except Exception as e:
        logger.error(f"Error fetching authors for book '{title}': {e}")
        return []
    finally:
        session.close()

def fetch_books_by_author(author_name: str):
    engine, session = connect_to_db()
    if session is None:
        return []

    try:
        books = (
            session.query(Book)
            .join(book_author_association, Book.id == book_author_association.c.book_id)
            .join(Author, Author.id == book_author_association.c.author_id)
            .filter(Author.name.ilike(f"%{author_name}%"))
            .all()
        )
        if not books:
            return []

        titles = [book.title for book in books]

        logger.info(f"Fetched books by {author_name}: {titles}")
        return titles
    finally:
        session.close()

def fetch_book_description(title: str):
    engine, session = connect_to_db()
    if session is None:
        return ""

    try:
        book = (
            session.query(Book)
            .filter(Book.title.ilike(f"%{title}%"))
            .first()
        )
        if not book:
            return ""

        description = book.description
        logger.info(f"Fetched description for {title}: {description}")
        return description
    finally:
        session.close()

def fetch_book_year(title: str):
    engine, session = connect_to_db()
    if session is None:
        return ""

    try:
        book = (
            session.query(Book)
            .filter(Book.title.ilike(f"%{title}%"))
            .first()
        )
        if not book:
            return ""

        year = book.year
        logger.info(f"Fetched year for {title}: {year}")
        return year
    finally:
        session.close()

def fetch_book_details(title: str):
    description = fetch_book_description(title)
    authors = fetch_book_authors(title)
    year = fetch_book_year(title)

    if not description or not authors or not year:
        return None

    details = {
        "title": title,
        "authors": authors,
        "year": year,
        "description": description
    }
    logger.info(f"Fetched details for {title}: {details}")
    return details
