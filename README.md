# GPT for Shell

[![Publish on Docker Hub](https://github.com/igormcsouza/gpt4shell/actions/workflows/publish.yml/badge.svg)](https://github.com/igormcsouza/gpt4shell/actions/workflows/publish.yml)

A chat for terminal with pretty response

## How to use?

Set the `OPENAI_API_KEY` environment variable (go to the OPENAI to fetch that key). Then run the following command:

```bash
docker run -e OPENAI_API_KEY -it igormcsouza/gptforshell:0.1.0 "<Your question here>"
```

And gpt will answer your question.

## Configuration

GPT4Shell supports configuration through a JSON file located at `~/.gpt4shell/config.json`. This allows you to customize the AI model, provider, and other settings.

### Creating a Configuration File

You can create an example configuration file by running:

```bash
gpt --config-example
```

This will create a file at `~/.gpt4shell/config.json` with example settings.

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `model` | string | `"gpt-3.5-turbo"` | The AI model to use (e.g., "gpt-4", "gpt-3.5-turbo") |
| `provider` | string | `"openai"` | The AI provider (currently only "openai" is supported) |
| `temperature` | number | `1.0` | Controls randomness (0.0 = deterministic, 2.0 = very random) |
| `prompt_template` | string | `"Answer the question..."` | Template for how the AI should behave |
| `max_tokens` | number/null | `null` | Maximum tokens in response (null = provider default) |
| `api_base` | string/null | `null` | Custom API base URL (null = provider default) |

### Example Configuration

```json
{
  "model": "gpt-4",
  "provider": "openai",
  "temperature": 0.7,
  "prompt_template": "You are a helpful assistant. Answer the question concisely and accurately:\n{question}",
  "max_tokens": 1000,
  "api_base": null
}
```

### Using Configuration with Docker

To use a custom configuration with Docker, mount your config file into the container:

```bash
docker run -e OPENAI_API_KEY -v ~/.gpt4shell/config.json:/root/.gpt4shell/config.json -it igormcsouza/gptforshell:0.1.0 "<Your question here>"
```

If no configuration file is found, GPT4Shell will use sensible defaults.