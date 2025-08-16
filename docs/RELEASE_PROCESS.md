# Release Process Guide

## Overview

This repository uses a **release-driven workflow** for Docker image versioning, ensuring immutable releases and proper version tracking. The release process automatically manages version updates to eliminate manual steps and potential errors.

## How to Create a Release

### 1. Create GitHub Release
1. Go to GitHub repository → Releases → "Create a new release"
2. Use tag format: `v{version}` (e.g., `v0.2.0`)
3. The version will be automatically set in `pyproject.toml` to match your tag
4. Add release notes describing changes
5. Publish release

### 2. Automatic Process
Once the release is published, the workflow automatically:

- ✅ Extracts version from release tag (removes `v` prefix)
- ✅ Updates `pyproject.toml` with the extracted version
- ✅ Commits version change back to repository
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

## Version Management

The workflow **automatically manages versions**:
- Release tag `v0.2.0` → sets `pyproject.toml` version to `0.2.0`
- Release tag `v1.5.2` → sets `pyproject.toml` version to `1.5.2`
- Version changes are committed back to the repository

Example process:
```
1. Create release with tag v0.2.0
2. Workflow extracts "0.2.0" from tag
3. Updates pyproject.toml: version = "0.2.0"
4. Commits: "Bump version to 0.2.0 for release v0.2.0"
5. Builds and pushes Docker images
✅ Version management complete
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
- ⚡ **Automated versioning** - no manual version updates required
- 🚀 **Multi-architecture** - supports both x86 and ARM
- 📊 **Deployment tracking** - visible in GitHub repository
- 🎯 **Intentional releases** - only on explicit releases, not pushes
- 🔄 **Version synchronization** - git tag and pyproject.toml always match