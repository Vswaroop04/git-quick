# Unified CLI Summary

## Question: Is it the same for npm and Python packages?

**YES!** 🎉 All three installation methods (pip, npm, Homebrew) now use the **exact same unified command structure**.

## How It Works

### Single Python Core

All three packages use the same Python CLI implementation:

```
pip install git-quick          ┐
npm install -g git-quick-cli   ├──→  Python Core (git_quick/cli.py)
brew install git-quick         ┘
```

### One Command Everywhere

**No matter how you install**, you get the same commands:

```bash
git-quick                # Quick commit & push (default)
git-quick story          # Show commit history
git-quick time start     # Time tracking
git-quick time stop
git-quick time report
git-quick sync           # Sync all branches
```

## Installation Comparison

| Package      | Installs                | What It Does     | Commands                |
| ------------ | ----------------------- | ---------------- | ----------------------- |
| **pip**      | Python package directly | Runs Python CLI  | git-quick + subcommands |
| **npm**      | Node.js wrapper         | Calls Python CLI | git-quick + subcommands |
| **Homebrew** | Python in virtualenv    | Runs Python CLI  | git-quick + subcommands |

## Technical Details

### pip Package

**Entry point:** `pyproject.toml`

```toml
[project.scripts]
git-quick = "git_quick.cli:cli"
```

**Flow:**

```
User runs: git-quick story
    ↓
Python entry point: git_quick.cli:cli
    ↓
Click group processes: ["story"]
    ↓
Executes: story command
```

### npm Package

**Entry point:** `package.json`

```json
{
  "bin": {
    "git-quick": "./bin/git-quick.js"
  }
}
```

**Flow:**

```
User runs: git-quick story
    ↓
Node wrapper: bin/git-quick.js
    ↓
Checks Python installed
    ↓
Installs Python package if needed
    ↓
Runs: python -m git_quick.cli story
    ↓
Python entry point: git_quick.cli:cli
    ↓
Click group processes: ["story"]
    ↓
Executes: story command
```

### Homebrew Package

**Entry point:** `Formula/git-quick.rb`

```ruby
class GitQuick < Formula
  include Language::Python::Virtualenv
  # Installs Python package in isolated virtualenv
end
```

**Flow:**

```
User runs: git-quick story
    ↓
Virtualenv Python: /usr/local/bin/git-quick
    ↓
Python entry point: git_quick.cli:cli
    ↓
Click group processes: ["story"]
    ↓
Executes: story command
```

## What Changed

### Before (Separate Commands)

**pip:**

```bash
git-quick     # Installed
git-story     # Installed
git-time      # Installed
git-sync-all  # Installed
```

**npm:**

```bash
git-quick     # Installed
git-story     # Installed
git-time      # Installed
git-sync-all  # Installed
```

**Homebrew:**

```bash
git-quick     # Installed
git-story     # Installed
git-time      # Installed
git-sync-all  # Installed
```

### After (Unified Command)

**ALL packages now install:**

```bash
git-quick     # Single command with subcommands
```

**Usage:**

```bash
git-quick              # Default action
git-quick story        # Subcommand
git-quick time start   # Nested subcommand
git-quick sync         # Subcommand
```

## User Experience

### Via pip

```bash
$ pip install git-quick
Successfully installed git-quick-1.0.0

$ which git-quick
/usr/local/bin/git-quick

$ git-quick --help
Usage: git-quick [OPTIONS] COMMAND [ARGS]...

Commands:
  commit  Quick commit and push
  story   Show commit history
  time    Time tracking commands
  sync    Sync all branches

$ git-quick story
📖 Commit Story
15 commits
```

### Via npm

```bash
$ npm install -g git-quick-cli
+ git-quick-cli@1.0.0

$ which git-quick
/usr/local/bin/git-quick

$ git-quick --help
Usage: git-quick [OPTIONS] COMMAND [ARGS]...

Commands:
  commit  Quick commit and push
  story   Show commit history
  time    Time tracking commands
  sync    Sync all branches

$ git-quick story
📖 Commit Story
15 commits
```

### Via Homebrew

```bash
$ brew install git-quick
🍺 Installing git-quick...

$ which git-quick
/usr/local/bin/git-quick

$ git-quick --help
Usage: git-quick [OPTIONS] COMMAND [ARGS]...

Commands:
  commit  Quick commit and push
  story   Show commit history
  time    Time tracking commands
  sync    Sync all branches

$ git-quick story
📖 Commit Story
15 commits
```

## Advantages

### 1. Consistent Experience

**Same commands** regardless of installation method:

- Developers can switch between Mac (Homebrew), Linux (pip), Windows (npm)
- Documentation works for everyone
- No confusion about which command to use

### 2. Single Source of Truth

- **One Python CLI implementation** in `git_quick/cli.py`
- Bug fixes propagate to all platforms instantly
- New features available everywhere at once

### 3. Cleaner Installation

**Before:**

```bash
$ npm install -g git-quick-cli
Installing 4 commands: git-quick, git-story, git-time, git-sync-all
```

**After:**

```bash
$ npm install -g git-quick-cli
Installing 1 command: git-quick
```

### 4. Better Discoverability

**Before:**

```bash
$ git-quick --help
# Only shows quick command help
# Users don't know about git-story, git-time, etc.
```

**After:**

```bash
$ git-quick --help
Commands:
  commit  Quick commit and push
  story   Show commit history
  time    Time tracking commands
  sync    Sync all branches
# Users see all features!
```

### 5. Industry Standard

Follows patterns used by popular tools:

- `git` (git commit, git push, git log)
- `docker` (docker run, docker ps, docker build)
- `kubectl` (kubectl get, kubectl apply, kubectl logs)
- `npm` (npm install, npm test, npm run)

## Backward Compatibility

Old commands still work (for Python package):

```bash
git-story      # Still works → redirects to git-quick story
git-time       # Still works → redirects to git-quick time
git-sync-all   # Still works → redirects to git-quick sync
```

But these are now deprecated. We recommend using the new unified structure.

## Migration Path

### For Users

**No action needed!** Old commands still work.

But we recommend updating:

```bash
# Old (still works)
git-story

# New (recommended)
git-quick story
```

### For Scripts

Update gradually:

```bash
# Old script (still works)
#!/bin/bash
git-quick
git-story
git-time report
git-sync-all

# New script (recommended)
#!/bin/bash
git-quick
git-quick story
git-quick time report
git-quick sync
```

## Summary

**Question:** Is the unified command the same for npm and Python packages?

**Answer:** YES! All three packages (pip, npm, Homebrew) use the **exact same** unified command structure:

```bash
git-quick               # Main command
git-quick story         # Subcommand
git-quick time start    # Nested subcommand
git-quick sync          # Subcommand
```

**How:** npm and Homebrew are just wrappers that call the same Python CLI core.

**Result:** Consistent experience across all platforms! 🎉
