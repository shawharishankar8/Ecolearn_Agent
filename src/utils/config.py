import os
from typing import Any, Dict

from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration management for EcoLearn Tutor"""

    # Gemini API Configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    # Try different model names - use the first available one
    AVAILABLE_MODELS = ["gemini-2.5-flash"]
    GEMINI_MODEL = "gemini-2.5-flash"
    # Agent Configuration
    MAX_ASSESSMENT_QUESTIONS = 5
    LEARNING_SESSION_TIMEOUT = 300  # 5 minutes

    # Memory Configuration
    SESSION_EXPIRY_HOURS = 24
    MAX_CONTEXT_LENGTH = 4000

    # External APIs
    OPENWEATHER_API = os.getenv("OPENWEATHER_API_KEY", "")
    WIKIPEDIA_API = "https://en.wikipedia.org/api/rest_v1/page/summary/"

    @classmethod
    def get_available_model(cls):
        """Get the first available model"""
        import google.generativeai as genai

        genai.configure(api_key=cls.GEMINI_API_KEY)

        for model_name in cls.AVAILABLE_MODELS:
            try:
                model = genai.GenerativeModel(model_name)
                # Test the model with a simple call
                response = model.generate_content("Say 'test'")
                print(f"Using model: {model_name}")
                return model_name
            except Exception as e:
                print(f"Model {model_name} not available: {e}")
                continue

        raise ValueError(
            "No available Gemini models found. Please check your API key and model availability."
        )

    @classmethod
    def validate_config(cls) -> bool:
        """Validate essential configuration"""
        if not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY environment variable is required")

        # Test the API key and get available model
        cls.GEMINI_MODEL = cls.get_available_model()
        return True
