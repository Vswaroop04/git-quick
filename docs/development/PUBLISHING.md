# Publishing Guide

How to publish Git Quick to PyPI, npm, and Homebrew.

## Before Publishing

### 1. Update Version Numbers

Update version in these files:

- `pyproject.toml` → `version = "0.1.0"`
- `package.json` → `"version": "0.1.0"`
- `git_quick/__init__.py` → `__version__ = "0.1.0"`
- `Formula/git-quick.rb` → `url` line with version

### 2. Update CHANGELOG.md

```markdown
## [0.1.0] - 2025-01-XX

### Added

- Initial release
- git-quick command
- git-story command
- git-time command
- git-sync-all command
- AI integration (Ollama, OpenAI, Anthropic)
- VS Code extension
```

### 3. Run Tests

```bash
make test
make lint
```

### 4. Build Documentation

```bash
# Ensure all docs are up to date
cat README.md
cat QUICKSTART.md
cat docs/INSTALLATION.md
```

## Publishing to PyPI

### 1. Setup PyPI Account

```bash
# Create account at https://pypi.org/account/register/

# Install tools
pip install build twine
```

### 2. Build Package

```bash
# Clean old builds
rm -rf dist/ build/ *.egg-info

# Build
python -m build

# Should create:
# dist/git_quick-0.1.0-py3-none-any.whl
# dist/git-quick-0.1.0.tar.gz
```

### 3. Test on TestPyPI (Recommended)

```bash
# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*

# Test installation
pip install --index-url https://test.pypi.org/simple/ git-quick

# Test it works
git-quick --version
```

### 4. Upload to PyPI

```bash
# Upload to production PyPI
python -m twine upload dist/*

# Verify at https://pypi.org/project/git-quick/
```

### 5. Test Installation

```bash
# Create clean environment
python -m venv test_env
source test_env/bin/activate

# Install from PyPI
pip install git-quick

# Test
git-quick --version
git-quick --help
```

## Publishing to npm

### 1. Setup npm Account

```bash
# Create account at https://www.npmjs.com/signup

# Login
npm login
```

### 2. Update Package Info

Edit `package.json`:

```json
{
  "name": "git-quick-cli",
  "version": "0.1.0",
  "repository": {
    "url": "https://github.com/vswaroop04/git-quick.git"
  }
}
```

### 3. Test Package Locally

```bash
# Create tarball
npm pack

# Should create: git-quick-cli-0.1.0.tgz

# Test installation
npm install -g ./git-quick-cli-0.1.0.tgz

# Test it works
git-quick --version
```

### 4. Publish to npm

```bash
# Publish
npm publish

# Verify at https://www.npmjs.com/package/git-quick-cli
```

### 5. Test Installation

```bash
# Uninstall test version
npm uninstall -g git-quick-cli

# Install from npm
npm install -g git-quick-cli

# Test
git-quick --version
```

## Publishing to Homebrew

### Option A: Create Your Own Tap (Easier)

### 1. Create Tap Repository

```bash
# Create new repo: homebrew-git-quick
# GitHub naming: homebrew-<name>

git clone https://github.com/yourusername/homebrew-git-quick.git
cd homebrew-git-quick
```

### 2. Create Formula

```bash
# Copy formula
cp Formula/git-quick.rb .

# Or create Formula directory
mkdir Formula
cp git-quick.rb Formula/
```

### 3. Generate SHA256

```bash
# Create release tarball
git tag v0.1.0
git push origin v0.1.0

# GitHub will create:
# https://github.com/vswaroop04/git-quick/archive/refs/tags/v0.1.0.tar.gz

# Download and get SHA256
curl -L https://github.com/vswaroop04/git-quick/archive/refs/tags/v0.1.0.tar.gz -o git-quick-0.1.0.tar.gz
shasum -a 256 git-quick-0.1.0.tar.gz

# Update Formula/git-quick.rb with SHA256
```

### 4. Update Formula

Edit `Formula/git-quick.rb`:

```ruby
class GitQuick < Formula
  desc "Lightning-fast Git workflows with AI-powered commit messages"
  homepage "https://github.com/vswaroop04/git-quick"
  url "https://github.com/vswaroop04/git-quick/archive/refs/tags/v0.1.0.tar.gz"
  sha256 "YOUR_ACTUAL_SHA256_HERE"
  license "MIT"
end
```

### 5. Test Formula

```bash
# Install from your tap
brew tap yourusername/git-quick
brew install git-quick

# Test
git-quick --version

# Audit formula
brew audit --strict Formula/git-quick.rb

# Test installation
brew test git-quick
```

### 6. Push Tap

```bash
git add Formula/git-quick.rb
git commit -m "Add git-quick formula v0.1.0"
git push origin main
```

### 7. Users Install With

```bash
brew tap yourusername/git-quick
brew install git-quick
```

### Option B: Submit to homebrew-core (Harder, More Exposure)

Requirements:

- 75+ GitHub stars
- 30+ forks
- Notable user base
- Stable for 3+ months

Process:

1. Create PR to https://github.com/Homebrew/homebrew-core
2. Follow guidelines: https://docs.brew.sh/Formula-Cookbook
3. Wait for maintainer review

## Publishing VS Code Extension

### 1. Setup Publisher Account

```bash
# Create account at https://marketplace.visualstudio.com/

# Install vsce
npm install -g @vscode/vsce

# Create publisher
vsce create-publisher your-publisher-name
```

### 2. Update Extension Manifest

Edit `vscode-extension/package.json`:

