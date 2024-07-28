import sys
import os
from sqlalchemy import delete, text
from sqlalchemy.exc import ProgrammingError
from app.database.connector import connect_to_db
from app.database.schemas.books import Book
from app.database.schemas.preferences import Preferences
from app.database.schemas.user import User
from app.database.schemas.author import Author
from app.database.schemas.book_author_association import book_author_association  # Ensure this import is correct

# Ensure the app directory is in the PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def delete_and_reset_all_data():
    # Connect to the database
    SessionLocal, engine = connect_to_db()
    
    session = SessionLocal()
    try:
        with session.begin():
            # Delete data in the correct order to respect foreign key constraints
            session.execute(delete(book_author_association))  # Delete from junction table first
            session.execute(delete(Preferences))  # Delete from tables with no foreign key constraints
            session.execute(delete(User))
            session.execute(delete(Author))  # Delete authors before books
            session.execute(delete(Book))  # Delete books last
            session.commit()
            print("All data deleted successfully.")
        
        # Reset primary key sequences
        sequences = ["books_id_seq", "authors_id_seq", "users_id_seq", "preferences_id_seq"]  # Add sequence for junction table if needed
        with engine.connect() as conn:
            for seq in sequences:
                try:
                    conn.execute(text(f"ALTER SEQUENCE {seq} RESTART WITH 1"))
                    print(f"Sequence {seq} reset successfully.")
                except ProgrammingError as e:
                    print(f"Sequence {seq} does not exist and cannot be reset: {e}")
    
    except Exception as e:
        session.rollback()
        print(f"Error deleting data: {e}")
    finally:
        session.close()

# Main execution
if __name__ == "__main__":
    delete_and_reset_all_data()
