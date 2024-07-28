# ollama_handler.py
import logging
from langchain_ollama import OllamaLLM

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

llm = OllamaLLM(model="llama3.1:8b")

def generate_response_with_ollama(descriptions: list) -> str:
    try:
        combined_descriptions = " Next book: ".join(descriptions)
        ollama_input = (
            "You are a helpful assistant tasked with summarizing multiple book descriptions. "
            "Please provide a concise summary based on the following information:\n\n" + combined_descriptions
        )

        ollama_response = llm.invoke(ollama_input, timeout=10)
        if ollama_response:
            return ollama_response.strip()
        else:
            logger.warning("Received an empty response from Ollama.")
            return "I'm sorry, I couldn't fetch the summary right now. Please try again later."
    except Exception as e:
        logger.error(f"Error generating response with Ollama: {e}", exc_info=True)
        return "An unexpected error occurred while summarizing the books. Please try again later."

def summarize_text(text: str) -> str:
    try:
        ollama_input = (
            f"You are a helpful assistant providing book-related information. "
            f"Please summarize the following text in 3-4 lines:\n\n{text}"
        )
        ollama_response = llm.invoke(ollama_input)
        return ollama_response.strip()
    except Exception as e:
        logger.error(f"Error summarizing text with Ollama: {e}", exc_info=True)
        return "Error summarizing text"