```json
{
  "publisher": "your-publisher-name",
  "repository": {
    "url": "https://github.com/vswaroop04/git-quick"
  }
}
```

### 3. Build Extension

```bash
cd vscode-extension

# Install dependencies
npm install

# Compile
npm run compile

# Package
vsce package

# Creates: git-quick-vscode-0.1.0.vsix
```

### 4. Test Extension

```bash
# Install locally
code --install-extension git-quick-vscode-0.1.0.vsix

# Test in VS Code
# - Restart VS Code
# - Try commands (Ctrl+Shift+P → "Git Quick")
```

### 5. Publish Extension

```bash
# Login
vsce login your-publisher-name

# Publish
vsce publish

# Or publish with version bump
vsce publish patch  # 0.1.0 -> 0.1.1
vsce publish minor  # 0.1.0 -> 0.2.0
vsce publish major  # 0.1.0 -> 1.0.0
```

### 6. Verify

Visit: https://marketplace.visualstudio.com/items?itemName=your-publisher-name.git-quick-vscode

## Post-Publishing

### 1. Create GitHub Release

```bash
# Tag version
git tag v0.1.0
git push origin v0.1.0

# Create release on GitHub
# https://github.com/vswaroop04/git-quick/releases/new

# Include:
- Release notes
- Installation instructions
- Links to PyPI, npm, Homebrew
```

### 2. Update Documentation

Update README.md with installation badges:

```markdown
[![PyPI](https://img.shields.io/pypi/v/git-quick)](https://pypi.org/project/git-quick/)
[![npm](https://img.shields.io/npm/v/git-quick-cli)](https://www.npmjs.com/package/git-quick-cli)
[![Homebrew](https://img.shields.io/badge/homebrew-git--quick-orange)](https://github.com/yourusername/homebrew-git-quick)
[![VS Code](https://img.shields.io/visual-studio-marketplace/v/your-publisher-name.git-quick-vscode)](https://marketplace.visualstudio.com/items?itemName=your-publisher-name.git-quick-vscode)
```

### 3. Social Media Announcement

Post on:

- Twitter/X
- Reddit (r/programming, r/git)
- Hacker News
- Dev.to
- LinkedIn

Example post:

```
🚀 Launching Git Quick v0.1.0!

Lightning-fast Git workflows with AI-powered commit messages.

✨ Features:
- One-command git add + commit + push
- AI-generated conventional commits
- Time tracking per branch
- Beautiful commit history

Install:
📦 pip install git-quick
📦 npm install -g git-quick-cli
🍺 brew install git-quick

https://github.com/vswaroop04/git-quick
```

### 4. Submit to Lists

- https://github.com/topics/git-tools
- https://github.com/alebcay/awesome-shell
- https://github.com/rothgar/awesome-tuis
- https://github.com/k4m4/terminals-are-sexy

## Updating Versions

### For Patch Release (0.1.0 → 0.1.1)

```bash
# Update version in all files
# pyproject.toml, package.json, __init__.py

# Build and publish
python -m build
python -m twine upload dist/*

npm version patch
npm publish

# Update Homebrew formula
# Update version and SHA256 in Formula/git-quick.rb

# Tag and release
git tag v0.1.1
git push origin v0.1.1
```

### For Minor Release (0.1.0 → 0.2.0)

Same as patch, but:

```bash
npm version minor
```

### For Major Release (0.1.0 → 1.0.0)

Same as patch, but:

```bash
npm version major
```

## Makefile Shortcuts

Add to `Makefile`:

```makefile
publish-test:
	python -m build
	python -m twine upload --repository testpypi dist/*

publish-pypi:
	python -m build
	python -m twine upload dist/*

publish-npm:
	npm publish

publish-all: publish-pypi publish-npm
	@echo "Published to PyPI and npm!"

release:
	@echo "Creating release..."
	@read -p "Version (e.g., 0.1.0): " version; \
	git tag v$$version; \
	git push origin v$$version; \
	echo "Release v$$version created!"
```

Usage:

```bash
make publish-test   # Test on TestPyPI
make publish-pypi   # Publish to PyPI
make publish-npm    # Publish to npm
make publish-all    # Publish to both
make release        # Create git tag
```

## Troubleshooting

### PyPI upload fails

```bash
# Check credentials
cat ~/.pypirc

# Re-login
python -m twine upload dist/* --verbose
```

### npm publish fails

```bash
# Check login
npm whoami

# Re-login
npm login

# Check package name available
npm search git-quick-cli
```

### Homebrew formula fails

```bash
# Test locally
brew install --build-from-source Formula/git-quick.rb

# Check for issues
brew audit --strict Formula/git-quick.rb

# Test installation
brew test git-quick
```

## Checklist

Before publishing:

- [ ] Version updated in all files
- [ ] CHANGELOG.md updated
- [ ] Tests passing
- [ ] Documentation updated
- [ ] README has correct installation instructions
- [ ] All commands tested
- [ ] Git tagged
- [ ] GitHub release created

After publishing:

- [ ] PyPI package works
- [ ] npm package works
- [ ] Homebrew formula works
- [ ] VS Code extension works
- [ ] Documentation links correct
- [ ] Social media posted
- [ ] Submitted to awesome lists

## Resources

- PyPI: https://pypi.org/
- npm: https://www.npmjs.com/
- Homebrew: https://docs.brew.sh/
- VS Code: https://code.visualstudio.com/api/working-with-extensions/publishing-extension
- Packaging Guide: https://packaging.python.org/
