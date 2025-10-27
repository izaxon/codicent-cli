# Copilot Instructions for Codicent CLI

**ALWAYS follow these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.**

## Working Effectively

### Bootstrap, Build, and Test the Repository
- Install dependencies: `pip install -r requirements.txt` - completes in 3 seconds. NEVER CANCEL.
- Install in development mode: `pip install -e .` - completes in 2 seconds. NEVER CANCEL.
- Validate installation: `codicent --help` and `codicent --version` - both work instantly without authentication
- Run core tests: `python3 -m unittest test_app.TestCodicentCLI -v` - completes in 0.3 seconds. NEVER CANCEL.

### Project Structure
- **Single-file architecture**: All logic concentrated in `app.py` 
- **Authentication module**: `auth.py` handles OAuth device flow and token caching
- **Test suite**: `test_app.py` with comprehensive unit tests (some need updates for auth changes)
- **Dependencies**: Listed in `requirements.txt` - all available on PyPI, no git dependencies needed
- **Documentation**: `README.md`, `DEVICE_AUTH_README.md` for authentication flow details

### Dependencies and Installation
```bash
# Method 1: Direct dependency installation (RECOMMENDED - 3 seconds)
pip install -r requirements.txt
pip install -e .

# Method 2: Individual package installation
pip install rich codicent-py prompt_toolkit requests
pip install -e .
```

### Testing and Validation

#### Core Functionality Tests (No Authentication Required)
```bash
# Test CLI help and version - instant response, works offline
codicent --help
codicent --version

# Test authentication status (shows proper error handling)
codicent status  # Returns "Not authenticated" 

# Basic syntax validation
python3 -m py_compile app.py auth.py test_app.py
```

#### Unit Test Suite - 0.3 seconds total. NEVER CANCEL.
```bash
# Run main test suite (avoid interactive tests that hang)  
python3 -m unittest test_app.TestCodicentCLI -v

# Run specific quick tests
python3 -m unittest test_app.TestCodicentCLI.test_show_help test_app.TestCodicentCLI.test_show_version -v

# DO NOT run: python3 test_app.py directly - hangs on interactive mode tests
# DO NOT run: python3 run_tests.py - contains outdated version check and hangs
```

#### Manual Validation Scenarios
**ALWAYS run these scenarios after making changes:**

1. **CLI Help and Version Test**:
   ```bash
   codicent --help  # Should show usage, options, examples
   codicent --version  # Should show "Codicent CLI v0.4.8"
   ```

2. **Authentication Flow Test** (no network required):
   ```bash
   codicent status  # Should show "Not authenticated"
   codicent "test" # Should show proper authentication error
   ```

3. **Interactive Mode Test**:
   ```bash
   # Start interactive mode (will show auth error, then Ctrl+C to exit)
   codicent -t
   # Should show: "🤖 Codicent CLI Interactive Mode" before auth error
   ```

4. **Piped Input Test**:
   ```bash
   echo "test question" | codicent  # Should handle piped input properly
   ```

## Authentication System
- **Device flow**: `codicent auth` initiates OAuth device authorization (requires network)
- **Token caching**: Tokens stored in `~/.codicent_token` with 600 permissions
- **Fallback**: `CODICENT_TOKEN` environment variable for legacy support
- **Commands**: `auth`, `status`, `logout` for authentication management

## Application Architecture

### Core Application (`app.py`)
- **Dual execution modes**: One-shot commands vs interactive chat (`-t` flag)
- **Input handling**: Arguments, stdin pipes, interactive prompts
- **Authentication**: Device flow (preferred) or environment variable fallback

### Mode Detection Logic
```python
interactive = False
if "-t" in sys.argv:
    interactive = True
elif len(sys.argv) == 1:
    interactive = True  # No args = interactive mode
```

### Message Type Routing
- Messages starting with `@` → `codicent.post_message()` (info type)
- Regular messages → `codicent.post_chat_reply()` with conversation tracking

### Conversation State Management
```python
conversationId = None  # Tracks conversation in interactive mode
conversationId = response["id"]  # Updated after each chat reply
```

## Development Patterns

### Adding New Command Flags
Add flag detection in `main()` before mode detection:
```python
if "--new-flag" in sys.argv:
    # Handle new flag
    sys.argv.remove("--new-flag")
```

### Extending Message Types  
Modify routing logic in `handle_question()`:
```python
if question.strip().startswith("@"):
    # Existing @ logic
elif question.strip().startswith("#"):
    # New # logic
```

### UI/UX Patterns
- **Rich library**: All formatting, spinners, markdown rendering
- **Prompt toolkit**: Interactive input with key bindings
- **Color scheme**: Errors (red), warnings (yellow), success (green)
- **Interactive prompt**: `¤` symbol with multi-line support

## Validation Checklist
Always run these before committing changes:

1. **Syntax Check**: `python3 -m py_compile app.py auth.py` - instant
2. **Basic Tests**: `python3 -m unittest test_app.TestCodicentCLI.test_show_help test_app.TestCodicentCLI.test_show_version` - instant  
3. **CLI Validation**: `codicent --help && codicent --version` - instant
4. **Authentication Validation**: `codicent status` - instant
5. **Installation Test**: `pip install -e .` - 2 seconds. NEVER CANCEL.

## Key Files and Locations
- **Main application**: `app.py` - single-file architecture
- **Authentication**: `auth.py` - OAuth device flow implementation  
- **Tests**: `test_app.py` - comprehensive test suite
- **Setup**: `setup.py` - package configuration
- **Dependencies**: `requirements.txt` - all PyPI packages
- **Documentation**: `README.md` - usage examples and setup
- **Auth documentation**: `DEVICE_AUTH_README.md` - device flow details

## Troubleshooting
- **Tests hanging**: Avoid `test_app.TestInteractiveMode` tests - they hang in non-interactive environments
- **Version mismatch**: `run_tests.py` checks for v0.4.3 but current is v0.4.8 - ignore this script
- **Network errors**: All basic functionality works offline, only actual API calls need network
- **Authentication**: Use `codicent status` to check auth state, `codicent auth` requires network access

## Common Tasks
- **Test changes**: Run `python3 -m unittest test_app.TestCodicentCLI -v` - 0.3 seconds
- **Validate CLI**: Run `codicent --help && codicent --version` - instant  
- **Check auth**: Run `codicent status` - instant
- **Install changes**: Run `pip install -e .` - 2 seconds
- **Syntax validation**: Run `python3 -m py_compile app.py auth.py` - instant
