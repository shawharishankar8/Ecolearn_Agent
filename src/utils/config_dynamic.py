import os
from typing import Any, Dict

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Dynamic configuration that finds available models"""

    # Gemini API Configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    @classmethod
    def get_available_model(cls):
        """Dynamically find and return an available model"""
        if not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY environment variable is required")

        genai.configure(api_key=cls.GEMINI_API_KEY)

        # Try to read from cached working model
        try:
            if os.path.exists("working_model.txt"):
                with open("working_model.txt", "r") as f:
                    cached_model = f.read().strip()
                    # Test the cached model
                    model = genai.GenerativeModel(cached_model)
                    response = model.generate_content("Test")
                    print(f"Using cached model: {cached_model}")
                    return cached_model
        except:
            pass  # If cached model fails, continue discovery

        # Discover available models
        available_models = []
        try:
            models = genai.list_models()
            for model in models:
                if "generateContent" in model.supported_generation_methods:
                    available_models.append(model.name)
                    print(f"Found available model: {model.name}")
        except Exception as e:
            print(f"Error listing models: {e}")
            raise

        if not available_models:
            raise ValueError("No Gemini models available for content generation")

        # Try each available model
        for model_name in available_models:
            try:
                print(f"Testing model: {model_name}")
                model = genai.GenerativeModel(model_name)
                response = model.generate_content("Say 'test' in one word.")
                print(
                    f"Model works: {model_name} - Response: '{response.text.strip()}'"
                )

                # Cache the working model
                with open("working_model.txt", "w") as f:
                    f.write(model_name)

                return model_name
            except Exception as e:
                print(f"Model failed {model_name}: {str(e)[:100]}...")
                continue

        raise ValueError("No working Gemini models found")

    @classmethod
    def validate_config(cls) -> bool:
        """Validate configuration and set working model"""
        if not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY environment variable is required")

        # Check if API key is placeholder
        if (
            "your_gemini_api_key_here" in cls.GEMINI_API_KEY
            or "your_key_here" in cls.GEMINI_API_KEY
        ):
            raise ValueError(
                "Please replace the placeholder API key with your actual Gemini API key."
                "Get one from: https://aistudio.google.com/app/apikey"
            )

        # Get available model
        cls.GEMINI_MODEL = cls.get_available_model()
        return True

    # Agent Configuration
    MAX_ASSESSMENT_QUESTIONS = 5
    LEARNING_SESSION_TIMEOUT = 300

    # Memory Configuration
    SESSION_EXPIRY_HOURS = 24
    MAX_CONTEXT_LENGTH = 4000
