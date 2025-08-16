# GPT for Shell

[![Build and Publish Docker Image on Release](https://github.com/igormcsouza/gpt4shell/actions/workflows/release.yml/badge.svg)](https://github.com/igormcsouza/gpt4shell/actions/workflows/release.yml)

A chat for terminal with pretty response

## How to use?

Set the `OPENAI_API_KEY` environment variable (go to the OPENAI to fetch that key). Then run the following command:

```bash
docker run -e OPENAI_API_KEY -it igormcsouza/gpt4shell:latest "<Your question here>"
```

And gpt will answer your question.

## Development

### Release Process

This project uses a release-driven workflow for Docker image versioning:

1. **Update Version**: Update the version in `pyproject.toml`
2. **Create Release**: Create a GitHub Release with a tag that matches the version (e.g., `v1.2.3`)
3. **Automatic Build**: The CI pipeline automatically:
   - Validates that the git tag matches the `pyproject.toml` version
   - Builds the Docker image for multiple architectures (amd64, arm64)
   - Pushes with multiple tags:
     - `igormcsouza/gpt4shell:1.2.3` (semantic version)
     - `igormcsouza/gpt4shell:sha-abc1234` (commit SHA for traceability)
     - `igormcsouza/gpt4shell:latest` (convenience tag)
   - Creates a deployment entry on GitHub

### Available Docker Tags

- **Version tags** (e.g., `:1.2.3`): Immutable releases tied to specific versions
- **SHA tags** (e.g., `:sha-abc1234`): For debugging and traceability to exact commits  
- **`:latest`**: Points to the most recent release (not recommended for production)

### Local Development

To build locally:

```bash
# Install dependencies
poetry install

# Run the application
poetry run gpt "Your question here"

# Build Docker image locally
./build
```