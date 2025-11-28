import time
from typing import Any, Dict, Optional

from utils.config import Config


class SessionManager:
    """Manages session memory and state"""

    def __init__(self):
        self.sessions: Dict[str, Dict] = {}
        self.session_expiry = Config.SESSION_EXPIRY_HOURS * 3600  # Convert to seconds

    def get_session(self, session_id: str) -> Dict[str, Any]:
        """Retrieve or create a session"""
        if session_id not in self.sessions:
            self.sessions[session_id] = self._create_new_session(session_id)

        session = self.sessions[session_id]

        # Check for expiry
        if time.time() - session["created_at"] > self.session_expiry:
            self.sessions[session_id] = self._create_new_session(session_id)

        return self.sessions[session_id]

    def update_session(self, session_id: str, updates: Dict[str, Any]):
        """Update session data"""
        if session_id in self.sessions:
            self.sessions[session_id].update(updates)
            self.sessions[session_id]["last_updated"] = time.time()

    def _create_new_session(self, session_id: str) -> Dict[str, Any]:
        """Create a new session with default structure"""
        return {
            "session_id": session_id,
            "created_at": time.time(),
            "last_updated": time.time(),
            "assessment_data": {},
            "learning_progress": [],
            "knowledge_level": "beginner",
            "preferences": {},
            "learning_interactions": [],
        }

    def compact_context(self, session: Dict, max_interactions: int = 10) -> Dict:
        """Implement context compaction to manage session size"""
        interactions = session.get("learning_interactions", [])

        if len(interactions) > max_interactions:
            # Keep most recent interactions and summarize older ones
            recent = interactions[-5:]  # Last 5 interactions
            older = interactions[:-5]

            # Summarize older interactions (simplified)
            summary = f"Previous {len(older)} interactions about environmental learning"

            session["learning_interactions"] = [
                {"type": "summary", "content": summary}
            ] + recent

        return session
