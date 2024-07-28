from sqlalchemy import Table, Column, Integer, ForeignKey
from app.database.schemas.base import Base

book_author_association = Table(
    'book_author_association', Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id'), primary_key=True),
    Column('author_id', Integer, ForeignKey('authors.id'), primary_key=True)
)
