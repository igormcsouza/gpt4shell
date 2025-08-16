# GPT4Shell

[![Publish on Docker Hub](https://github.com/igormcsouza/gpt4shell/actions/workflows/publish.yml/badge.svg)](https://github.com/igormcsouza/gpt4shell/actions/workflows/publish.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

A terminal-based chat application that provides a beautiful, rich-formatted interface to interact with OpenAI's GPT models directly from your command line.

## ✨ Features

- 🤖 **AI-Powered**: Interact with GPT-3.5-turbo for intelligent responses
- 🎨 **Rich Formatting**: Beautiful terminal output with syntax highlighting
- 🐳 **Docker Ready**: Easy deployment with pre-built Docker images  
- ⚡ **Simple CLI**: Single command to ask questions and get answers
- 🔧 **Developer Friendly**: Built with modern Python tools (Poetry, LangChain)

## 📋 Requirements

- Python 3.11+ (for local installation)
- OpenAI API Key ([get one here](https://platform.openai.com/api-keys))
- Docker (for containerized usage)

## 🚀 Installation & Usage

### Option 1: Docker (Recommended)

The easiest way to use GPT4Shell is with Docker:

```bash
# Set your OpenAI API key
export OPENAI_API_KEY="your-api-key-here"

# Run with Docker
docker run -e OPENAI_API_KEY -it igormcsouza/gptforshell:0.1.0.1 "What is the meaning of life?"
```

### Option 2: Local Installation with Poetry

For development or local use:

```bash
# Clone the repository
git clone https://github.com/igormcsouza/gpt4shell.git
cd gpt4shell

# Install Poetry (if not already installed)
pip install poetry

# Install dependencies
poetry install

# Set your OpenAI API key
export OPENAI_API_KEY="your-api-key-here"

# Run the application
poetry run gpt "How do I write a Python function?"
```

### Option 3: Development Setup

```bash
# Clone and enter the project
git clone https://github.com/igormcsouza/gpt4shell.git
cd gpt4shell

# Install in development mode
poetry install

# Set your OpenAI API key
export OPENAI_API_KEY="your-api-key-here"

# Run using Poetry
poetry run gpt "Explain quantum computing"
```

## 💡 Usage Examples

```bash
# Ask about programming
poetry run gpt "How do I create a REST API in Python?"

# Get explanations
poetry run gpt "Explain the difference between AI and ML"

# Ask for code examples  
poetry run gpt "Show me a Python script to read CSV files"

# General questions
poetry run gpt "What are the benefits of using containers?"
```

### Getting Help

```bash
poetry run gpt --help
```

## 🏗️ Project Structure

```
gpt4shell/
├── gpt4shell/           # Main package
│   ├── __init__.py      # CLI entry point and main logic
│   └── __main__.py      # Module execution entry
├── Dockerfile           # Container configuration
├── pyproject.toml       # Project metadata and dependencies
├── poetry.lock          # Locked dependencies
├── build               # Docker build script
└── README.md           # This file
```

## 🛠️ Development

### Building the Docker Image

```bash
# Make the build script executable
chmod +x build

# Build the image (uses version from pyproject.toml)
./build
```

### Running Tests

Currently, this project focuses on simplicity and doesn't include a test suite. Contributions to add testing are welcome!

### Code Style

The project uses Poetry for dependency management and follows Python best practices:

- **LangChain**: For AI model integration
- **Rich**: For beautiful terminal output
- **OpenAI**: For GPT model access

## 📚 How It Works

GPT4Shell uses:
1. **LangChain** to create a simple prompt template and chain
2. **OpenAI API** to connect to GPT-3.5-turbo model  
3. **Rich** library to format and display responses beautifully in the terminal
4. **Poetry** for modern Python dependency management

The application takes your question, sends it to OpenAI's API with a simple prompt template, and displays the formatted response in your terminal.

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Make** your changes
4. **Commit** your changes (`git commit -m 'Add amazing feature'`)
5. **Push** to the branch (`git push origin feature/amazing-feature`)
6. **Open** a Pull Request

### Ideas for Contributions

- Add conversation history
- Support for different GPT models
- Configuration file support
- Add comprehensive testing
- Improve error handling
- Add more output formatting options

## 📝 License

This project is open source. Please check the repository for license details.

## 🙏 Acknowledgments

- [OpenAI](https://openai.com/) for providing the GPT API
- [LangChain](https://langchain.com/) for the AI framework
- [Rich](https://rich.readthedocs.io/) for beautiful terminal formatting