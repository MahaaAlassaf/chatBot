from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.schemas.book_author_association import book_author_association
from app.database.schemas.base import Base

class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    # Relationship to Book
    books = relationship("Book", secondary=book_author_association, back_populates="authors")