import os
from typing import Optional

# Lazily import and initialize heavy LLM/indexing resources so that importing
# this module (for example when starting FastAPI) doesn't perform network
# calls or long-running initialization.

_query_engine = None

def _init_query_engine():
    """Initialize and cache the query engine on first use."""
    global _query_engine
    if _query_engine is not None:
        return

    # Import heavy dependencies inside the initializer
    from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
    from llama_index.llms.openai import OpenAI as LlamaOpenAI

    llama_llm = LlamaOpenAI(model="gpt-3.5-turbo", api_key=os.getenv("OPENAI_API_KEY"))

    documents = SimpleDirectoryReader("data").load_data()

    index = VectorStoreIndex.from_documents(documents)

    _query_engine = index.as_query_engine(llm=llama_llm)

def query_documents(user_query: str) -> str:
    """Query the indexed documents. Initializes the index on first call.

    Returns a stringified response from the query engine.
    """
    _init_query_engine()
    return str(_query_engine.query(user_query))