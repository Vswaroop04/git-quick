# Git Quick - Quickstart Guide

Get started with Git Quick in 5 minutes!

## Installation

```bash
pip install git-quick
```

Or from source:

```bash
git clone <your-repo-url>
cd git-quick
pip install -e .
```

## First Run

### 1. Set up AI Provider

**Option A: Ollama (Local, Free, Recommended)**

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull a model
ollama pull llama3.2

# That's it! Git Quick will use Ollama by default
```

**Option B: OpenAI**

```bash
# Create config file
cat > ~/.gitquick.toml << EOF
[quick]
ai_provider = "openai"

[ai]
openai_api_key = "sk-..."
EOF
```

**Option C: Skip AI (use simple generation)**

Just use `gq --no-ai` flag

### 2. Try it out!

```bash
# Navigate to a git repo
cd /path/to/your/project

# Make some changes
echo "test" >> README.md

# Use gq!
gq
```

That's it! You'll see:

1. Staged changes
2. AI-generated commit message
3. Confirmation prompt
4. Auto-commit and push

## Core Commands Cheatsheet

```bash
# Quick commit & push (default command)
gq

# Quick commit with custom message
gq -m "feat: add new feature"

# Show commit history
gq story

# Track development time
gq time start
gq time report

# Sync all branches
gq sync
```

**One unified command:** All features now accessible via `gq` subcommands!

## VS Code Extension

1. Install extension from VS Code marketplace
2. Use keyboard shortcuts:
   - `Ctrl+Shift+G Q` - Quick commit & push
   - `Ctrl+Shift+G M` - Generate commit message

## What Makes This Different?

### vs lazygit

- Lighter weight, CLI-only
- AI-powered commit messages
- Simpler for everyday workflows

### vs git-extras

- Modern, actively maintained
- AI integration
- Better UX with rich terminal output

### vs gh

- Focuses on local Git workflows, not GitHub
- Faster for common operations
- Time tracking built-in

### vs gitmoji-cli

- More than just emojis
- Full workflow automation
- AI message generation

## Common Use Cases

### Daily Development

```bash
# Morning: sync everything
gq sync

# During work: quick commits
gq

# Check progress
gq story
gq time report
```

### Feature Development

```bash
# Start feature
git checkout -b feature/awesome
gq time start

# Work, work, work...
gq  # Multiple times

# Check what you did
gq story --group-by type
```

### Bug Fixes

```bash
# Quick fix
git checkout -b fix/bug-123
echo "fix" >> file.py
gq  # AI generates: "fix: resolve bug-123"
```

### Release Prep

```bash
# Generate changelog
gq story --format markdown > CHANGELOG.md

# See time investment
gq time report --all
```

## Configuration

Create `~/.gitquick.toml`:

```toml
[quick]
auto_push = true          # Auto-push after commit
emoji_style = "gitmoji"   # Add emojis to commits
ai_provider = "ollama"    # AI provider

[story]
group_by = "date"         # How to group commits
max_commits = 50          # Limit history

[time]
auto_track = true         # Auto-track branch time
```

## Tips

### 1. Use Aliases (Optional)

```bash
# gq is already short, but you can add more if you like
# Add to ~/.bashrc or ~/.zshrc
alias gqs='gq story'
alias gqt='gq time'
```

### 2. Dry Run First

```bash
gq --dry-run  # See what would happen
```

### 3. No Push Mode

```bash
gq --no-push  # Commit but don't push
```

### 4. Per-Project Config

Create `.gitquick.toml` in project root:

```toml
[quick]
emoji_style = "none"  # This project prefers no emojis
```

## Troubleshooting

### Command not found

```bash
# Add Python bin to PATH
export PATH="$HOME/.local/bin:$PATH"
```

### AI not working

```bash
# Use fallback generation
gq --no-ai

# Or check Ollama is running
curl http://localhost:11434/api/version
```

### Permission denied

```bash
chmod +x ~/.local/bin/gq
```

## Next Steps

- Read [Full Documentation](README.md)
- See [Usage Examples](docs/USAGE.md)
- Check [Configuration Guide](docs/SETUP.md)
- Join community (coming soon!)

## Pro Tips

### Workflow Automation

```bash
# Create a daily commit script
cat > ~/bin/daily-commit.sh << 'EOF'
#!/bin/bash
cd ~/my-project
gq
gq story --max 1
EOF
chmod +x ~/bin/daily-commit.sh
```

### Git Hooks

```bash
# Auto-track time on branch switch
cat > .git/hooks/post-checkout << 'EOF'
#!/bin/bash
gq time start
EOF
chmod +x .git/hooks/post-checkout
```

### Team Setup

```bash
# Share config with team
cat > .gitquick.toml << EOF
[quick]
emoji_style = "none"
conventional_commits = true
auto_push = false  # Team prefers manual push
EOF
git add .gitquick.toml
git commit -m "chore: add gq config"
```

## Getting Help

- GitHub Issues: Report bugs
- Discussions: Ask questions
- Twitter: @gitquick (coming soon)
- Discord: (coming soon)

## License

MIT - feel free to use and modify!

---

Made with ❤️ by developers, for developers
