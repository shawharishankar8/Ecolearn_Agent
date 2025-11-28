import pytest
import asyncio
from src.agents.assessment_agent import AssessmentAgent

@pytest.mark.asyncio
async def test_assessment_agent_initialization():
    """Test that assessment agent initializes correctly"""
    agent = AssessmentAgent()
    assert agent.current_step == 0
    assert len(agent.assessment_flow) > 0

@pytest.mark.asyncio
async def test_assessment_flow():
    """Test assessment flow progression"""
    agent = AssessmentAgent()
    session = {}
    
    # Test initial assessment
    result = await agent.assess_knowledge("I'm interested in climate change", session)
    assert "question" in result
    assert agent.current_step == 1

if __name__ == "__main__":
    pytest.main([__file__])
