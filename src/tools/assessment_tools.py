from typing import Any, Dict

import google.generativeai as genai

from utils.config import Config


class KnowledgeAssessmentTool:
    """Custom tool for knowledge assessment"""

    def __init__(self):
        # Initialize Gemini model with available model
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)

    async def assess(
        self, user_input: str, assessment_type: str, session: Dict
    ) -> Dict[str, Any]:
        """Assess user knowledge based on input and assessment type"""

        # Clean the input to avoid code processing
        clean_input = self._clean_input(user_input)

        prompt = self._create_assessment_prompt(clean_input, assessment_type, session)

        try:
            response = self.model.generate_content(prompt)
            return self._parse_assessment_response(response.text, assessment_type)
        except Exception as e:
            print(f"Assessment error: {e}")
            return self._get_fallback_assessment(assessment_type)

    def _clean_input(self, user_input: str) -> str:
        """Clean user input to remove code and focus on environmental topics"""
        # If input looks like code, return a default environmental topic
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

    def _create_assessment_prompt(
        self, user_input: str, assessment_type: str, session: Dict
    ) -> str:
        """Create assessment prompt for Gemini"""

        assessment_templates = {
            "general_environmental_knowledge": """
            Based on the user's response: "{user_input}"
            Assess their general environmental knowledge level (beginner, intermediate, advanced).
            Ask one follow-up question to clarify their understanding.
            Keep it conversational and educational about environmental topics.
            """,
            "specific_interests": """
            User said: "{user_input}"
            Identify their specific interests in environmental topics like climate change, recycling, renewable energy, etc.
            Suggest 2-3 relevant learning areas.
            Ask which topic they'd like to explore first.
            """,
        }

        template = assessment_templates.get(
            assessment_type, assessment_templates["general_environmental_knowledge"]
        )

        return template.format(user_input=user_input)

    def _parse_assessment_response(
        self, response: str, assessment_type: str
    ) -> Dict[str, Any]:
        """Parse Gemini response into structured assessment data"""
        lines = [line.strip() for line in response.split("\n") if line.strip()]
        question = next(
            (line for line in lines if "?" in line),
            "What aspect of environmental science interests you most?",
        )

        return {
            "next_question": question,
            "assessment_type": assessment_type,
            "raw_response": response,
        }

    def _get_fallback_assessment(self, assessment_type: str) -> Dict[str, Any]:
        """Provide fallback assessment questions"""
        fallback_questions = {
            "general_environmental_knowledge": "How would you describe your current understanding of environmental issues?",
            "specific_interests": "What environmental topics are you most curious about?",
            "current_understanding": "What do you already know about environmental science?",
            "motivation_level": "Why are you interested in learning about environmental topics?",
        }

        return {
            "next_question": fallback_questions.get(
                assessment_type, "Tell me about your interest in environmental topics."
            ),
            "assessment_type": assessment_type,
            "is_fallback": True,
        }
