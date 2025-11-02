# Git Quick - Lightning-fast Git workflows

A modern CLI tool and VS Code extension that speeds up repetitive Git commands with smart defaults, AI-powered commit messages, and developer productivity features.

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

```bash
pip install git-quick
```

Or from source:
```bash
git clone https://github.com/yourusername/git-quick.git
cd git-quick
pip install -e .
```

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
