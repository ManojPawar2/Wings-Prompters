import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Embedding model. This newer-format Gemini key only serves gemini-embedding-001
# on the v1beta endpoint (text-embedding-004 returns 404 for it). This model has a
# low free-tier rate limit, so indexing throttles to one in-flight request per key
# (see vector_store.build) to avoid 429 storms rather than bursting and retrying.
EMBEDDING_MODEL = "models/gemini-embedding-001"


def get_all_embeddings() -> list[GoogleGenerativeAIEmbeddings]:
    """
    Initialise and return one GoogleGenerativeAIEmbeddings instance per available
    Gemini key. Collecting ALL keys (primary + secondary, plus any legacy /
    comma-separated values) lets the vector store embed batches in parallel across
    keys — roughly multiplying indexing throughput and adding rate-limit failover.
    Placeholder keys (containing '_KEY_') are ignored.
    """
    sources = (
        os.getenv("GEMINI_API_KEY_RAG", ""),
        os.getenv("GEMINI_API_KEY_PRIMARY", ""),
        os.getenv("GEMINI_API_KEY_SECONDARY", ""),
        os.getenv("GEMINI_API_KEY", ""),
    )

    valid_keys: list[str] = []
    seen: set[str] = set()
    for source in sources:
        for k in (part.strip() for part in source.split(",")):
            if not k or "_KEY_" in k.upper() or k in seen:
                continue
            seen.add(k)
            valid_keys.append(k)

    if not valid_keys:
        raise EnvironmentError(
            "No valid GEMINI_API_KEY found. "
            "Please check your .env file and ensure real keys are provided."
        )

    return [
        GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL, google_api_key=key)
        for key in valid_keys
    ]
