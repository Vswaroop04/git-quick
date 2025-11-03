# Publishing Setup Guide

This guide explains how to set up automatic publishing to npm and PyPI when you push to the main branch.

## Overview

The GitHub Actions workflow (`.github/workflows/publish.yml`) automatically:

1. ✅ Detects version bump type from commit messages
2. ✅ Bumps version in `pyproject.toml`, `package.json`, and `cli.py`
3. ✅ Creates a git tag
4. ✅ Publishes to PyPI
5. ✅ Publishes to npm
6. ✅ Creates a GitHub release

## Version Bumping Logic

The workflow analyzes your commit messages to determine the version bump:

| Commit Type                     | Version Bump              | Example              |
| ------------------------------- | ------------------------- | -------------------- |
| `BREAKING CHANGE:` or `feat!:`  | **Major** (1.1.0 → 2.0.0) | Breaking API changes |
| `feat:` or `feat(scope):`       | **Minor** (1.1.0 → 1.1.0) | New features         |
| `fix:`, `chore:`, `docs:`, etc. | **Patch** (1.1.0 → 1.0.1) | Bug fixes, updates   |

### Examples

```bash
# Patch bump (0.1.0 → 0.1.1)
git commit -m "fix: resolve null pointer in config"

# Minor bump (0.1.0 → 0.2.0)
git commit -m "feat: add setup wizard"

# Major bump (0.1.0 → 1.1.0)
git commit -m "feat!: redesign CLI interface"
# or
git commit -m "feat: redesign CLI interface

BREAKING CHANGE: CLI flags have changed"
```

## Prerequisites

### 1. PyPI Account Setup

1. **Create PyPI account**: https://pypi.org/account/register/
2. **Enable 2FA**: https://pypi.org/manage/account/
3. **Generate API token**:

   - Go to: https://pypi.org/manage/account/token/
   - Token name: `github-actions-git-quick`
   - Scope: "Entire account" (or project-specific after first release)
   - Copy the token (starts with `pypi-`)

4. **Add token to GitHub Secrets**:
   - Go to: `https://github.com/YOUR_USERNAME/git-quick/settings/secrets/actions`
   - Click "New repository secret"
   - Name: `PYPI_API_TOKEN`
   - Value: Paste your PyPI token

### 2. npm Account Setup

1. **Create npm account**: https://www.npmjs.com/signup
2. **Enable 2FA** (Auth-only recommended): https://www.npmjs.com/settings/YOUR_USERNAME/tfa
3. **Generate access token**:

   - Go to: https://www.npmjs.com/settings/YOUR_USERNAME/tokens
   - Click "Generate New Token"
   - Type: "Automation" (for CI/CD)
   - Copy the token

4. **Add token to GitHub Secrets**:
   - Go to: `https://github.com/YOUR_USERNAME/git-quick/settings/secrets/actions`
   - Click "New repository secret"
   - Name: `NPM_TOKEN`
   - Value: Paste your npm token

### 3. GitHub Repository Setup

The workflow needs write permissions:

1. Go to: `https://github.com/YOUR_USERNAME/git-quick/settings/actions`
2. Under "Workflow permissions", select:
   - ✅ "Read and write permissions"
3. Save

## First Release (Manual)

Before the automated workflow can work, you need to publish the first version manually:

### PyPI First Release

```bash
# 1. Build the package
python -m build

# 2. Upload to PyPI
python -m twine upload dist/*
# Enter your PyPI username and password when prompted
```

### npm First Release

```bash
# 1. Login to npm
npm login

# 2. Publish
npm publish
```

## Testing the Workflow

### Option 1: Test with a dry-run

```bash
# Make a test commit
echo "test" >> README.md
git add README.md
git commit -m "docs: test auto-publish"
git push origin main

# Watch the workflow
# Go to: https://github.com/YOUR_USERNAME/git-quick/actions
```

### Option 2: Test on a branch first

Create a test branch and workflow:

```bash
# Create test branch
git checkout -b test-publish

# Modify workflow to run on test-publish branch
# Edit .github/workflows/publish.yml:
# branches:
#   - test-publish

git add .github/workflows/publish.yml
git commit -m "test: workflow on test branch"
git push origin test-publish
```

