import pytest
import asyncio
from src.agents.assessment_agent import AssessmentAgent
from src.memory.session_manager import SessionManager

def test_session_manager():
    """Test session manager functionality"""
    manager = SessionManager()
    session = manager.get_session("test_id")
    assert session['session_id'] == "test_id"
    assert session['knowledge_level'] == 'beginner'

@pytest.mark.asyncio
async def test_assessment_agent_flow():
    """Test assessment agent flow"""
    agent = AssessmentAgent()
    session = {}
    
    # Test initial assessment
    result = await agent.assess_knowledge("I'm interested in climate change", session)
    assert "question" in result
    assert "type" in result
    assert result["type"] == "assessment_question"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
