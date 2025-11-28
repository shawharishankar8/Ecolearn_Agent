from typing import Any, Dict, List

import google.generativeai as genai

from tools.assessment_tools_simple import KnowledgeAssessmentTool
from utils.config_simple import Config


class AssessmentAgent:
    """Sequential agent for knowledge assessment - Simple version"""

    def __init__(self):
        self.assessment_tool = KnowledgeAssessmentTool()
        self.assessment_flow = [
            "general_environmental_knowledge",
            "specific_interests",
            "current_understanding",
        ]
        self.current_step = 0

    async def assess_knowledge(self, user_input: str, session: Dict) -> Dict[str, Any]:
        """Sequential assessment process"""

        if self.current_step >= len(self.assessment_flow):
            learning_path = self._generate_learning_path(session)
            return {
                "assessment_complete": True,
                "learning_path": learning_path,
                "message": "Assessment complete! Ready to start learning.",
            }

        current_assessment_type = self.assessment_flow[self.current_step]

        try:
            assessment_result = await self.assessment_tool.assess(
                user_input, current_assessment_type, session
            )
        except Exception as e:
            # Fallback if assessment fails
            assessment_result = {
                "next_question": "What environmental topics interest you?",
                "assessment_type": current_assessment_type,
                "is_fallback": True,
            }

        self.current_step += 1

        return {
            "type": "assessment_question",
            "question": assessment_result["next_question"],
            "progress": f"{self.current_step}/{len(self.assessment_flow)}",
            "assessment_complete": self.current_step >= len(self.assessment_flow),
        }

    def _generate_learning_path(self, session: Dict) -> List[str]:
        """Generate personalized learning path"""
        return [
            "Introduction to Environmental Science",
            "Climate Change Fundamentals",
            "Sustainable Living Practices",
            "Conservation and Biodiversity",
        ]
