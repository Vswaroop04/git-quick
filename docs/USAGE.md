# Usage Guide

Complete guide to using Git Quick.

## git-quick

Quick commit and push with AI-generated messages.

### Basic Usage

```bash
# Quick commit and push (interactive)
git-quick

# With custom message
git-quick -m "feat: add new feature"

# Without push
git-quick --no-push

# Without AI (use fallback)
git-quick --no-ai

# Dry run (see what would happen)
git-quick --dry-run
```

### Workflow

1. Make changes to your files
2. Run `git-quick`
3. Review generated commit message
4. Confirm or edit
5. Automatically pushed to remote

### Example Session

```bash
$ git-quick

📋 Current status:
 M src/main.py
 M tests/test_main.py

📦 Staging all changes...
✓ Staged 2 file(s)

🤖 Generating commit message...

╭─ Generated Message ─────────────────────────╮
│ ✨ feat(main): add user authentication      │
╰─────────────────────────────────────────────╯

Use this message? [Y/n]: y

💾 Committing...
✓ Committed: a3f4d1e

🚀 Pushing to main...
✓ Pushed to origin/main

✨ Done!
```

## git-story

Show commit history in a beautiful format.

### Basic Usage

```bash
# Show commits since last release
git-story

# Show commits since specific tag
git-story --since v1.0.0

# Group by type (feat, fix, etc.)
git-story --group-by type

# Group by author
git-story --group-by author

# Limit number of commits
git-story --max 20

# Export to markdown
git-story --format markdown > CHANGELOG.md
```

### Example Output

```bash
$ git-story --group-by type

╭─ 📖 Commit Story ──────────────────────╮
│ 15 commits                             │
╰────────────────────────────────────────╯

FEAT
  • a3f4d1e add user authentication
  • b2c3e4f add dashboard page
  • c1d2e3f add email notifications

FIX
  • d4e5f6g fix login redirect
  • e5f6g7h fix database connection

DOCS
  • f6g7h8i update README
  • g7h8i9j add API documentation
```

## git-time

Track time spent on branches.

### Commands

```bash
# Start tracking current branch
git-time start

# Stop tracking
git-time stop

# Show report for current branch
git-time report

# Show report for all branches
git-time report --all

# Show report for specific branch
git-time report --branch feature-branch
```

### Example Output

```bash
$ git-time report --all

⏱️  Time Tracking Report

┌────────────────┬──────────┬──────────┬──────────┐
│ Branch         │ Total    │ Sessions │ Status   │
├────────────────┼──────────┼──────────┼──────────┤
│ feature-auth   │ 5h 30m   │ 8        │ 🟢 Active│
│ bugfix-login   │ 2h 15m   │ 3        │ ⚪ Stopped│
│ main           │ 1h 45m   │ 5        │ ⚪ Stopped│
└────────────────┴──────────┴──────────┴──────────┘
```

## git-sync-all

Update all local branches from remote.

### Basic Usage

```bash
# Sync all branches
git-sync-all

# Dry run (preview)
git-sync-all --dry-run

# Without pruning deleted branches
git-sync-all --no-prune
```

### Example Output

```bash
$ git-sync-all

╭─ 🔄 Syncing all branches ────────────────╮
│                                           │
╰───────────────────────────────────────────╯

Stashing uncommitted changes...
✓ Changes stashed

📥 Fetching from remote...
✓ Fetched latest changes

Found 5 local branches

Syncing branches... ━━━━━━━━━━━━━━━━━━━━━━ 100%

Restoring stashed changes...
✓ Changes restored

📊 Results:

┌────────────┬───────┬──────────────────────┐
│ Status     │ Count │ Branches             │
├────────────┼───────┼──────────────────────┤
│ ✅ Updated │ 2     │ main, develop        │
│ ✓ Up to    │ 2     │ feature-a, feature-b │
│   date     │       │                      │
│ ⚠️ No      │ 1     │ local-only           │
│   tracking │       │                      │
└────────────┴───────┴──────────────────────┘

✨ Sync complete!
```

## VS Code Extension

### Commands

Access via Command Palette (Cmd/Ctrl + Shift + P):

1. **Git Quick: Quick Commit & Push**
   - Stage, commit, and push in one click
   - Keyboard: `Ctrl+Shift+G Q`

2. **Git Quick: Generate AI Commit Message**
   - Generate message for staged changes
   - Inserts into commit input box
   - Keyboard: `Ctrl+Shift+G M`

3. **Git Quick: Show Commit Story**
   - Opens commit history in new tab

4. **Git Quick: Show Time Report**
   - Shows time tracking report

5. **Git Quick: Sync All Branches**
   - Syncs all branches with remote

### Source Control Integration

- Buttons in Source Control view
- Status bar quick access
- One-click workflows

## Advanced Usage

### Custom Commit Templates

Create templates in `~/.gitquick/templates/`:

```bash
# ~/.gitquick/templates/feature.txt
feat({{scope}}): {{description}}

## Changes
- {{change1}}
- {{change2}}

## Testing
{{testing}}
```

Use with:
```bash
git-quick --template feature
```

### Scripting

Use in scripts:

```bash
#!/bin/bash
# Auto-commit script

# Check for changes
if git diff-index --quiet HEAD --; then
    echo "No changes"
    exit 0
fi

# Quick commit with AI
git-quick --no-push

# Run tests
npm test

# Push if tests pass
if [ $? -eq 0 ]; then
    git push
else
    echo "Tests failed, not pushing"
    exit 1
fi
```

### CI/CD Integration

```yaml
# .github/workflows/auto-commit.yml
name: Auto Commit

on:
  schedule:
    - cron: '0 0 * * *'  # Daily

jobs:
  commit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install Git Quick
        run: pip install git-quick
      - name: Auto commit
        run: |
          git config user.name "Bot"
          git config user.email "bot@example.com"
          git-quick -m "chore: automated update"
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Tips & Tricks

### 1. Use Aliases

```bash
# Add to ~/.bashrc or ~/.zshrc
alias gq='git-quick'
alias gs='git-story'
alias gt='git-time'
alias gsa='git-sync-all'
```

### 2. Configure Per-Repository

Create `.gitquick.toml` in repo root for project-specific settings:

```toml
[quick]
emoji_style = "none"  # No emojis for this project
auto_push = false     # Manual push
```

### 3. Use with Git Aliases

```bash
# Add to ~/.gitconfig
[alias]
    quick = !git-quick
    story = !git-story
    time = !git-time
    sync = !git-sync-all
```

Then use:
```bash
git quick
git story
```

### 4. Combine Commands

```bash
# Quick workflow
git-quick && npm run build && npm run test
```

## Common Workflows

### Feature Development

```bash
# Start new feature
git checkout -b feature/awesome
git-time start

# Make changes...

# Quick commit
git-quick

# More changes...

# See your progress
git-story
git-time report
```

### Bug Fix

```bash
# Create fix branch
git checkout -b fix/bug-123

# Fix the bug...

# Quick commit with AI message
git-quick

# Check commit message
git log -1
```

### Release Preparation

```bash
# Sync everything
git-sync-all

# Generate changelog
git-story --format markdown > CHANGELOG.md

# Check time spent
git-time report --all
```

## Next Steps

- See [Configuration Guide](CONFIG.md) for advanced configuration
- Check [Setup Guide](SETUP.md) for installation options
- Read [Contributing Guide](../CONTRIBUTING.md) to contribute
