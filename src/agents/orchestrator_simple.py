from typing import Any, Dict, List

import google.generativeai as genai

from agents.assessment_agent_simple import AssessmentAgent
from agents.content_agent_simple import ContentAgent
from agents.progress_agent import ProgressAgent
from memory.session_manager import SessionManager
from utils.config_simple import Config


class EcoLearnOrchestrator:
    """
    Main orchestrator agent - Simple version
    """

    def __init__(self):
        Config.validate_config()

        # Configure Gemini
        genai.configure(api_key=Config.GEMINI_API_KEY)

        # Initialize specialist agents
        self.assessment_agent = AssessmentAgent()
        self.content_agent = ContentAgent()
        self.progress_agent = ProgressAgent()
        self.session_manager = SessionManager()

        # Initialize Gemini model
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)

        # Agent state
        self.current_state = "assessment"

    async def process_user_input(
        self, user_input: str, session_id: str
    ) -> Dict[str, Any]:
        """Main method to process user input through the agent system"""

        # Retrieve or create session
        session = self.session_manager.get_session(session_id)

        # Add user input to session
        if "learning_interactions" not in session:
            session["learning_interactions"] = []
        session["learning_interactions"].append({"type": "user", "content": user_input})

        # Route to appropriate agent based on current state
        if self.current_state == "assessment":
            response = await self._handle_assessment_phase(user_input, session)
        elif self.current_state == "learning":
            response = await self._handle_learning_phase(user_input, session)
        else:
            response = await self._handle_progress_phase(user_input, session)

        # Update session memory
        self.session_manager.update_session(
            session_id,
            {
                "last_interaction": user_input,
                "response": response,
                "state": self.current_state,
            },
        )

        return response

    async def _handle_assessment_phase(
        self, user_input: str, session: Dict
    ) -> Dict[str, Any]:
        """Sequential agent pattern for assessment"""
        try:
            assessment_result = await self.assessment_agent.assess_knowledge(
                user_input, session
            )
        except Exception as e:
            # If assessment fails, provide default response
            assessment_result = {
                "assessment_complete": True,
                "learning_path": [
                    "Environmental Basics",
                    "Climate Change",
                    "Sustainable Living",
                ],
                "message": "Let's start learning about environmental topics.",
            }

        if assessment_result.get("assessment_complete", False):
            self.current_state = "learning"
            learning_path = assessment_result.get(
                "learning_path",
                ["Environmental Basics", "Climate Change", "Sustainable Living"],
            )
            return {
                "type": "learning_start",
                "message": "Assessment complete! Let's start learning.",
                "learning_path": learning_path,
            }

        return assessment_result

    async def _handle_learning_phase(
        self, user_input: str, session: Dict
    ) -> Dict[str, Any]:
        """Parallel agent pattern for content delivery"""

        # Run content generation
        try:
            content_results = [
                await self.content_agent.generate_explanation(user_input, session),
                await self.content_agent.generate_examples(user_input, session),
                await self.content_agent.generate_visual_suggestion(
                    user_input, session
                ),
            ]
        except Exception as e:
            # Fallback content if API fails
            content_results = [
                {
                    "type": "explanation",
                    "content": f"Let me explain {user_input} in environmental context.",
                },
                {
                    "type": "examples",
                    "content": "There are many practical examples we can explore.",
                },
                {
                    "type": "visual_suggestion",
                    "content": "Visual aids can help understand this concept.",
                },
            ]

        # Check progress
        if len(session.get("learning_interactions", [])) >= 3:
            self.current_state = "progress"
            progress_check = await self.progress_agent.check_progress(session)
            content_results.append(progress_check)

        return {
            "type": "learning_content",
            "content": content_results,
            "session_progress": len(session.get("learning_interactions", [])),
        }

    async def _handle_progress_phase(
        self, user_input: str, session: Dict
    ) -> Dict[str, Any]:
        """Loop agent pattern for progress tracking"""
        progress_result = await self.progress_agent.evaluate_progress(
            user_input, session
        )

        # Loop back to learning if needed
        if progress_result.get("needs_more_learning", False):
            self.current_state = "learning"
            updated_result = progress_result.copy()
            updated_result["next_step"] = "continuing_learning"
            return updated_result

        return progress_result
