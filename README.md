# ChatBot Project
Overview
This ChatBot project is composed of several Python scripts designed to handle various tasks related to data fetching, intent extraction, and managing data with ChromaDB. The project includes a Streamlit app for user interaction and APIs built with FastAPI.

Directory Structure
basic

Copy
.
├── chroma.py
├── fetch_data.py
├── intent_extraction.py
├── main.py
├── ollama_handler.py
├── requirements.txt
├── SaveDataToVectorstore.py
└── streamlit_app.py
Files Description
chroma.py: Handles ChromaDB related operations.
fetch_data.py: Contains functions to fetch data from various sources.
intent_extraction.py: Implements intent extraction logic.
main.py: The main entry point for the FastAPI application.
ollama_handler.py: Manages interactions with the Ollama API.
requirements.txt: Lists all the dependencies required for the project.
SaveDataToVectorstore.py: Contains logic to save data to a vector store.
streamlit_app.py: Implements the Streamlit application for user interaction.
Installation
Clone the repository:
sh

Copy
git clone <repository_url>
cd <repository_name>
Create a virtual environment and activate it:
sh

Copy
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install the dependencies:
sh

Copy
pip install -r requirements.txt
Usage
Running the FastAPI Application
To run the FastAPI application, execute:

sh

Copy
uvicorn main:app --reload
The application will be available at http://127.0.0.1:8000.

Running the Streamlit Application
To run the Streamlit application, execute:

sh

Copy
streamlit run streamlit_app.py
The Streamlit app will be available at http://localhost:8501.

How It Works
Overview
This project integrates various modules to provide functionalities such as data fetching, intent extraction, and data storage using ChromaDB. The Streamlit app serves as a user interface for interacting with these functionalities.

ChromaDB Operations
The chroma.py script handles all operations related to ChromaDB, including connecting to the database, querying, and storing data.

Data Fetching
The fetch_data.py script contains functions to fetch data from various sources. This script can be customized to include different APIs or data sources as needed.

Intent Extraction
The intent_extraction.py script implements logic for extracting intents from text data. It uses natural language processing techniques to analyze and categorize user inputs.

API Handling
The main.py script serves as the entry point for the FastAPI application. It defines the API endpoints and handles requests and responses. The ollama_handler.py script manages interactions with the Ollama API, which might include data fetching, processing, or other API-related tasks.

Vector Store Operations
The SaveDataToVectorstore.py script contains the logic to save data into a vector store, which is useful for handling large datasets and performing efficient searches.

User Interface
The streamlit_app.py script implements a Streamlit application that provides a user-friendly interface for interacting with the backend functionalities. Users can fetch data, perform intent extraction, and view results directly from the Streamlit app.

Dependencies
The project relies on the following packages, as specified in requirements.txt:

fastapi
uvicorn
streamlit
requests
sentence-transformers
chromadb
langchain-core
To install these dependencies, run:

sh

Copy
pip install -r requirements.txt
Contributing
If you wish to contribute to this project, please follow these steps:

Fork the repository.
Create a new branch (git checkout -b feature/your-feature-name).
Make your changes.
Commit your changes (git commit -m 'Add some feature').
Push to the branch (git push origin feature/your-feature-name).
Create a new Pull Request.
License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgements
Special thanks to all contributors and the open-source community for their valuable work and resources.
