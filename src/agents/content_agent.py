from typing import Any, Dict

import google.generativeai as genai

from utils.config import Config


class ContentAgent:
    """Content generation agent for educational materials"""

    def __init__(self):
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)

    async def generate_explanation(
        self, user_input: str, session: dict
    ) -> Dict[str, Any]:
        """Generate educational explanations"""
        clean_input = self._clean_user_input(user_input)

        try:
            prompt = f"""Create a clear, educational explanation about this environmental topic: {clean_input}
            
            Guidelines:
            - Explain in simple, engaging terms
            - Focus on practical environmental impact
            - Keep it under 3 sentences
            - Make it relevant to daily life"""

            response = self.model.generate_content(prompt)
            return {"type": "explanation", "content": response.text}
        except Exception as e:
            return {
                "type": "explanation",
                "content": f"Let me explain {clean_input} in simple terms. This environmental topic relates to sustainable practices that help protect our planet.",
            }

    async def generate_examples(self, user_input: str, session: dict) -> Dict[str, Any]:
        """Generate real-world examples"""
        clean_input = self._clean_user_input(user_input)

        try:
            prompt = f"""Provide 2 practical, real-world examples for this environmental concept: {clean_input}
            
            Make the examples:
            - Easy to understand
            - Relevant to everyday life
            - Actionable for individuals"""

            response = self.model.generate_content(prompt)
            return {"type": "examples", "content": response.text}
        except Exception as e:
            return {
                "type": "examples",
                "content": f"Here are practical examples for {clean_input}: 1) Simple daily actions, 2) Community involvement opportunities.",
            }

    async def generate_visual_suggestion(
        self, user_input: str, session: dict
    ) -> Dict[str, Any]:
        """Generate visual learning suggestions"""
        clean_input = self._clean_user_input(user_input)

        try:
            prompt = f"""Suggest a visual way to understand this environmental concept: {clean_input}
            
            Provide:
            - A visualization idea (chart, diagram, etc.)
            - Why it helps understanding
            - Where to find or create it"""

            response = self.model.generate_content(prompt)
            return {"type": "visual_suggestion", "content": response.text}
        except Exception as e:
            return {
                "type": "visual_suggestion",
                "content": f"To visualize {clean_input}, consider looking at environmental impact charts or sustainable practice infographics online.",
            }

    def _clean_user_input(self, user_input: str) -> str:
        """Clean user input to remove code and focus on actual content"""
        # Remove common code indicators and script content
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
            "config.py",
            "assessment_tools.py",
            "orchestrator.py",
            "content_agent.py",
        ]

        # If input contains code indicators, return a default environmental topic
        if any(indicator in user_input for indicator in code_indicators):
            # Try to extract any environmental keywords
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
                "pollution",
                "biodiversity",
                "renewable",
                "carbon",
                "emissions",
                "warming",
            ]

            for keyword in env_keywords:
                if keyword in user_input.lower():
                    return keyword

            # Default fallback to general environmental topic
            return "environmental sustainability"

        return user_input.strip()
