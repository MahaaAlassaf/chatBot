import pandas as pd
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE, Settings
import sys
import contextlib

# Initialize the ChromaDB PersistentClient
client = chromadb.PersistentClient(
    path="chroma_db", 
    settings=Settings(),
)

collection = client.get_or_create_collection(name="collection_name")

@contextlib.contextmanager
def suppress_output():
    with open('/dev/null', 'w') as devnull:
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = devnull
        sys.stderr = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

def store_books_in_vectorDB():
    model = SentenceTransformer('all-MiniLM-L6-v2')

    df = pd.read_csv("/Users/mahassaf004/Desktop/books.csv", usecols=['title', 'authors', 'categories', 'description'])
    documents = []
    embeddings_list = []
    IDs = []
    metadatas = []

    for index, row in df.iterrows():
        text = ' '.join(row.astype(str).values)
        documents.append(text)
        embedding = model.encode(text).tolist()
        embeddings_list.append(embedding)
        IDs.append(str(index))
        metadata = {
            'title': row['title'],
            'authors': row['authors'],
            'categories': row['categories'],
            'description': row['description']
        }
        metadatas.append(metadata)

    try:
        print(f"Adding {len(documents)} documents to the collection.")
        with suppress_output():
            collection.add(
                documents=documents,
                embeddings=embeddings_list,
                ids=IDs,
                metadatas=metadatas
            )
    except Exception as e:
        print(f"Error occurred while adding documents: {e}")

    return "Documents added to the collection successfully."

def add_book_to_vectorDB(title, authors, categories, description):
    text = f"{title} {authors} {categories} {description}"
    model = SentenceTransformer('all-MiniLM-L6-v2')

    embedding = model.encode(text).tolist()
    metadata = {
        'title': title,
        'authors': authors,
        'categories': categories,
        'description': description
    }

    with suppress_output():
        collection.add(
            documents=[text],
            embeddings=[embedding],
            ids=[title],
            metadatas=[metadata]
        )

def similarity_text(description: str):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    query_embedding = model.encode(description).tolist()

    try:
        results = collection.query(query_embeddings=[query_embedding], n_results=5)
        return results['metadatas'], results['documents']
    except Exception as e:
        print(f"Error querying collection: {e}")
        raise

def get_books():
    books = collection.get()
    return books

def update_book(title, new_data):
    collection.delete(ids=[title])
    add_book_to_vectorDB(**new_data)
    return "Book update"

def delete_book(title):
    collection.delete(ids=[title])
    return "Book deleted"

store_books_in_vectorDB()