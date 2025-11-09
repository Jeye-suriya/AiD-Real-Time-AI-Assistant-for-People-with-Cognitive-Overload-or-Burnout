import os
from dotenv import load_dotenv

# Import FastAPI with a helpful error message if the package is missing
try:
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
except Exception as e:
    raise ImportError(
        "Missing required package 'fastapi'.\n"
        "Please install project dependencies, for example:\n"
        "  pip install -r requirements.txt\n"
        "Or install FastAPI directly:\n"
        "  pip install fastapi uvicorn\n"
    ) from e
from models import ChatRequest
from chat_engine import get_response
from crisis import contains_crisis_keywords, SAFETY_MESSAGE
from logger import log_chat

load_dotenv()

app = FastAPI()

# Allow CORS from frontend to access the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", "null", "file://"],  # Allow local file access
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI-Powered Mental Health Chatbot!"}

@app.post("/chat")
def chat_with_memory(request: ChatRequest):
    try:
        print("DEBUG: Starting chat request processing")
        session_id = request.session_id
        user_query = request.query
        print(f"DEBUG: Got request - session_id: {session_id}, query: {user_query}")

        # Crisis keyword check
        if contains_crisis_keywords(user_query):
            print("DEBUG: Crisis keywords detected")
            log_chat(session_id, user_query, SAFETY_MESSAGE, is_crisis=True)
            return {"response": SAFETY_MESSAGE}

        # Normal LLM response
        print("DEBUG: Getting LLM response")
        response = get_response(session_id, user_query)
        print(f"DEBUG: Got response: {response[:100]}...")
        log_chat(session_id, user_query, response, is_crisis=False)
        return {"response": response}
    except Exception as e:
        print(f"DEBUG: Error in chat_with_memory: {str(e)}")
        import traceback
        traceback.print_exc()
        return {"response": f"An error occurred: {str(e)}", "error": True}

@app.post("/doc-chat")
def chat_with_documents(request: ChatRequest):
    # Import lazily to avoid heavy initialization at module import time
    from doc_engine import query_documents
    response = query_documents(request.query)
    return {"response": response}


@app.get("/diag")
def diag():
    """Diagnostic endpoint to check runtime environment without exposing secrets."""
    import importlib, os

    openai_set = bool(os.getenv("OPENAI_API_KEY"))
    langchain_installed = importlib.util.find_spec("langchain") is not None
    llama_installed = importlib.util.find_spec("llama_index") is not None

    return {
        "openai_key_present": openai_set,
        "langchain_installed": langchain_installed,
        "llama_index_installed": llama_installed,
    }