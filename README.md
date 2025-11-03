# Git Quick - Lightning-fast Git workflows

[![PyPI](https://img.shields.io/badge/pypi-v0.1.0-blue)](https://pypi.org/project/git-quick/)
[![npm](https://img.shields.io/badge/npm-v0.1.0-red)](https://www.npmjs.com/package/git-quick-cli)
[![Homebrew](https://img.shields.io/badge/homebrew-available-orange)](https://github.com/yourusername/homebrew-git-quick)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue)](https://www.python.org/)

A modern CLI tool and VS Code extension that speeds up repetitive Git commands with smart defaults, AI-powered commit messages, and developer productivity features.

## ⚡ Quick Install

```bash
# Homebrew (macOS/Linux)
brew tap yourusername/git-quick
brew install git-quick

# npm (All platforms)
npm install -g git-quick-cli

# pip (Python)
pip install git-quick
```

[See all installation options →](docs/INSTALLATION.md)

## Features

### Core Commands

- **`git-quick`** - Combines `git add`, `commit`, and `push` with smart defaults
  - Auto-detects branch
  - AI-generated commit messages from diffs
  - Emoji/scope support (gitmoji-style)
  - Interactive mode for fine-tuning

- **`git-story`** - Compact, colorized commit summary
  - Shows commits since last release/tag
  - Grouped by author, date, or type
  - Export to markdown for changelogs

- **`git-time`** - Track development time per branch/feature
  - Automatic time tracking per branch
  - Reports with breakdowns
  - Integration with time-tracking tools

- **`git-sync-all`** - Update all local branches safely
  - Stash uncommitted changes
  - Fast-forward all branches
  - Conflict detection and reporting

### VS Code Extension

- Format commit messages with templates
- AI commit message suggestions in editor
- One-click git-quick from command palette
- Status bar integration

## Installation

### Homebrew (macOS/Linux)
```bash
brew tap yourusername/git-quick
brew install git-quick
```

### npm (Cross-platform)
```bash
npm install -g git-quick-cli
```

### pip (Python)
```bash
pip install git-quick
```

### From Source
```bash
git clone https://github.com/yourusername/git-quick.git
cd git-quick
pip install -e .
```

**See [Installation Guide](docs/INSTALLATION.md) for detailed instructions, including Windows setup.**

## Quick Start

```bash
# Quick commit and push with AI message
git-quick

# See your commit story
git-story

# Track your time
git-time report

# Sync all branches
git-sync-all
```

## Configuration

Create `~/.gitquick.toml`:

```toml
[quick]
auto_push = true
emoji_style = "gitmoji"
ai_provider = "ollama"  # or "openai", "anthropic"

[story]
default_range = "last-release"
color_scheme = "dark"

[time]
auto_track = true
idle_threshold = 300  # seconds
```

## Roadmap

- [ ] Core CLI commands
- [ ] AI commit message generation
- [ ] VS Code extension
- [ ] Git hooks integration
- [ ] Team collaboration features
- [ ] Plugin system

## License

MIT
