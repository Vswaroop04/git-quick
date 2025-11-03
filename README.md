# Git Quick - Lightning-fast Git workflows

[![PyPI](https://img.shields.io/badge/pypi-v1.1.1-blue)](https://pypi.org/project/git-quick/)
[![npm](https://img.shields.io/badge/npm-v1.1.1-red)](https://www.npmjs.com/package/git-quick-cli)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue)](https://www.python.org/)

A modern CLI tool and VS Code extension that speeds up repetitive Git commands with smart defaults, AI-powered commit messages, and developer productivity features.

## ⚡ Quick Install

```bash
# npm (All platforms)
npm install -g git-quick-cli

# pip (Python)
pip install git-quick
```

**First Run:** `gq` will automatically guide you through AI setup on first use!

[See all installation options →](docs/INSTALLATION.md)

## Features

### Core Commands

- **`gq`** - Combines `git add`, `commit`, and `push` with smart defaults

  - Auto-detects branch
  - AI-generated commit messages from diffs
  - Emoji/scope support (gitmoji-style)
  - Interactive mode for fine-tuning

- **`gq story`** - Compact, colorized commit summary

  - Shows commits since last release/tag
  - Grouped by author, date, or type
  - Export to markdown for changelogs

- **`gq time start`** - Track development time per branch/feature

  - Automatic time tracking per branch
  - Reports with breakdowns
  - Integration with time-tracking tools

- **`gq sync`** - Update all local branches safely

  - Stash uncommitted changes
  - Fast-forward all branches
  - Conflict detection and reporting

- **`gq --setup`** - Run setup wizard
  - Configure/Change AI providers
  - Configure other settings

### VS Code Extension (In Progress)

- Format commit messages with templates
- AI commit message suggestions in editor
- One-click git-quick from command palette
- Status bar integration

## Installation

### Quick Install (Works immediately with smart fallback)

```bash
# npm (All platforms)
npm install -g git-quick-cli

# pip (Python)
pip install git-quick
```

**Note:** `gq` works immediately after installation! It uses intelligent commit message generation based on your changes. For AI-powered messages, optionally install Ollama (see below).

### Optional: AI-Powered Messages (Ollama)

For enhanced AI commit messages, install Ollama (free, runs locally):

```bash
# macOS/Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Or visit: https://ollama.ai/download

# Pull a model
ollama pull llama3
```

### From Source

```bash
git clone https://github.com/vswaroop04/git-quick.git
cd git-quick
pip install -e .
```

**See [Installation Guide](docs/INSTALLATION.md) for detailed instructions.**

## 📚 Documentation

- **[Quick Start](QUICKSTART.md)** - Get started in 5 minutes
- **[Installation](docs/INSTALLATION.md)** - Platform-specific installation
- **[AI Setup](docs/setup/AI_SETUP.md)** - Configure AI providers
- **[Configuration](docs/setup/CONFIGURATION_GUIDE.md)** - All configuration options
- **[Usage Guide](docs/USAGE.md)** - Complete command reference
- **[Contributing](CONTRIBUTING.md)** - How to contribute

**[📖 View All Documentation →](docs/README.md)**

## Quick Start

```bash
# First time: Run setup wizard
gq --setup

# Or just run gq and it will prompt you automatically
gq

# Other commands
gq story              # See your commit story
gq time report        # Track your time
gq sync               # Sync all branches
```

### First-Time Setup

On your first run, `gq` will ask you to choose an AI provider:

1. **Ollama** (Recommended) - Free, local, private AI

   - Automatically installs and downloads model
   - No API keys needed

2. **OpenAI** - Best quality, requires API key

   - Enter your API key when prompted

3. **Anthropic (Claude)** - Great for technical commits

   - Enter your API key when prompted

4. **No AI** - Smart fallback mode
   - Works immediately, no setup needed

You can always reconfigure later with `gq --setup`

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

## License

MIT
