🧠 AI-Powered Mental Health Chatbot

An empathetic, AI-driven mental health chatbot built using FastAPI and OpenAI GPT models.
It provides supportive and non-judgmental conversations while maintaining ethical boundaries and promoting professional help when necessary.
The app also detects potential crisis-related messages and provides emergency contact information automatically.

🌟 Features

💬 Conversational AI using GPT-3.5-turbo

🧩 Crisis detection with automatic safety messages

📂 Document-based Q&A using LlamaIndex

🪵 Chat logging with session tracking

⚙️ Environment configuration with .env

🚀 RESTful backend API built with FastAPI

🧰 Project Structure
.
├── main.py              # FastAPI application entry point
├── chat_engine.py       # Core OpenAI chat logic
├── crisis.py            # Crisis keyword detection and safety messages
├── doc_engine.py        # LlamaIndex-based document querying
├── models.py            # Pydantic data models
├── logger.py            # CSV-based logging system
├── requirements.txt     # Project dependencies
├── .env                 # Environment variables (contains your OpenAI API key)
├── chat_log.csv         # Saved chat logs (auto-generated)
└── data/                # Optional folder for documents (used by doc_engine.py)

⚙️ Setup Instructions
1. Clone the repository
git clone https://github.com/yourusername/mental-health-chatbot.git
cd mental-health-chatbot

2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate     # For Linux/Mac
venv\Scripts\activate        # For Windows

3. Install dependencies
pip install -r requirements.txt

4. Configure environment variables

Create a .env file in the root directory with your OpenAI API key:

OPENAI_API_KEY="your-openai-api-key"


⚠️ Important: Never share or commit your .env file.

5. Run the FastAPI server
uvicorn main:app --reload


Visit the app at:
👉 http://127.0.0.1:8000

🧪 API Endpoints
GET /

Returns a welcome message confirming the API is active.

POST /chat

Handles chat interactions and performs crisis keyword checks.

Request body:

{
  "session_id": "user123",
  "query": "I'm feeling really down today."
}


Response:

{
  "response": "I'm really sorry you're feeling this way. You're not alone..."
}

POST /doc-chat

Queries uploaded documents using LlamaIndex.

GET /diag

Provides diagnostic information about the environment and dependencies.

🛠️ Technologies Used

FastAPI – Backend framework

OpenAI GPT-3.5-turbo – Core conversational model

LangChain / LlamaIndex – Document-based Q&A

Python-dotenv – Environment variable management

CSV Logging – Simple chat history persistence

🧠 Crisis Detection

The chatbot detects sensitive or crisis-related keywords (e.g., “suicidal”, “hopeless”, “want to die”)
and automatically responds with supportive messages and helpline resources for different regions:

India: 9152987821 (iCall), 1800-599-0019 (Vandrevala Foundation)
USA: 988 (Suicide & Crisis Lifeline)
UK: 116 123 (Samaritans)

📄 Logging

All chat sessions are logged in chat_log.csv with:

Timestamp

Session ID

User Query

AI Response

Crisis Flag

🧩 Future Improvements

Frontend UI (React, Vue, or Flutter)

Database integration for persistent sessions

Sentiment analysis

Multi-language support

Cloud deployment (Render / Hugging Face Spaces)

🤝 Contributing

Pull requests are welcome!
For major changes, please open an issue to discuss your ideas before submitting.

🛡️ Disclaimer

This chatbot is not a substitute for professional mental health care.
If you are in crisis or need immediate help, please reach out to a trusted friend, family member, or professional helpline.

Made with ❤️ using FastAPI & OpenAI GPT
