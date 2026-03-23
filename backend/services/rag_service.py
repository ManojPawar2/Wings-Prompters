"""
rag_service.py
--------------
Orchestrates the full indexing pipeline:

  GitHub URL → github_service → ingestion_service → embedding_service → vector_store

Also exposes the `retrieve` helper used by chat_service.
"""

from . import github_service, ingestion_service, embedding_service, vector_store
from langchain_core.documents import Document


def index_repository(github_url: str) -> dict:
    """
    Full indexing pipeline for a GitHub repository.

    Steps
    -----
    1. Fetch all relevant source files from GitHub.
    2. Split files into overlapping, self-describing chunks.
    3. Build (or rebuild) the FAISS vector store.

    Returns
    -------
    dict with keys: files_fetched, files_indexed, chunks_indexed
    """
    # 1. Fetch files
    print(f"[DEBUG] Fetching repository files from: {github_url}")
    files, meta = github_service.fetch_repository_files(github_url)
    print(f"[DEBUG] Successfully fetched {len(files)} files.")
    
    if not files:
        raise ValueError(
            f"No indexable source files found in repository: {github_url}"
        )

    # 2. Chunk into LangChain Documents
    print("[DEBUG] Chunking files into documents...")
    
    # Progress logging
    processed_count = 0
    for path, _ in files:
        processed_count += 1
        if processed_count % 10 == 0:
            print(f"[RAG] Prepared {processed_count} files for chunking...")

    documents = ingestion_service.create_documents(files)
    print(f"[DEBUG] Created {len(documents)} chunks.")
    
    if not documents:
        raise ValueError("Chunking produced zero documents. Check file contents.")

    # 3. Build vector store
    print("[DEBUG] Loading/Retrieving local embedding model...")
    embeddings_list = embedding_service.get_all_embeddings()
    print("[DEBUG] Building FAISS vector store (embedding chunks)...")
    vector_store.build(documents, embeddings_list)
    print("[DEBUG] FAISS index built successfully.")

    # 4. Return stats
    stats = ingestion_service.get_ingestion_stats(files, documents)
    stats["branch"] = meta.get("branch", "unknown")
    stats["owner"] = meta.get("owner", "")
    stats["repo"] = meta.get("repo", "")
    return stats


def retrieve(query: str, k: int = 5) -> list[Document]:
    """
    Embed *query* and return the top-k most relevant code chunks.
    Automatically falls back to secondary API keys if the primary one is exhausted (429).
    """
    embeddings_list = embedding_service.get_all_embeddings()
    
    last_error = None
    for embeddings in embeddings_list:
        try:
            return vector_store.search(query, embeddings, k=k)
        except Exception as exc:
            # If it's a quota error (429), try the next key
            if "429" in str(exc) or "RESOURCE_EXHAUSTED" in str(exc):
                print(f"[RAG] Key exhausted, trying fallback... Error: {exc}")
                last_error = exc
                continue
            # If it's some other critical error, re-raise immediately
            raise exc
            
    # If we tried all keys and all failed, provide a "Static Fallback"
    if last_error:
        print(f"[RAG] All keys exhausted. Providing static fallback context...")
        # Get a high-level overview of the repo from the ingestion stats if possible
        summary = "Architectural context is currently limited due to API quota. Use general knowledge of the repo structure."
        if hasattr(vector_store, "_stats") and vector_store._stats:
            summary = f"Repo Summary: {vector_store._stats.get('chunks_indexed', 0)} chunks were indexed from this repository."
        
        fallback_doc = Document(
            page_content=f"--- QUOTA LIMIT REACHED ---\n{summary}\nNote: Detailed code retrieval is currently disabled. Answer based on architecture and bootstrapping logic.",
            metadata={"file_path": "SYSTEM_FALLBACK"}
        )
        return [fallback_doc]
    return []
