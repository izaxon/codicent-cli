#!/usr/bin/env python3
"""
Demo script to showcase the enhanced Codicent CLI interface.
This script demonstrates the visual improvements without requiring an API token.
"""

import sys
import os
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
import time

def demo_interactive_mode():
    """Demonstrate the interactive mode visual features."""
    console = Console()
    
    # Show the startup banner
    console.print("\n[bold green]🤖 Codicent CLI Interactive Mode[/bold green]")
    console.print("[dim]Type your questions or use Ctrl+C to exit.[/dim]")
    console.print("[dim]Prefix with @ for info messages.[/dim]")
    console.print("─" * 50)
    
    # Simulate a few interactions
    demo_conversations = [
        {
            "user": "What is Python?",
            "bot": "Python is a high-level, interpreted programming language known for its simplicity and readability. It was created by Guido van Rossum and first released in 1991.\n\n**Key features:**\n- Easy to learn and use\n- Extensive standard library\n- Cross-platform compatibility\n- Strong community support"
        },
        {
            "user": "Can you show me a simple example?",
            "bot": "Here's a simple Python example:\n\n```python\n# Hello World in Python\nprint(\"Hello, World!\")\n\n# Working with variables\nname = \"Alice\"\nage = 25\nprint(f\"My name is {name} and I am {age} years old.\")\n```\n\nPython's syntax is clean and intuitive!"
        }
    ]
    
    for conversation in demo_conversations:
        # Show user input prompt and message in cyan
        console.print(f"[cyan]¤ {conversation['user']}[/cyan]")
        
        # Show thinking animation
        with console.status("[dim]🤔 Thinking...[/dim]", spinner="dots"):
            time.sleep(1.5)  # Simulate API call
        
        # Show bot response in green with markdown
        console.print()
        console.print(Markdown(conversation["bot"]), style="green")
        console.print()
        console.print("[dim]" + "─" * 50 + "[/dim]")
        
        # Pause for effect
        time.sleep(1)
    
    # Show info message demo
    console.print(f"[cyan]¤ @mention This is an info message[/cyan]")
    
    with console.status("[dim]Sending message...[/dim]", spinner="dots"):
        time.sleep(1)
    
    console.print("[green]✅ Message posted successfully.[/green]")
    console.print("[dim]" + "─" * 50 + "[/dim]")
    
    console.print("\n[yellow]👋 Demo completed![/yellow]")
    console.print("\n[dim]This demonstrates the enhanced visual interface of Codicent CLI:[/dim]")
    console.print("[dim]• Colored user/bot messages for clear separation[/dim]")
    console.print("[dim]• Visual separators between conversations[/dim]")
    console.print("[dim]• Rich markdown formatting for responses[/dim]")
    console.print("[dim]• Animated status indicators[/dim]")
    console.print("[dim]• Friendly emojis and visual cues[/dim]")

def main():
    """Main demo function."""
    console = Console()
    
    console.print("[bold blue]🎨 Codicent CLI Visual Enhancement Demo[/bold blue]")
    console.print("[dim]This demo shows the improved user interface without requiring an API token.[/dim]\n")
    
    try:
        demo_interactive_mode()
    except KeyboardInterrupt:
        console.print("\n[yellow]👋 Demo interrupted by user.[/yellow]")

if __name__ == "__main__":
    main()
