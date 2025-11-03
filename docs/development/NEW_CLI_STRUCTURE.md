# New Unified CLI Structure

## Overview

Git Quick now uses a **single unified command** with subcommands, making it cleaner and more intuitive!

## New Command Structure

```bash
git-quick               # Quick commit & push (default)
gq story         # Show commit history
gq time start    # Time tracking
gq sync          # Sync branches
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
gq story                       # Show commits
gq story --group-by type       # Group by type
gq story --format markdown     # Export markdown
gq story --max 20              # Limit commits
```

### Time (Time Tracking)

```bash
gq time start                  # Start tracking
gq time stop                   # Stop tracking
gq time report                 # Show report
gq time report --all           # All branches
gq time report --branch feat   # Specific branch
```

### Sync (Update Branches)

```bash
gq sync                 # Sync all branches
gq sync --dry-run       # Preview changes
gq sync --no-prune      # Don't prune deleted branches
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
gq story        # History
gq time start   # Time tracking
gq sync         # Sync
```

## Backward Compatibility

**Good news:** Old commands still work for backward compatibility!

```bash
git-story              # Still works, redirects to gq story
git-time start         # Still works, redirects to gq time start
git-sync-all           # Still works, redirects to gq sync
```

But we recommend using the new unified style.

## Help System

```bash
git-quick --help              # Main help
gq story --help        # Story help
gq time --help         # Time help
gq time start --help   # Time start help
gq sync --help         # Sync help
```

## Examples

### Quick Workflow

```bash
# Make changes
echo "feature" >> file.txt

# Quick commit (default command)
git-quick

# See what you did
gq story

# Track your time
gq time report
```

### Using Subcommands

```bash
# Start tracking time
gq time start

# Work on feature...

# Commit changes
git-quick -m "feat: add awesome feature"

# Check commit history
gq story --group-by type

# Stop tracking
gq time stop

# Sync all branches
gq sync
```

### Advanced Usage

```bash
# Show last 10 commits grouped by author
gq story --group-by author --max 10

# Export changelog
gq story --format markdown > CHANGELOG.md

# Time report for specific branch
gq time report --branch feature-branch

# Dry run sync
gq sync --dry-run
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

gq time <TAB>
  start  stop  report

gq story <TAB>
  --group-by  --format  --max  --since
```

## Aliases

You can still create short aliases:

```bash
# In ~/.bashrc or ~/.zshrc
alias gq='git-quick'
alias gqs='gq story'
alias gqt='gq time'
alias gqsync='gq sync'
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
gq story
gq time report
gq sync
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
alias gqs='gq story'
alias gqt='gq time'
alias gqsync='gq sync'
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
