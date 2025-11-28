#!/usr/bin/env python3
import asyncio
import os
import sys
from typing import Optional

sys.path.append(os.path.dirname(__file__))

from agents.orchestrator_simple import EcoLearnOrchestrator
from utils.config_simple import Config


class EcoLearnTutor:
    def __init__(self):
        self.orchestrator = None
        self.session_id = "default_session"

    async def initialize(self):
        try:
            print("Initializing EcoLearn Tutor...")
            Config.validate_config()
            self.orchestrator = EcoLearnOrchestrator()

            print("\n" + "=" * 50)
            print("WELCOME TO ECOLEARN TUTOR")
            print("=" * 50)
            print("I'm your AI environmental education assistant!")
            print("\nI'll help you learn about:")
            print("- Climate change and sustainability")
            print("- Environmental science and conservation")
            print("- Green technologies and practices")
            print("- Biodiversity and ecosystem protection")
            print("\nFIRST: I'll ask a few questions to understand your interests")
            print("THEN: I'll create a personalized learning path for you")
            print("FINALLY: We'll explore environmental topics together!")
            print("\nTo get started, tell me:")
            print("- What environmental topics interest you?")
            print("- OR what would you like to learn about?")
            print("- OR just say 'hello' to begin!")
            print("\nType 'quit', 'exit', or 'bye' to end the session")
            print("-" * 50)

            return True
        except Exception as e:
            print(f"Failed to initialize: {str(e)}")
            return False

    async def run(self):
        if not await self.initialize():
            return

        try:
            while True:
                try:
                    user_input = input("\nYou: ").strip()

                    if user_input.lower() in ["quit", "exit", "bye"]:
                        print("\nThanks for learning with EcoLearn Tutor! Goodbye!")
                        break
                    if not user_input:
                        print("Please type something to continue...")
                        continue

                    # Make sure orchestrator is initialized (helps static analyzers and prevents None access)
                    assert self.orchestrator is not None, "Orchestrator not initialized"
                    response = await self.orchestrator.process_user_input(
                        user_input, self.session_id
                    )
                    self._display_response(response)

                except KeyboardInterrupt:
                    print("\n\nSession ended. Thanks for using EcoLearn Tutor!")
                    break
                except Exception as e:
                    print(f"Error: {str(e)}")
                    continue

        except Exception as e:
            print(f"Application error: {str(e)}")

    def _display_response(self, response):
        response_type = response.get("type", "unknown")

        if response_type == "assessment_question":
            question = response.get(
                "question", "Tell me about your environmental interests."
            )
            print(f"\nEcoLearn: {question}")
            progress = response.get("progress", "")
            if progress:
                print(f"Assessment Progress: {progress}")

        elif response_type == "learning_start":
            print(f"\nEcoLearn: {response.get('message', 'Lets start learning!')}")
            learning_path = response.get("learning_path", [])
            if learning_path:
                print("\nYour personalized learning path:")
                for i, topic in enumerate(learning_path, 1):
                    print(f"  {i}. {topic}")
            print("\nNow you can ask me anything about environmental topics!")
            print("Try questions like:")
            print("- 'Explain climate change'")
            print("- 'What is renewable energy?'")
            print("- 'How can I reduce my carbon footprint?'")

        elif response_type == "learning_content":
            content_items = response.get("content", [])
            print("\nEcoLearn:")
            for item in content_items:
                if isinstance(item, dict):
                    content_type = item.get("type", "")
                    content = item.get("content", "")

                    if content_type == "explanation":
                        print(f"EXPLANATION: {content}")
                    elif content_type == "examples":
                        print(f"EXAMPLES: {content}")
                    elif content_type == "visual_suggestion":
                        print(f"VISUAL AID: {content}")
                    elif content_type == "progress_check":
                        print(f"PROGRESS: {content.get('message', '')}")
                    else:
                        print(f"- {content}")
                else:
                    print(f"- {item}")

        elif response_type == "progress_check":
            print(f"\nEcoLearn: {response.get('message', 'Checking your progress...')}")

        else:
            print(
                f"\nEcoLearn: {response.get('message', 'How can I help you learn about the environment?')}"
            )


async def main():
    tutor = EcoLearnTutor()
    await tutor.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nGoodbye!")
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        sys.exit(1)
