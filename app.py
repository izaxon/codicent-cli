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
    codicent = Codicent(token)
    conversationId = None

    interactive = False
    if "-t" in sys.argv:
        interactive = True
        sys.argv.remove("-t")
    elif len(sys.argv) == 1:
        interactive = True
        
    if not interactive:
        if len(sys.argv) < 2:
            if sys.stdin.isatty():
                print("Usage: codicent <question> or codicent < chat.txt or cat chat.txt | codicent or codicent (equal to codicent -t)")
                return
            question = sys.stdin.read().strip()
        else:
            question = " ".join(sys.argv[1:])
    else:
        if len(sys.argv) > 1:
            question = " ".join(sys.argv[1:])
        elif not sys.stdin.isatty():
            question = sys.stdin.read().strip()
        else: 
            question = ""

    def handle_question(question):
        nonlocal conversationId
        if question.strip().startswith("@"):
            response = codicent.post_message(question, type="info")
            console = Console()
            console.print("Message posted successfully.")
        else:
            console = Console()
            # Wrap the call in a spinner animation.
            with console.status("", spinner="dots"):
                response = codicent.post_chat_reply(question, conversationId)
            conversationId = response["id"]
            if interactive: console.print()
            console.print(Markdown(response["content"]))
            console.print() 

    if question != "":
        handle_question(question)
    
    if interactive:
        while True:
            try:
                question = input("¤ ")
            except KeyboardInterrupt:
                break
            except EOFError:
                break
            if question.strip() != "":
                handle_question(question)

if __name__ == "__main__":
    main()
