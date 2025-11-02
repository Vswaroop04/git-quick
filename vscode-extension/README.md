# Git Quick VS Code Extension

Supercharge your Git workflow with AI-powered commit messages and productivity commands.

## Features

### Commands

- **Git Quick: Quick Commit & Push** (`Ctrl+Shift+G Q`)
  - Stage all changes, generate AI commit message, commit, and push
  - Interactive confirmation before committing

- **Git Quick: Generate AI Commit Message** (`Ctrl+Shift+G M`)
  - Generate commit message for staged changes
  - Inserts message into SCM input box

- **Git Quick: Show Commit Story**
  - View colorized commit history since last release
  - Group by date, author, or type

- **Git Quick: Show Time Report**
  - Track time spent on branches
  - Detailed session breakdown

- **Git Quick: Sync All Branches**
  - Update all local branches from remote
  - Safe fast-forward with stashing

### Status Bar

Quick access button in status bar for common Git Quick operations.

### SCM Integration

Buttons in Source Control view for quick access to:
- Quick commit & push
- Generate AI commit message

## Requirements

- Git Quick CLI installed (`pip install git-quick`)
- Python 3.8+
- Git repository

## Extension Settings

- `gitQuick.autoPush`: Automatically push after committing (default: true)
- `gitQuick.emojiStyle`: Commit message emoji style (default: gitmoji)
- `gitQuick.aiProvider`: AI provider (ollama/openai/anthropic)
- `gitQuick.aiModel`: AI model to use (default: llama3.2)
- `gitQuick.cliPath`: Path to git-quick CLI (default: git-quick)
- `gitQuick.conventionalCommits`: Use conventional commit format (default: true)

## Keyboard Shortcuts

- `Ctrl+Shift+G Q` (Mac: `Cmd+Shift+G Q`): Quick commit & push
- `Ctrl+Shift+G M` (Mac: `Cmd+Shift+G M`): Generate AI commit message

## Installation

1. Install Git Quick CLI:
   ```bash
   pip install git-quick
   ```

2. Install this extension from VS Code marketplace

3. Configure AI provider in settings (optional)

## Usage

1. Make changes to your code
2. Press `Ctrl+Shift+G Q` to quick commit and push
3. Or use Command Palette (`Ctrl+Shift+P`) and search for "Git Quick"

## License

MIT
