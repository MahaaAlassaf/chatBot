<<<<<<< HEAD
# Book_IMS
Book Inventroy Management System
=======
# ChatBot Project

## Overview
This Book ChatBot project is composed of several Python scripts designed to handle various tasks related to book data fetching, intent extraction, and managing book-related data with ChromaDB. The project includes a Streamlit app for user interaction and APIs built with FastAPI.

## Files Description for llm folder
- **chroma.py**: Handles ChromaDB related operations.
- **fetch_data.py**: Contains functions to fetch data from various sources.
- **intent_extraction.py**: Implements intent extraction logic.
- **main.py**: The main entry point for the FastAPI application.
- **ollama_handler.py**: Manages interactions with the Ollama API.
- **requirements.txt**: Lists all the dependencies required for the project.
- **SaveDataToVectorstore.py**: Contains logic to save data to a vector store.
- **streamlit_app.py**: Implements the Streamlit application for user interaction.

## How It Works
1. Fetching User Input: The user inputs queries related to books through the Streamlit app.
2. Intent Extraction: The system analyzes these inputs to determine the user's intent.
3. Data Fetching: Based on the extracted intent, relevant from sources.
4. Data Storage and Retrieval: The fetched data is stored and managed in ChromaDB, allowing for efficient querying and retrieval for recommendtion.
5. User Interface Interaction: The results are displayed in the Streamlit app, providing an interactive experience for the user. for interacting with the backend functionalities. Users can fetch data, perform intent extraction, and view results directly from the Streamlit app.

>>>>>>> a68b1b0d32d777017b385831cfde3d43ef4a514a
