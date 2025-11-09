import os
import logging
import openai
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

logger.debug('Starting chat_engine.py')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
logger.debug('OPENAI_API_KEY present: %s', bool(OPENAI_API_KEY))

if not OPENAI_API_KEY:
    raise ValueError('OPENAI_API_KEY not found in environment')

# Accept both OpenAI API key formats: sk-proj- (new) and sk- (legacy)
if not (OPENAI_API_KEY.startswith('sk-proj-') or OPENAI_API_KEY.startswith('sk-')):
    raise ValueError('Invalid API key format. OpenAI API keys should start with "sk-proj-" (new format) or "sk-" (legacy format)')

# Set API key globally
openai.api_key = OPENAI_API_KEY

try:
    # Initialize the OpenAI client
    def get_response(session_id: str, user_query: str) -> str:
        try:
            logger.debug('Creating OpenAI client')
            client = openai.OpenAI(api_key=OPENAI_API_KEY)
            
            logger.debug('Sending request to OpenAI API')
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful mental health chatbot. You provide supportive and empathetic responses while maintaining appropriate boundaries and suggesting professional help when needed."
                    },
                    {"role": "user", "content": user_query}
                ],
                temperature=0.7
            )
            logger.debug('Received response from OpenAI API')
            return response.choices[0].message.content
        except Exception as e:
            logger.error('Error in get_response: %s', str(e))
            raise

except Exception as e:
    logger.error('Error initializing OpenAI: %s', str(e))
    logger.exception('Full traceback:')
    
    def get_response(session_id: str, user_query: str) -> str:
        error_msg = "An error occurred while initializing the chat service. Please try again later."
        logger.error(error_msg)
        return error_msg