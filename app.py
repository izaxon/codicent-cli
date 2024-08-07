import sys
import os
from codicentpy import Codicent
from rich.console import Console
from rich.markdown import Markdown

def main():
    token = os.getenv("CODICENT_TOKEN")
    if not token:
        print("Error: Please set the CODICENT_TOKEN environment variable.")
        return

    if len(sys.argv) < 2:
        if sys.stdin.isatty():
            print("Usage: codicent <question> or codicent < chat.txt or cat chat.txt | codicent")
            return
        else:
            question = sys.stdin.read().strip()
    else:
        question = " ".join(sys.argv[1:])

    codicent = Codicent(token)

    reply = codicent.get_chat_reply(question)
    
    console = Console()
    console.print(Markdown(reply))

if __name__ == "__main__":
    main()
