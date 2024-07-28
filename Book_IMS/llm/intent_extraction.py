# intent_extraction.py
from enum import Enum
import logging
import json
from langchain_ollama import OllamaLLM

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Intents(Enum):
    GET_AUTHORS = "get_authors"
    GET_YEAR = "get_year"
    GET_DESCRIPTION = "get_description"
    GET_SUMMARY_DESCRIPTION = "get_summary_description"
    GET_BOOK_DETAILS = "get_book_details"
    GET_RECOMMENDATIONS = "get_recommendations"
    SUMMARIZE_MULTIPLE_BOOKS = "summarize_multiple_books"
    GET_BOOKS_BY_AUTHOR = "get_books_by_author"
    GET_BOOKS_BY_YEAR = "get_books_by_year"
    GENERAL = "GENERAL"

llm = OllamaLLM(model="llama3.1:8b")

def determine_intent_and_entities(document: str):
    try:
        ollama_input = (
            f"You are a helpful assistant specializing in book-related queries. Your task is to determine the user's intent "
            f"and extract relevant entities from the following information: '{document}'. "
            f"Possible intents are: get_authors, get_year, get_description, get_summary_description, get_book_details, get_recommendations, summarize_multiple_books, get_books_by_author, get_books_by_year, general. "
            f"For 'get_authors', the entity name should be 'title'. "
            f"For 'get_year', the entity name should be 'title'. "
            f"For 'get_description', the entity name should be 'title'. "
            f"For 'get_summary_description', the entity name should be 'title'. "
            f"For 'summarize_multiple_books', the entity name should be 'titles'. "
            f"For 'get_books_by_author', the entity name should be 'author'. "
            f"For 'get_books_by_year', the entity name should be 'year'. "
            f"For 'get_recommendations', the entity name should be 'description'. "
            f"For 'general', provide the intent without specific entities. "
            f"Provide the intent and entities in JSON format like this:\n"
            f"{{\n  \"intent\": \"<intent>\",\n  \"entities\": {{ \"<entity_name>\": \"<entity_value>\" }}\n}}"
        )

        ollama_response = llm.invoke(ollama_input)
        response_json = ollama_response.strip()
        logger.info(f"Ollama response: {response_json}")

        try:
            json_start = response_json.index("{")
            json_end = response_json.rindex("}") + 1
            response_json = response_json[json_start:json_end]
            response_data = json.loads(response_json)
        except (ValueError, json.JSONDecodeError) as e:
            logger.error(f"Error extracting or decoding JSON: {e}", exc_info=True)
            logger.error(f"Response content: {response_json}")
            return Intents.GENERAL.value, {}

        logger.info(f"Parsed response: {response_data}")

        intent = response_data.get("intent", Intents.GENERAL.value)
        entities = response_data.get("entities", {})

        if not intent:
            intent = Intents.GENERAL.value
        if not isinstance(entities, dict):
            entities = {}

        logger.info(f"Determined intent: {intent}, entities: {entities}")
        return intent, entities
    except Exception as e:
        logger.error(f"Error determining intent and entities with Ollama: {e}", exc_info=True)
        return Intents.GENERAL.value, {}