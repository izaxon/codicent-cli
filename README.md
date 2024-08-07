# Codicent CLI

Codicent CLI is a command-line interface for interacting with the Codicent API. It allows you to send questions to the Codicent chat and receive formatted responses.

## Installation

### Prerequisites

- Python 3.6 or higher
- `pip` (Python package installer)

### Steps

1. Clone the repository:
   ```sh
   git clone https://github.com/izaxon/codicent-cli.git
   cd codicent-cli
   ```

2. Install the Git dependency:
   ```sh
   pip install git+https://github.com/izaxon/codicent-py.git
   ```

3. Install the CLI application:
   ```sh
   pip install .
   ```

## Usage

1. Set the `CODICENT_TOKEN` environment variable with your Codicent API token:
   ```sh
   export CODICENT_TOKEN="YOUR_API_TOKEN"
   ```

2. Run the CLI command with your question:
   ```sh
   codicent "What can you help me with?"
   ```

3. You can also pipe a file into `codicent`:
   ```sh
   codicent < chat.txt
   cat chat.txt | codicent
   ```

## Example

```sh
$ export CODICENT_TOKEN="your_api_token"
$ codicent "What can you help me with?"
```

## Development

### Requirements

- `setuptools`
- `rich`

### Setup

1. Create a `requirements.txt` file with the following content:
   ```txt
   rich
   ```

2. Create a `setup.py` file with the following content:
   ```python
   from setuptools import setup, find_packages

   with open("requirements.txt") as f:
       required = f.read().splitlines()

   setup(
       name='codicent-cli',
       version='0.1',
       py_modules=['app'],
       install_requires=required,
       entry_points={
           'console_scripts': [
               'codicent=app:main',
           ],
       },
   )
   ```

3. Create an `app.py` file with the following content:
   ```python
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
           print("Usage: codicent <question>")
           return

       question = " ".join(sys.argv[1:])
       codicent = Codicent(token)

       reply = codicent.get_chat_reply(question)
       
       console = Console()
       console.print(Markdown(reply))

   if __name__ == "__main__":
       main()
   ```

## License

This project is licensed under the MIT License.
