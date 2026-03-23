import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Gemini embedding model identifier
EMBEDDING_MODEL = "models/gemini-embedding-001"


def get_all_embeddings() -> list[GoogleGenerativeAIEmbeddings]:
    """
    Initialise and return a list of GoogleGenerativeAIEmbeddings instances.
    Reads GEMINI_API_KEY_RAG (or fallback GEMINI_API_KEY) from the environment,
    allowing comma-separated multiple keys.
    Automatically filters out dummy/placeholder keys starting with 'AIzaSy_KEY_'.
    """
    # Collect all possible keys from environment
    key_sources = [
        os.getenv("GEMINI_API_KEY_RAG"),
        os.getenv("GEMINI_API_KEY_PRIMARY"),
        os.getenv("GEMINI_API_KEY_SECONDARY"),
        os.getenv("GEMINI_API_KEY"),
        os.getenv("GOOGLE_API_KEY")
    ]
    
    # Filter out None and empty strings, and handle comma-separated lists
    all_keys_raw = []
    for source in key_sources:
        if source:
            all_keys_raw.extend([k.strip() for k in source.split(",") if k.strip()])
    
    valid_keys = []
    seen = set()
    for k in all_keys_raw:
        if k not in seen and "_KEY_" not in k.upper():
            valid_keys.append(k)
            seen.add(k)

    if not valid_keys:
        raise EnvironmentError(
            "No valid GEMINI_API_KEY found. "
            "Please check your .env file and ensure a real key is provided."
        )
        
    return [
        GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL, google_api_key=key)
        for key in valid_keys
    ]
