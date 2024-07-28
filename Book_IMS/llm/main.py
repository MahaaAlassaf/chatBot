# main.py
import logging
from typing import List
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from llm.SaveDataToVectorstore import similarity_text
from llm.intent_extraction import determine_intent_and_entities
from llm.fetch_data import (
    fetch_book_authors, fetch_book_description, fetch_book_details,
    fetch_book_year, fetch_books_by_author, fetch_books_by_year
)
from llm.ollama_handler import generate_response_with_ollama, summarize_text
from api import get_recommendations
from app.database.connector import get_db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI()

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    num_books: int = 2

@app.post("/chat/")
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        user_message = request.messages[-1].content
        logger.info(f"Received message: {user_message}")

        intent, entities = determine_intent_and_entities(user_message)
        logger.info(f"Intent: {intent}, Entities: {entities}")

        if intent == "get_authors":
            title = entities.get("title", "")
            if title:
                authors = fetch_book_authors(db, title)
                if not authors:
                    return {"response": f"Sorry, we don't have information on the authors for the book '{title}'."}
                if len(authors) == 1:
                    return {"response": f"The author of the book '{title}' is: {authors[0]}."}
                else:
                    return {"response": f"The authors of the book '{title}' are: {', '.join(authors)}."}

        elif intent == "get_year":
            title = entities.get("title", "")
            if title:
                year = fetch_book_year(db, title)
                if not year:
                    return {"response": f"Sorry, we don't have information on the year for the book '{title}'."}
                return {"response": f"The book '{title}' was published in {year}."}

        elif intent == "summarize_multiple_books":
                    titles = entities.get("titles", [])
                    descriptions = []
                    for title in titles:
                        description = fetch_book_description(db, title)
                        if description:
                            descriptions.append(description)
                        else:
                            descriptions.append(f"No description available for {title}.")
                    if descriptions:
                        summary = generate_response_with_ollama(descriptions)
                        return {"response": summary}
                    else:
                        return {"response": "No descriptions available to summarize."}

            
        elif intent == "get_description":
            title = entities.get("title", "")
            if title:
                description = fetch_book_description(db, title)
                if not description:
                    return {"response": "Sorry, we don't have a description for this book."}
                return {"response": description}

        elif intent == "get_book_details":
            title = entities.get("title", "")
            if title:
                details = fetch_book_details(db, title)
                if not details:
                    return {"response": "Sorry, we don't have information on this book."}
                return {"response": details}

        elif intent == "get_books_by_author":
            author = entities.get("author", "")
            if author:
                books = fetch_books_by_author(db, author)
                if not books:
                    return {"response": f"Sorry, we don't have books by the author '{author}'."}
                return {"response": books}

        elif intent == "get_books_by_year":
            year = entities.get("title", "")
            if year:
                books = fetch_books_by_year(db, year)
                if not books:
                    return {"response": f"Sorry, we don't have books published in the year '{year}'."}
                return {"response": books}

        elif intent == "get_recommendations":
            description = entities.get("description", "")
            if description:
                metadata, documents = similarity_text(description)
                if not metadata:
                    return {"response": "Sorry, no recommendations are available based on the provided description."}
                return {"response": {"metadata": metadata, "documents": documents}}
            else:
                return {"response": "No description provided for recommendations."}


        ollama_input = (
            f"You are a helpful assistant who provides book-related information only. "
            f"Do not answer questions that are out of scope. User asked: {user_message}. "
            f"Provide a suitable response if it is within your scope."
        )
        response_text = generate_response_with_ollama(ollama_input)
        return {"response": response_text}

    except Exception as e:
        logger.error(f"Error during chat: {e}")
        raise HTTPException(status_code=500, detail="Error during chat")

@app.get("/")
def read_root():
    return {"Hello": "World"}