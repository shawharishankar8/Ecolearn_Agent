import os

import google.generativeai as genai
from dotenv import load_dotenv

# Load .env from project root (one level up from src)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
env_path = os.path.join(project_root, ".env")
load_dotenv(env_path)


class Config:
    """Configuration management for EcoLearn Tutor"""

    # Gemini API Configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    # Use gemini-2.0-flash which is available
    GEMINI_MODEL = "gemini-2.0-flash"

    # Agent Configuration
    MAX_ASSESSMENT_QUESTIONS = 5
    LEARNING_SESSION_TIMEOUT = 300

    # Memory Configuration
    SESSION_EXPIRY_HOURS = 24
    MAX_CONTEXT_LENGTH = 4000

    @classmethod
    def validate_config(cls) -> bool:
        """Validate essential configuration"""
        if not cls.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY environment variable is required. Check your .env file"
            )

        # Configure Gemini with the API key
        genai.configure(api_key=cls.GEMINI_API_KEY)

        # Test the configuration
        try:
            model = genai.GenerativeModel(cls.GEMINI_MODEL)
            response = model.generate_content("Test")
            print(f"API configuration successful using {cls.GEMINI_MODEL}")
            return True
        except Exception as e:
            raise ValueError(f"API configuration failed: {str(e)}")
