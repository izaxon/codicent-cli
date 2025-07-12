# Copilot Instructions for Codicent CLI

## Project Overview
Codicent CLI is a Python command-line interface that wraps the Codicent API, providing both one-shot command execution and interactive chat sessions. The entire application logic resides in `app.py` as a single-module CLI tool.

## Architecture & Key Components

### Core Application (`app.py`)
- **Single-file architecture**: All logic concentrated in one module for simplicity
- **Dual execution modes**: One-shot commands vs interactive chat sessions (`-t` flag)
- **Input handling**: Supports arguments, stdin pipes, and interactive prompts
- **API integration**: Uses external `codicentpy` package for Codicent API calls

### Key Patterns

#### Mode Detection Logic
```python
interactive = False
if "-t" in sys.argv:
    interactive = True
elif len(sys.argv) == 1:
    interactive = True  # No args = interactive mode
```

#### Message Type Routing
- Messages starting with `@` → `codicent.post_message()` (info type)
- Regular messages → `codicent.post_chat_reply()` with conversation tracking

#### Conversation State Management
```python
conversationId = None  # Tracks conversation in interactive mode
conversationId = response["id"]  # Updated after each chat reply
```

## Development Workflows

### Environment Setup
```bash
# Install the git dependency first (required before setup.py)
pip install git+https://github.com/izaxon/codicent-py.git

# Install in development mode
pip install -e .
```

### Testing the CLI
```bash
# Set required environment variable
export CODICENT_TOKEN="your_token"

# Test one-shot mode
codicent "test question"

# Test interactive mode
codicent -t

# Test piped input
echo "test" | codicent
```

## Project-Specific Conventions

### Dependencies Management
- **Split approach**: `requirements.txt` includes git dependencies, `setup.py` excludes them
- **Git dependency pattern**: External `codicentpy` package installed separately before setup
- **Rich library**: Used for spinner animations and markdown rendering

### Error Handling Patterns
- **Environment validation**: Always check `CODICENT_TOKEN` before API calls
- **Graceful interrupts**: Handle `KeyboardInterrupt` and `EOFError` in interactive mode
- **Input validation**: Check `sys.stdin.isatty()` to detect piped vs terminal input

### UI/UX Patterns
- **Loading feedback**: Spinner animation during API calls using `rich.console.status`
- **Markdown rendering**: All API responses rendered as markdown via `rich.Markdown`
- **Interactive prompt**: Custom prompt character `¤` for brand consistency

## Integration Points

### External Dependencies
- **codicentpy**: Core API client (git dependency from `izaxon/codicent-py`)
- **rich**: Terminal formatting and animations
- **Standard library**: Heavy reliance on `sys`, `os` for CLI operations

### API Integration
- **Authentication**: Token-based via `CODICENT_TOKEN` environment variable
- **Chat API**: `post_chat_reply(question, conversationId)` for conversational interactions
- **Message API**: `post_message(question, type="info")` for @-prefixed messages

## Common Modification Patterns

### Adding New Command Flags
Add flag detection after the interactive mode logic in `main()`:
```python
if "--new-flag" in sys.argv:
    # Handle new flag
    sys.argv.remove("--new-flag")
```

### Extending Message Types
Modify the routing logic in `handle_question()`:
```python
if question.strip().startswith("@"):
    # Existing @ logic
elif question.strip().startswith("#"):
    # New # logic
```

### Changing Output Formatting
Customize the response rendering in `handle_question()`:
```python
console.print(Markdown(response["content"]))  # Current
# Replace with custom formatting
```

## File Structure Notes
- **Single module design**: Keep all logic in `app.py` unless complexity significantly increases
- **No test directory**: Currently no formal testing structure
- **Minimal configuration**: No config files, relies on environment variables and command-line args
