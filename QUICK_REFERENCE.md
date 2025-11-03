# Git Quick - Quick Reference Card

## Installation (Pick One)

```bash
brew install git-quick          # Homebrew (Mac/Linux)
npm install -g git-quick-cli    # npm (All platforms)
pip install git-quick           # pip (Python)
```

## Commands

**Single unified command with subcommands:**

| Command | What it does |
|---------|--------------|
| `git-quick` | Stage, commit, and push with AI message (default) |
| `git-quick story` | Show beautiful commit history |
| `git-quick time start` | Start tracking time on current branch |
| `git-quick time report` | Show time report |
| `git-quick sync` | Update all branches from remote |

**Tip:** Old commands (`git-story`, `git-time`, `git-sync-all`) still work for backward compatibility!

## Common Usage

```bash
# Quick commit (AI generates message)
git-quick

# Quick commit with your message
git-quick -m "feat: add login"

# Commit without push
git-quick --no-push

# Without AI (fallback mode)
git-quick --no-ai

# Dry run (see what would happen)
git-quick --dry-run

# Skip confirmation prompts (non-interactive)
git-quick --yes
git-quick -y

# Show commit history
git-quick story

# Group by type (feat, fix, docs)
git-quick story --group-by type

# Export to markdown
git-quick story --format markdown > CHANGELOG.md

# Track time
git-quick time start
git-quick time stop
git-quick time report --all

# Sync all branches
git-quick sync
```

## AI Setup (Optional)

**Ollama (Recommended - Free):**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama3.2
git-quick  # Works!
```

**OpenAI (Paid):**
```bash
cat > ~/.gitquick.toml << 'EOF'
[quick]
ai_provider = "openai"
[ai]
openai_api_key = "sk-proj-YOUR-KEY"
EOF
```

**No AI:**
```bash
git-quick --no-ai  # Uses fallback
```

## Configuration File

Create `~/.gitquick.toml`:

```toml
[quick]
auto_push = true
emoji_style = "gitmoji"
ai_provider = "ollama"

[ai]
openai_api_key = ""
anthropic_api_key = ""
ollama_host = "http://localhost:11434"
```

## Aliases (Optional)

```bash
# Add to ~/.bashrc or ~/.zshrc
alias gq='git-quick'
alias gs='git-story'
alias gt='git-time'
alias gsa='git-sync-all'
```

## Troubleshooting

```bash
# Command not found?
export PATH="$HOME/.local/bin:$PATH"

# Check version
git-quick --version

# Get help
git-quick --help
```

## More Info

- Full docs: `cat README.md`
- Installation: `cat docs/INSTALLATION.md`
- AI setup: `cat AI_SETUP.md`
- Usage examples: `cat docs/USAGE.md`

---

**Made with ❤️ for developers who hate repetitive Git commands**
