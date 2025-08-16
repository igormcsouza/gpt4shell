# GPT4Shell Development Instructions

GPT4Shell is a Python CLI application that provides a terminal-based chat interface to OpenAI's GPT models using LangChain. The application is packaged as a Docker container and distributed via Docker Hub.

**CRITICAL**: Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Working Effectively

### Prerequisites and Environment Setup
- Python 3.11+ is required (Python 3.12 works)
- Poetry is the package manager - install with: `pip3 install poetry`
- Docker is available for container builds
- **REQUIRED**: Set `OPENAI_API_KEY` environment variable for the application to function

### Bootstrap and Development Workflow
- **Install dependencies**: `poetry install` -- takes ~17 seconds. NEVER CANCEL. Set timeout to 60+ seconds.
- **Run the application**: `poetry run gpt "your question here"` (requires OPENAI_API_KEY)
- **Get help**: `poetry run gpt --help`
- **Show dependency tree**: `poetry show --tree`

### Building
- **Docker build**: `./build` -- **CURRENTLY FAILS** due to network connectivity issues with Poetry 2.0.1 in Dockerfile. Build time was >2.5 minutes before failure. NEVER CANCEL docker builds - they can take 10+ minutes.
- **Local build**: Not required - Poetry handles packaging automatically

### Testing
- **No test suite exists** - This project does not have automated tests configured
- **Manual validation**: Test the CLI with: `poetry run gpt --help` and verify it shows usage information
- **Error validation**: Running `poetry run gpt "test"` without OPENAI_API_KEY should show: "Did not find openai_api_key, please add an environment variable `OPENAI_API_KEY`"

## Validation

### Manual Testing Scenarios
After making code changes, always perform these validation steps:
1. **Installation test**: `poetry install` completes successfully 
2. **Help functionality**: `poetry run gpt --help` displays usage information
3. **Error handling**: `poetry run gpt "test"` without API key shows proper error message
4. **Dependency check**: `poetry show --tree` displays the dependency structure

### Build Validation
- **Local development**: Poetry virtual environment works correctly
- **Docker builds**: Currently fail due to Poetry version issues in Dockerfile - document any fixes needed

## Key Projects and Structure

### Repository Structure
```
.
├── README.md                 # Basic usage documentation
├── Dockerfile               # Container build configuration (has issues)
├── build                    # Docker build script
├── pyproject.toml          # Poetry configuration and dependencies  
├── poetry.lock             # Locked dependency versions
├── gpt4shell/              # Main application code
│   ├── __init__.py         # Main application logic and CLI entry point
│   └── __main__.py         # Module execution entry point
├── .devcontainer/          # VS Code dev container configuration
└── .github/                # GitHub workflows and configurations
    └── workflows/
        └── publish.yml     # Docker Hub publishing workflow
```

### Important Files
- **`gpt4shell/__init__.py`**: Contains the main application logic, argument parsing, and LangChain integration
- **`pyproject.toml`**: Poetry configuration with dependencies (langchain, langchain-openai, rich)
- **`Dockerfile`**: Container configuration (currently broken due to Poetry 2.0.1 network issues)
- **`build`**: Shell script to build Docker image with version from pyproject.toml

### Dependencies
- **Runtime**: langchain, langchain-openai, rich, Python 3.11+
- **Development**: Poetry for dependency management
- **No linting tools configured** - no flake8, black, isort, or pytest in the project

## Common Tasks

### Development Commands That Work
```bash
# Install Poetry (if not installed)
pip3 install poetry

# Install project dependencies (17 seconds)
poetry install

# Run application with help
poetry run gpt --help

# Test error handling (without API key)
poetry run gpt "test question"

# Show dependency information
poetry show --tree

# Get Poetry version
poetry --version
```

### Commands That Don't Work
```bash
# Docker build - fails due to Poetry 2.0.1 network issues
./build

# Running as Python module (outside Poetry environment)
python3 -m gpt4shell --help  # ModuleNotFoundError

# Direct pip install (no setup.py available)
pip install .  # Not supported, use Poetry
```

### Timing Expectations
- **Poetry install**: ~17 seconds - NEVER CANCEL, set timeout to 60+ seconds
- **Docker build**: >2.5 minutes before failure - NEVER CANCEL, set timeout to 15+ minutes
- **Application startup**: Immediate once dependencies are installed

### Version Information
- **Current version**: 0.1.0.1 (defined in pyproject.toml)
- **Python requirement**: ^3.11 (works with 3.12)
- **Poetry version used**: 2.1.4+

## Troubleshooting

### Common Issues
1. **Missing OPENAI_API_KEY**: Application requires this environment variable to function
2. **Poetry not found**: Install with `pip3 install poetry`
3. **Docker build fails**: Known issue with Poetry 2.0.1 network connectivity in Dockerfile
4. **Module not found outside Poetry**: Always use `poetry run` commands

### Known Limitations
- No automated tests or linting tools configured
- Docker build currently broken due to Poetry version issues
- Application cannot run without valid OpenAI API key
- No development dependencies or pre-commit hooks configured

## Making Changes

### Before Committing
- Run `poetry install` to ensure dependencies are correct
- Test `poetry run gpt --help` to verify CLI works
- Test error handling by running without API key
- **No linting step required** - project has no linting tools configured

### After Changes
- Verify the application still starts and shows help correctly
- Test that dependencies install without errors  
- Update version in pyproject.toml if needed for releases
- **No CI testing** - GitHub workflow only publishes to Docker Hub

## Application Usage

### CLI Interface
```bash
# Get help
poetry run gpt --help

# Ask a question (requires OPENAI_API_KEY environment variable)
export OPENAI_API_KEY="your-key-here"
poetry run gpt "What is Python?"

# Docker usage (when build works)
docker run -e OPENAI_API_KEY -it igormcsouza/gptforshell:0.1.0 "Your question here"
```

### Error Messages
- **No API key**: "Did not find openai_api_key, please add an environment variable `OPENAI_API_KEY`"
- **Invalid key**: OpenAI API authentication errors
- **Network issues**: LangChain HTTP connection errors