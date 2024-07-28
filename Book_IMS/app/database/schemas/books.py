from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.schemas.base import Base
from app.database.schemas.book_author_association import book_author_association

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    genre = Column(String, nullable=True)
    description = Column(String, nullable=True)
    year = Column(Integer, nullable=True)

    # Relationship to Author
    authors = relationship("Author", secondary=book_author_association, back_populates="books")
