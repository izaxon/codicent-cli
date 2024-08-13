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

    if question.strip().startswith("@"):
        response = codicent.post_message(question, type="info")
        console = Console()
        console.print("Message posted successfully.")
    else:
        response = codicent.get_chat_reply(question)
        console = Console()
        console.print(Markdown(response))

if __name__ == "__main__":
    main()
