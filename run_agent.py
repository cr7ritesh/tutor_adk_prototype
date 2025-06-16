### 5. `run_agent.py` (Optional - for custom running)python
#!/usr/bin/env python3
"""
Custom runner for the AI Tutor Agent
"""

import os
import sys
from pathlib import Path

# Add the agent directory to Python path
agent_dir = Path(__file__).parent / "ai_tutor_agent"
sys.path.insert(0, str(agent_dir))

from ai_tutor_agent import ai_tutor_agent

def main():
    """Run the AI Tutor Agent in terminal mode"""
    print("🎓 AI Tutor Agent Starting...")
    print("Type 'exit' to quit, 'help' for assistance")
    print("-" * 50)
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("👋 Thanks for using AI Tutor! Keep learning!")
                break
            elif user_input.lower() == 'help':
                print_help()
                continue
            elif not user_input:
                continue
                
            # Here you would integrate with ADK's chat functionality
            # For this prototype, we'll show a simple response
            print(f"\n🤖 AI Tutor: I received your message: '{user_input}'")
            print("Note: Run 'adk chat ai_tutor_agent' for full functionality")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def print_help():
    """Print help information"""
    help_text = """
🎓 AI Tutor Commands:

Basic Examples:
- "Assess my knowledge level"
- "I want to learn Python basics"
- "Give me the intro to AI quiz"
- "Help me understand machine learning"
- "What's my current progress?"

Assessment Examples:
- "I'm new to AI and programming"
- "I know some Python but new to AI"
- "I'm experienced with both AI and programming"

For full functionality, use:
- adk web (browser interface)
- adk chat ai_tutor_agent (terminal chat)
"""
    print(help_text)

if __name__ == "__main__":
    main()