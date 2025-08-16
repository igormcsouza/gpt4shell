# Release Process Guide

## Overview

This repository now uses a **release-driven workflow** for Docker image versioning, ensuring immutable releases and proper version tracking.

## How to Create a Release

### 1. Update Version
```bash
# Update version in pyproject.toml
poetry version patch  # or minor, major
```

### 2. Create GitHub Release
1. Go to GitHub repository → Releases → "Create a new release"
2. Use tag format: `v{version}` (e.g., `v0.2.0`)
3. Tag must match the version in `pyproject.toml`
4. Add release notes describing changes
5. Publish release

### 3. Automatic Process
Once the release is published, the workflow automatically:

- ✅ Validates tag matches `pyproject.toml` version
- ✅ Builds Docker image for multiple architectures  
- ✅ Pushes three image tags:
  - `igormcsouza/gpt4shell:0.2.0` (semantic version)
  - `igormcsouza/gpt4shell:sha-abc1234` (commit SHA)
  - `igormcsouza/gpt4shell:latest` (convenience)
- ✅ Creates GitHub deployment entry
- ✅ Updates repository deployment status

## Manual Testing

You can also trigger the workflow manually:
1. Go to Actions → "Build and Publish Docker Image on Release"
2. Click "Run workflow"
3. Enter the release tag to build

## Version Validation

The workflow **will fail** if:
- Git tag doesn't match `pyproject.toml` version
- Missing Docker Hub credentials
- Build errors occur

Example validation:
```
Git tag: v0.2.0 → 0.2.0
pyproject.toml: 0.2.0
✅ Version validation passed
```

## Docker Usage

After release, users can pull:

```bash
# Specific version (recommended for production)
docker pull igormcsouza/gpt4shell:0.2.0

# Latest release
docker pull igormcsouza/gpt4shell:latest

# Specific commit (for debugging)
docker pull igormcsouza/gpt4shell:sha-abc1234
```

## Benefits

- 🔒 **Immutable releases** - no overwriting existing tags
- 🔍 **Full traceability** - commit SHA tags for debugging  
- ✅ **Version validation** - prevents version mismatches
- 🚀 **Multi-architecture** - supports both x86 and ARM
- 📊 **Deployment tracking** - visible in GitHub repository
- 🎯 **Intentional releases** - only on explicit releases, not pushes