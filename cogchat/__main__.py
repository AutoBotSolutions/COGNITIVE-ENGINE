"""
CogChat Entry Point

Main entry point for running CogChat in different modes.
"""

import asyncio
import sys
from typing import Optional


def print_usage():
    """Print usage information"""
    print("""
CogChat - Cognitive Engine Chat Interface

Usage:
    python -m cogchat [mode]

Modes:
    cli        - Command-line interface (default)
    server     - Web server interface
    test       - Test the system

Examples:
    python -m cogchat
    python -m cogchat cli
    python -m cogchat server
    python -m cogchat test
    """)


async def run_cli():
    """Run the CLI interface"""
    from .cli import main
    await main()


def run_server():
    """Run the web server"""
    from .server import start_server
    start_server()


async def run_test():
    """Test the system"""
    from .chat import chat
    
    print("\nCogChat Test Mode")
    print("Testing chat functionality...\n")
    
    # Create a session
    session_id = chat.create_session()
    print(f"Created session: {session_id}")
    
    # Send a test message
    print("Sending test message...")
    result = await chat.chat("Hello, this is a test message.")
    
    if 'error' in result:
        print(f"Error: {result['error']}")
        return False
    
    print(f"Response: {result['response']}")
    print(f"Session: {result['session_id']}")
    print(f"Message #: {result['message_number']}")
    
    # Get session info
    session_info = chat.get_session_info(session_id)
    print(f"\nSession Info:")
    print(f"  Messages: {session_info['message_count']}")
    print(f"  Created: {session_info['created_at']}")
    
    print("\n✓ Test passed!")
    return True


def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
    else:
        mode = "cli"
    
    if mode in ["-h", "--help", "help"]:
        print_usage()
        return
    
    if mode == "cli":
        asyncio.run(run_cli())
    elif mode == "server":
        run_server()
    elif mode == "test":
        asyncio.run(run_test())
    else:
        print(f"Unknown mode: {mode}")
        print_usage()


if __name__ == "__main__":
    main()
