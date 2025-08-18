# Semantic Release Guide

This project uses [Python Semantic Release](https://python-semantic-release.readthedocs.io/) to automate version management and releases. This eliminates the need for manual version bumping and resolves branch protection issues.

## How It Works

Semantic Release automatically:
- Analyzes commit messages to determine the next version number
- Updates the version in `pyproject.toml`
- Creates git tags and GitHub releases
- Generates a changelog
- Triggers Docker image builds only when a new version is released

## Commit Message Convention

Use the [Conventional Commits](https://www.conventionalcommits.org/) format:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Types and Version Impact

| Type | Description | Version Bump | Example |
|------|-------------|--------------|---------|
| `feat` | New feature | **Minor** (0.1.0 → 0.2.0) | `feat: add new command option` |
| `fix` | Bug fix | **Patch** (0.1.0 → 0.1.1) | `fix: resolve CLI argument parsing` |
| `perf` | Performance improvement | **Patch** (0.1.0 → 0.1.1) | `perf: optimize response rendering` |
| `docs` | Documentation changes | No release | `docs: update README examples` |
| `style` | Code style changes | No release | `style: fix formatting` |
| `refactor` | Code refactoring | No release | `refactor: simplify error handling` |
| `test` | Adding/updating tests | No release | `test: add unit tests for CLI` |
| `build` | Build system changes | No release | `build: update dependencies` |
| `ci` | CI/CD changes | No release | `ci: fix workflow permissions` |
| `chore` | Maintenance tasks | No release | `chore: update .gitignore` |

### Breaking Changes

For **major** version bumps (0.1.0 → 1.0.0), add `BREAKING CHANGE:` in the footer:

```
feat: redesign CLI interface

BREAKING CHANGE: Command arguments have been restructured. 
See migration guide for details.
```

Or use an exclamation mark:

```
feat!: redesign CLI interface
```

## Examples

### New Feature (Minor Release)
```bash
git commit -m "feat: add support for custom system prompts"
```
Result: 0.1.0 → 0.2.0

### Bug Fix (Patch Release)
```bash
git commit -m "fix: handle empty API responses gracefully"
```
Result: 0.1.0 → 0.1.1

### Breaking Change (Major Release)
```bash
git commit -m "feat!: require Python 3.12+ for new async features"
```
Result: 0.1.0 → 1.0.0

### No Release
```bash
git commit -m "docs: update installation instructions"
git commit -m "ci: improve workflow caching"
git commit -m "style: format code with black"
```
Result: No version change

## Release Process

1. **Make commits** following the convention above
2. **Push to main** - Semantic Release runs automatically
3. **New releases** are created when there are `feat` or `fix` commits
4. **Docker images** are built only for new releases
5. **Changelog** is automatically updated

## Manual Release

To trigger a release manually:

```bash
# Go to GitHub Actions
# Run "Semantic Release and Docker Build" workflow
# Select "Run workflow" → "main"
```

## Migration from Manual Versioning

- ✅ **No more manual version updates** in `pyproject.toml`
- ✅ **No more manual git tags** - created automatically  
- ✅ **No more branch protection conflicts** - no PRs needed for version updates
- ✅ **Automatic changelog** generation
- ✅ **Consistent release process**

## Benefits

1. **Solves Branch Protection Issues**: No need to create PRs for version updates
2. **Consistent Versioning**: Based on semantic meaning of changes
3. **Automated Process**: No manual intervention required
4. **Clear History**: Conventional commits make project history readable
5. **Automatic Changelogs**: Generated from commit messages
6. **Zero Configuration**: Works out of the box with current setup

## Troubleshooting

### No Release Created
- Check commit messages follow the convention
- Ensure you have `feat:` or `fix:` commits since last release
- Documentation/style changes don't trigger releases

### Version Not Updated
- Semantic Release handles version automatically
- Don't manually edit version in `pyproject.toml`
- Version is updated during the release process

### Docker Build Skipped
- Docker images are only built for new releases
- Push commits with `feat:` or `fix:` to trigger a release