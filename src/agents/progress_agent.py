from typing import Dict, Any

class ProgressAgent:
    """Progress tracking agent"""
    
    async def check_progress(self, session: dict) -> Dict[str, Any]:
        """Check learning progress"""
        interactions = len(session.get('learning_interactions', []))
        progress_percentage = min(100, (interactions / 10) * 100)
        
        return {
            "type": "progress_check",
            "progress_percentage": progress_percentage,
            "interactions_count": interactions,
            "message": f"You've completed {progress_percentage:.0f}% of this learning session."
        }
    
    async def evaluate_progress(self, user_input: str, session: dict) -> Dict[str, Any]:
        """Evaluate overall progress and determine next steps"""
        interactions = len(session.get('learning_interactions', []))
        
        # Simple logic: if less than 5 interactions, suggest more learning
        needs_more_learning = interactions < 5
        
        return {
            "needs_more_learning": needs_more_learning,
            "total_interactions": interactions,
            "recommendation": "Continue learning" if needs_more_learning else "Ready for assessment"
        }
