#!/usr/bin/env python3
"""
Simple test script for EcoLearn Tutor
"""

import asyncio
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from src.agents.orchestrator_simple import EcoLearnOrchestrator
from src.utils.config_simple import Config


async def test_basic_functionality():
    """Test basic functionality"""
    try:
        print("Testing EcoLearn Tutor basic functionality...")

        # Validate config
        Config.validate_config()
        print("Configuration validated successfully")

        # Create orchestrator
        orchestrator = EcoLearnOrchestrator()
        print("Orchestrator created successfully")

        # Test assessment phase
        session_id = "test_session"
        response1 = await orchestrator.process_user_input(
            "I want to learn about climate change", session_id
        )
        print("First response:", response1.get("type", "unknown"))

        print("Basic functionality test passed!")
        return True

    except Exception as e:
        print(f"Test failed: {str(e)}")
        return False


if __name__ == "__main__":
    asyncio.run(test_basic_functionality())