## Workflow Diagram

```
Push to main
    ↓
Analyze commits (feat/fix/BREAKING)
    ↓
Determine bump (major/minor/patch)
    ↓
Update versions:
  - pyproject.toml
  - package.json
  - cli.py
    ↓
Commit & tag (v1.2.3)
    ↓
Build packages
    ↓
Publish to PyPI ──────→ pip install git-quick==1.2.3
    ↓
Publish to npm ───────→ npm install -g git-quick-cli@1.2.3
    ↓
Create GitHub Release → https://github.com/.../releases/v1.2.3
```

## Skipping CI

If you want to push without triggering a release:

```bash
git commit -m "docs: update README [skip ci]"
```

The `[skip ci]` flag tells GitHub Actions to skip the workflow.

## Troubleshooting

### PyPI publish fails with "File already exists"

**Problem**: Version already exists on PyPI.

**Solution**:

1. Delete the git tag: `git tag -d v1.2.3 && git push origin :refs/tags/v1.2.3`
2. Manually bump version in `pyproject.toml` and `package.json`
3. Commit and push again

### npm publish fails with "403 Forbidden"

**Problem**: npm token is invalid or has wrong permissions.

**Solution**:

1. Generate a new "Automation" token on npmjs.com
2. Update the `NPM_TOKEN` secret in GitHub
3. Re-run the workflow

### Workflow doesn't trigger

**Problem**: Push didn't trigger the workflow.

**Solution**:

1. Check that you pushed to `main` branch
2. Check that you didn't push only ignored files (README.md, docs/\*)
3. Check workflow permissions in repository settings

### Version bump is wrong

**Problem**: Workflow bumped minor instead of patch (or vice versa).

**Solution**: Use correct conventional commit format:

- `feat:` for minor bumps
- `fix:`, `chore:`, `docs:` for patch bumps
- `feat!:` or `BREAKING CHANGE:` for major bumps

## Manual Version Override

If you need to set a specific version:

```bash
# Edit pyproject.toml
version = "2.0.0"

# Edit package.json
"version": "2.0.0"

# Edit git_quick/cli.py
@click.version_option(version="2.0.0", ...)

# Commit
git add pyproject.toml package.json git_quick/cli.py
git commit -m "chore: bump version to 2.0.0 [skip ci]"
git tag -a "v2.0.0" -m "Release v2.0.0"
git push origin main --tags
```

Then manually publish:

```bash
python -m build
python -m twine upload dist/*
npm publish
```

## Release Checklist

Before pushing to main:

- [ ] All tests pass locally
- [ ] README is up to date
- [ ] CHANGELOG is updated (optional)
- [ ] Commit messages follow conventional commit format
- [ ] Version bump type is correct for your changes

## Security Notes

1. **Never commit tokens** to the repository
2. **Use GitHub Secrets** for all sensitive data
3. **Enable 2FA** on PyPI and npm accounts
4. **Use Automation tokens** for npm (not Classic tokens)
5. **Rotate tokens** periodically (every 6-12 months)

## Advanced: Pre-release Versions

To publish a pre-release (beta, alpha, rc):

```bash
# Set version manually
echo "version = \"1.1.0-beta.1\"" # in pyproject.toml
echo "\"version\": \"1.1.0-beta.1\"" # in package.json

# Commit with [skip ci] to avoid auto-publish
git commit -m "chore: pre-release v1.1.0-beta.1 [skip ci]"
git tag -a "v1.1.0-beta.1" -m "Pre-release v1.1.0-beta.1"
git push origin main --tags

# Manually publish
python -m build
python -m twine upload dist/*
npm publish --tag beta
```

Users can then install:

```bash
pip install git-quick==1.1.0b1
npm install -g git-quick-cli@beta
```

## Support

If you encounter issues:

1. Check the workflow logs: `https://github.com/YOUR_USERNAME/git-quick/actions`
2. Verify secrets are set correctly
3. Test publishing manually first
4. Check PyPI and npm package pages

---

**Happy Publishing! 🚀**
