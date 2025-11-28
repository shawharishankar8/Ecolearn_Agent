from typing import Any, Dict, List

import google.generativeai as genai
from assessment_agent import AssessmentAgent
from content_agent import ContentAgent
from progress_agent import ProgressAgent

from memory.session_manager import SessionManager
from utils.config import Config


class EcoLearnOrchestrator:
    """
    Main orchestrator agent that manages the multi-agent system
    Implements Sequential and Parallel agent patterns
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

        # Initialize Gemini model with available model
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)

        # Agent state
        self.current_state = "assessment"  # assessment, learning, progress

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
        assessment_result = await self.assessment_agent.assess_knowledge(
            user_input, session
        )

        if assessment_result.get("assessment_complete", False):
            self.current_state = "learning"
            # Ensure learning_path exists
            learning_path = assessment_result.get(
                "learning_path",
                [
                    "Environmental Basics",
                    "Climate Change",
                    "Sustainable Living",
                    "Conservation",
                ],
            )
            return {
                "type": "learning_start",
                "message": "Assessment complete! Let's start learning about environmental topics.",
                "learning_path": learning_path,
            }

        return assessment_result

    async def _handle_learning_phase(
        self, user_input: str, session: Dict
    ) -> Dict[str, Any]:
        """Parallel agent pattern for content delivery"""

        # Run content generation in parallel
        content_tasks = [
            self.content_agent.generate_explanation(user_input, session),
            self.content_agent.generate_examples(user_input, session),
            self.content_agent.generate_visual_suggestion(user_input, session),
        ]

        # Use asyncio.gather for true parallelism
        import asyncio

        content_results = await asyncio.gather(*content_tasks, return_exceptions=True)

        # Handle any exceptions
        clean_results = []
        for result in content_results:
            if isinstance(result, Exception):
                clean_results.append(
                    {
                        "type": "error",
                        "content": f"Content generation error: {str(result)}",
                    }
                )
            else:
                clean_results.append(result)

        # Check if we should transition to progress tracking
        if len(session.get("learning_interactions", [])) >= 3:
            self.current_state = "progress"
            progress_check = await self.progress_agent.check_progress(session)
            clean_results.append(progress_check)

        return {
            "type": "learning_content",
            "content": clean_results,
            "session_progress": len(session.get("learning_interactions", [])),
        }

    async def _handle_progress_phase(
        self, user_input: str, session: Dict
    ) -> Dict[str, Any]:
        """Loop agent pattern for progress tracking"""
        progress_result = await self.progress_agent.evaluate_progress(
            user_input, session
        )

        # Loop back to learning if more content is needed
        if progress_result.get("needs_more_learning", False):
            self.current_state = "learning"
            # Fix: Create a new dictionary to avoid type conflict
            updated_result = progress_result.copy()
            updated_result["next_step"] = "continuing_learning"
            return updated_result

        return progress_result
