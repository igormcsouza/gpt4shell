# Release Process Guide

## Overview

This repository uses a **release-driven workflow** for Docker image versioning, relying entirely on GitHub release tags for version management. The process is simplified to eliminate manual version synchronization and reduce complexity.

## How to Create a Release

### 1. Create GitHub Release
1. Go to GitHub repository → Releases → "Create a new release"
2. Use tag format: `v{version}` (e.g., `v0.2.0`)
3. Add release notes describing changes
4. Publish release

### 2. Automatic Process
Once the release is published, the workflow automatically:

- ✅ Extracts version from release tag (removes `v` prefix)
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

The workflow uses **git tags exclusively** for versioning:
- Release tag `v0.2.0` → Docker images tagged as `0.2.0`
- Release tag `v1.5.2` → Docker images tagged as `1.5.2`
- `pyproject.toml` contains a placeholder version (`0.0.0`) and is not used for release versioning

Example process:
```
1. Create release with tag v0.2.0
2. Workflow extracts "0.2.0" from tag
3. Builds and pushes Docker images with version tags
✅ Release complete - no version synchronization needed
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
- ⚡ **Simplified versioning** - git tags are the single source of truth
- 🚀 **Multi-architecture** - supports both x86 and ARM
- 📊 **Deployment tracking** - visible in GitHub repository
- 🎯 **Intentional releases** - only on explicit releases, not pushes
- 🔄 **No version synchronization** - eliminates pyproject.toml version management complexity