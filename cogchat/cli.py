"""
CogChat CLI - Command Line Interface

A friendly command-line interface for interacting with the Cognitive Engine.
"""

import asyncio
import sys
from typing import Optional

# Handle both module and direct execution
try:
    from .chat import CogChat, chat
except ImportError:
    # Add parent directory to path for direct execution
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from cogchat.chat import CogChat, chat


class CogChatCLI:
    """Command-line interface for CogChat"""
    
    def __init__(self):
        self.chat = CogChat()
        self.running = True
    
    def print_banner(self):
        """Print the startup banner"""
        banner = """
╔════════════════════════════════════════════════════════════════╗
║                                                                ║ 
║                    COGCHAT                                    ║ 
║                                                                ║
║              Cognitive Engine Chat Interface                   ║
║                                                                ║
║              Friendly • Simple • Powerful                      ║ 
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def print_help(self):
        """Print help information"""
        help_text = """
CogChat Commands:
  /help           - Show this help message
  /quit, /exit    - Exit the chat
  /new            - Start a new session
  /sessions       - List all sessions
  /info           - Show current session info
  /trace          - Toggle cognitive trace display
  /clear          - Clear current session
  
Any other text will be sent to the Cognitive Engine for processing.
        """
        print(help_text)
    
    def print_session_info(self):
        """Print current session information"""
        session = self.chat.get_active_session()
        if session:
            info = self.chat.get_session_info()
            print(f"\nSession: {info['session_id']}")
            print(f"Messages: {info['message_count']}")
            print(f"Created: {info['created_at']}")
        else:
            print("\nNo active session. Type /new to start one.")
    
    def print_sessions(self):
        """Print all sessions"""
        sessions = self.chat.list_sessions()
        if not sessions:
            print("\nNo sessions yet.")
            return
        
        print("\nSessions:")
        for session in sessions:
            marker = " (active)" if session['session_id'] == self.chat.active_session_id else ""
            print(f"  {session['session_id']}: {session['message_count']} messages{marker}")
    
    async def process_command(self, command: str) -> bool:
        """
        Process a command.
        
        Returns True if the command was handled, False if it should be treated as a message.
        """
        if command.startswith('/'):
            parts = command.split()
            cmd = parts[0].lower()
            
            if cmd in ['/quit', '/exit']:
                self.running = False
                return True
            elif cmd == '/help':
                self.print_help()
                return True
            elif cmd == '/new':
                session_id = self.chat.create_session()
                print(f"\nCreated new session: {session_id}")
                return True
            elif cmd == '/sessions':
                self.print_sessions()
                return True
            elif cmd == '/info':
                self.print_session_info()
                return True
            elif cmd == '/clear':
                if self.chat.active_session_id:
                    self.chat.delete_session(self.chat.active_session_id)
                    print("\nSession cleared.")
                return True
            else:
                print(f"\nUnknown command: {cmd}")
                print("Type /help for available commands.")
                return True
        
        return False
    
    async def run(self):
        """Run the CLI interface"""
        self.print_banner()
        self.print_help()
        
        # Create initial session
        session_id = self.chat.create_session()
        print(f"\nCreated session: {session_id}")
        print("Type your message or /help for commands.\n")
        
        while self.running:
            try:
                # Get user input
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                # Check for commands
                if await self.process_command(user_input):
                    continue
                
                # Send to Cognitive Engine
                print("Processing...")
                result = await self.chat.chat(user_input, include_trace=False)
                
                if 'error' in result:
                    print(f"\nError: {result['error']}")
                else:
                    print(f"\nCognitive Engine: {result['response']}")
                    print(f"\n[Session: {result['session_id']}, Message #{result['message_number']}]")
                
                print()
                
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                self.running = False
            except EOFError:
                print("\n\nGoodbye!")
                self.running = False
            except Exception as e:
                print(f"\nError: {e}")
                print("Type /help for commands or /quit to exit.\n")


async def main():
    """Main entry point for CogChat CLI"""
    cli = CogChatCLI()
    await cli.run()


if __name__ == "__main__":
    asyncio.run(main())
