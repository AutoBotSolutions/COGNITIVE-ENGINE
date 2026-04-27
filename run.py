#!/usr/bin/env python3
"""
Cognitive Engine - Entry Point

Main entry point for the Cognitive Engine system.
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def print_banner():
    """Print the startup banner"""
    banner = """
╔════════════════════════════════════════════════════════════════╗
║                                                                ║ 
║                    COGNITIVE ENGINE                            ║
║                                                                ║
║              Explicit • Persistent • Inspectable               ║
║                                                                ║
║              Thought Formation System                          ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
    """
    print(banner)


async def interactive_mode():
    """Run the engine in interactive mode"""
    from api.interface import interface
    from utils.logger import logger
    
    print("\nInteractive Mode")
    print("Type 'quit' or 'exit' to stop\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            if not user_input:
                continue
            
            print("\nProcessing...")
            result = await interface.process_async(user_input)
            
            if result.get("success"):
                # Show the thought first
                top_thoughts = result.get('top_thoughts', [])
                if top_thoughts:
                    print(f"\nThought: {top_thoughts[0].get('premise', 'No thought generated')}")
                
                # Then show the human-readable response
                print(f"\nResponse: {result['output']}")
                print(f"\n[Stats: {result['thought_count']} thoughts, {result['iterations']} iterations, {result['duration_seconds']:.2f}s]")
            else:
                print(f"\nError: {result.get('error', 'Unknown error')}")
            
            print()
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            logger.error(f"Error: {e}")
            print(f"\nError: {e}\n")


async def agent_mode():
    """Run the engine in agent mode"""
    from agent.agent import CognitiveAgent
    from utils.logger import logger
    
    print("\nAgent Mode")
    print("Set a goal for the autonomous agent\n")
    
    agent = CognitiveAgent()
    
    while True:
        try:
            goal_input = input("Goal: ").strip()
            
            if goal_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            if not goal_input:
                continue
            
            print("\nSetting goal and running autonomous cycle...")
            goal_id = await agent.set_goal(goal_input)
            result = await agent.run_autonomous(goal_id, max_cycles=5)
            
            print(f"\nResult: {result}")
            print(f"Status: {agent.get_status()}\n")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            logger.error(f"Error: {e}")
            print(f"\nError: {e}\n")


def dashboard_mode():
    """Run the dashboard server"""
    from dashboard.server import start_dashboard
    from utils.logger import logger
    
    print("\nDashboard Mode")
    print("Starting dashboard server...\n")
    
    try:
        start_dashboard()
    except KeyboardInterrupt:
        print("\nDashboard stopped")


async def test_mode():
    """Run a simple test of the engine"""
    from api.interface import interface
    from utils.logger import logger
    
    print("\nTest Mode")
    print("Running basic functionality test...\n")
    
    test_queries = [
        "What is the meaning of life?",
        "Explain quantum computing in simple terms.",
        "How can I improve my productivity?"
    ]
    
    for query in test_queries:
        print(f"\nTesting: {query}")
        result = interface.process(query)
        
        if result.get("success"):
            # Show the thought first
            top_thoughts = result.get('top_thoughts', [])
            if top_thoughts:
                print(f"✓ Thought: {top_thoughts[0].get('premise', 'No thought generated')[:100]}...")
            
            # Then show the response
            print(f"  Response: {result['output'][:100]}...")
            print(f"  Stats: {result['thought_count']} thoughts, {result['iterations']} iterations")
        else:
            print(f"✗ Failed: {result.get('error')}")
    
    print("\nTest complete!")


def main():
    """Main entry point"""
    print_banner()
    
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
    else:
        print("Select mode:")
        print("1. Interactive Mode")
        print("2. Agent Mode")
        print("3. Dashboard Mode")
        print("4. Test Mode")
        print()
        
        try:
            choice = input("Enter choice (1-4): ").strip()
        except KeyboardInterrupt:
            print("\nGoodbye!")
            return
        
        modes = {
            '1': 'interactive',
            '2': 'agent',
            '3': 'dashboard',
            '4': 'test'
        }
        mode = modes.get(choice, 'interactive')
    
    try:
        if mode == 'interactive':
            asyncio.run(interactive_mode())
        elif mode == 'agent':
            asyncio.run(agent_mode())
        elif mode == 'dashboard':
            dashboard_mode()
        elif mode == 'test':
            asyncio.run(test_mode())
        else:
            print(f"Unknown mode: {mode}")
            print("Usage: python run.py [interactive|agent|dashboard|test]")
    except KeyboardInterrupt:
        print("\nGoodbye!")


if __name__ == "__main__":
    main()
