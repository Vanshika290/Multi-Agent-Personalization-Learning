import os
from dotenv import load_dotenv

# Load local environment variables from .env if present
load_dotenv()

# Default Gemini model preference
DEFAULT_MODEL = "gemini-2.5-flash"
AVAILABLE_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.5-pro",
    "gemini-1.5-flash",
    "gemini-1.5-pro"
]

def get_api_key() -> str:
    """Retrieve Gemini API key from environment variable or session."""
    return os.getenv("GEMINI_API_KEY", "").strip()
