from typing import Any, Dict

import google.generativeai as genai

from utils.config_simple import Config


class ContentAgent:
    """Content generation agent - Simple version"""

    def __init__(self):
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)

    async def generate_explanation(
        self, user_input: str, session: dict
    ) -> Dict[str, Any]:
        """Generate educational explanations"""
        clean_input = self._clean_user_input(user_input)

        try:
            prompt = f"Explain this environmental topic in simple terms: {clean_input}"
            response = self.model.generate_content(prompt)
            return {"type": "explanation", "content": response.text}
        except Exception as e:
            return {
                "type": "explanation",
                "content": f"Let me explain {clean_input} in environmental context.",
            }

    async def generate_examples(self, user_input: str, session: dict) -> Dict[str, Any]:
        """Generate real-world examples"""
        clean_input = self._clean_user_input(user_input)

        try:
            prompt = f"Provide 2 practical examples for: {clean_input}"
            response = self.model.generate_content(prompt)
            return {"type": "examples", "content": response.text}
        except Exception as e:
            return {
                "type": "examples",
                "content": f"Practical examples for {clean_input}.",
            }

    async def generate_visual_suggestion(
        self, user_input: str, session: dict
    ) -> Dict[str, Any]:
        """Generate visual learning suggestions"""
        clean_input = self._clean_user_input(user_input)

        try:
            prompt = f"Suggest a visual way to understand: {clean_input}"
            response = self.model.generate_content(prompt)
            return {"type": "visual_suggestion", "content": response.text}
        except Exception as e:
            return {
                "type": "visual_suggestion",
                "content": f"Visual aids can help understand {clean_input}.",
            }

    def _clean_user_input(self, user_input: str) -> str:
        """Clean user input to remove code"""
        code_indicators = [
            "def ",
            "class ",
            "import ",
            "async ",
            "await ",
            "print(",
            "self.",
            "if ",
            "for ",
            "while ",
            "try:",
            "except:",
            "with ",
            "open(",
            "api_key",
            "GEMINI_API_KEY",
            "cat >",
            "EOF",
        ]

        if any(indicator in user_input for indicator in code_indicators):
            env_keywords = [
                "environment",
                "climate",
                "sustainable",
                "green",
                "energy",
                "recycle",
                "planet",
                "earth",
                "eco",
                "conservation",
            ]

            for keyword in env_keywords:
                if keyword in user_input.lower():
                    return keyword

            return "environmental sustainability"

        return user_input.strip()
