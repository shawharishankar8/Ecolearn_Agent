import os
from typing import Any, Dict

import google.generativeai as genai
from dotenv import load_dotenv

# Load .env from project root
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
env_path = os.path.join(project_root, ".env")
load_dotenv(env_path)


class KnowledgeAssessmentTool:
    """Custom tool for knowledge assessment - Simple version"""

    def __init__(self):
        # Configure Gemini with API key
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.0-flash")

    async def assess(
        self, user_input: str, assessment_type: str, session: Dict
    ) -> Dict[str, Any]:
        """Assess user knowledge based on input and assessment type"""

        clean_input = self._clean_input(user_input)
        prompt = self._create_assessment_prompt(clean_input, assessment_type)

        try:
            response = self.model.generate_content(prompt)
            return {
                "next_question": response.text.strip(),
                "assessment_type": assessment_type,
                "raw_response": response.text,
            }
        except Exception as e:
            print(f"Assessment error: {e}")
            return self._get_fallback_assessment(assessment_type)

    def _clean_input(self, user_input: str) -> str:
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
        ]
        if any(indicator in user_input for indicator in code_indicators):
            return "environmental sustainability"
        return user_input

    def _create_assessment_prompt(self, user_input: str, assessment_type: str) -> str:
        if assessment_type == "specific_interests":
            return f"""User is interested in: "{user_input}"
            
Please suggest 3 specific environmental topics related to this interest and list them clearly.
Then ask which one they want to explore first.

Make sure to include the options in your response."""
        else:
            return f'Ask a follow-up question about environmental topics based on: "{user_input}"'

    def _get_fallback_assessment(self, assessment_type: str) -> Dict[str, Any]:
        return {
            "next_question": "What specific environmental topic would you like to learn about?",
            "assessment_type": assessment_type,
            "is_fallback": True,
        }
