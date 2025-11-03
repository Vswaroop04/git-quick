# New Unified CLI Structure

## Overview

Git Quick now uses a **single unified command** with subcommands, making it cleaner and more intuitive!

## New Command Structure

```bash
git-quick               # Quick commit & push (default)
git-quick story         # Show commit history
git-quick time start    # Time tracking
git-quick sync          # Sync branches
```

## All Commands

### Main Command (Default)

```bash
git-quick                     # Quick commit & push (default action)
git-quick -m "message"        # With custom message
git-quick --no-push           # Commit without push
git-quick --no-ai             # Without AI
git-quick --dry-run           # Preview
```

### Story (Commit History)

```bash
git-quick story                       # Show commits
git-quick story --group-by type       # Group by type
git-quick story --format markdown     # Export markdown
git-quick story --max 20              # Limit commits
```

### Time (Time Tracking)

```bash
git-quick time start                  # Start tracking
git-quick time stop                   # Stop tracking
git-quick time report                 # Show report
git-quick time report --all           # All branches
git-quick time report --branch feat   # Specific branch
```

### Sync (Update Branches)

```bash
git-quick sync                 # Sync all branches
git-quick sync --dry-run       # Preview changes
git-quick sync --no-prune      # Don't prune deleted branches
```

## What Changed?

### Before (Old - Still Works!)

```bash
git-quick              # Commit & push
git-story              # History
git-time start         # Time tracking
git-sync-all           # Sync
```

### After (New - Recommended!)

```bash
git-quick              # Commit & push (same!)
git-quick story        # History
git-quick time start   # Time tracking
git-quick sync         # Sync
```

## Backward Compatibility

**Good news:** Old commands still work for backward compatibility!

```bash
git-story              # Still works, redirects to git-quick story
git-time start         # Still works, redirects to git-quick time start
git-sync-all           # Still works, redirects to git-quick sync
```

But we recommend using the new unified style.

## Help System

```bash
git-quick --help              # Main help
git-quick story --help        # Story help
git-quick time --help         # Time help
git-quick time start --help   # Time start help
git-quick sync --help         # Sync help
```

## Examples

### Quick Workflow

```bash
# Make changes
echo "feature" >> file.txt

# Quick commit (default command)
git-quick

# See what you did
git-quick story

# Track your time
git-quick time report
```

### Using Subcommands

```bash
# Start tracking time
git-quick time start

# Work on feature...

# Commit changes
git-quick -m "feat: add awesome feature"

# Check commit history
git-quick story --group-by type

# Stop tracking
git-quick time stop

# Sync all branches
git-quick sync
```

### Advanced Usage

```bash
# Show last 10 commits grouped by author
git-quick story --group-by author --max 10

# Export changelog
git-quick story --format markdown > CHANGELOG.md

# Time report for specific branch
git-quick time report --branch feature-branch

# Dry run sync
git-quick sync --dry-run
```

## Why This Change?

### Benefits

1. **Cleaner namespace** - One command instead of four
2. **Better discoverability** - `git-quick --help` shows all commands
3. **More intuitive** - Subcommands are obvious
4. **Industry standard** - Matches git, docker, kubectl patterns
5. **Still backward compatible** - Old commands work!

### Comparison

**Old way:**
```bash
$ which git-quick
/usr/local/bin/git-quick

$ which git-story
/usr/local/bin/git-story

$ which git-time
/usr/local/bin/git-time

$ which git-sync-all
/usr/local/bin/git-sync-all
```

**New way:**
```bash
$ which git-quick
/usr/local/bin/git-quick

$ git-quick --help
Commands:
  story   Show commit history
  time    Time tracking
  sync    Sync branches
```

## Tab Completion

The new structure enables better tab completion:

```bash
git-quick <TAB>
  story  time  sync  commit

git-quick time <TAB>
  start  stop  report

git-quick story <TAB>
  --group-by  --format  --max  --since
```

## Aliases

You can still create short aliases:

```bash
# In ~/.bashrc or ~/.zshrc
alias gq='git-quick'
alias gqs='git-quick story'
alias gqt='git-quick time'
alias gqsync='git-quick sync'
```

Then use:
```bash
gq                    # Quick commit
gqs                   # Story
gqt start             # Start time
gqsync                # Sync
```

## Migration Guide

### If You're Already Using Git Quick

**No action needed!** Old commands still work.

But we recommend updating your scripts:

```bash
# Old script
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

### If You Have Aliases

Update your aliases:

```bash
# Old
alias gq='git-quick'
alias gs='git-story'
alias gt='git-time'
alias gsa='git-sync-all'

# New (recommended)
alias gq='git-quick'
alias gqs='git-quick story'
alias gqt='git-quick time'
alias gqsync='git-quick sync'
```

## Summary

**Single unified command:** `git-quick`

**With subcommands:**
- `story` - Commit history
- `time` - Time tracking
- `sync` - Sync branches
- (default) - Quick commit & push

**Old commands still work** for backward compatibility!

**Cleaner, more intuitive, industry standard!** ✨
