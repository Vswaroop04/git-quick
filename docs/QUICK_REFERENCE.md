# Git Quick - Quick Reference Card

## Installation (Pick One)

```bash
brew install git-quick          # Homebrew (Mac/Linux)
npm install -g git-quick-cli    # npm (All platforms)
pip install git-quick           # pip (Python)
```

## Commands

**Primary command: `gq` with subcommands:**

| Command          | What it does                                      |
| ---------------- | ------------------------------------------------- |
| `gq`             | Stage, commit, and push with AI message (default) |
| `gq story`       | Show beautiful commit history                     |
| `gq time start`  | Start tracking time on current branch             |
| `gq time report` | Show time report                                  |
| `gq sync`        | Update all branches from remote                   |

**Backward compatibility:** Old commands (`git-quick`, `git-story`, `git-time`, `git-sync-all`) still work!

## Common Usage

```bash
# Quick commit (AI generates message)
gq

# Quick commit with your message
gq -m "feat: add login"

# Commit without push
gq --no-push

# Without AI (fallback mode)
gq --no-ai

# Dry run (see what would happen)
gq --dry-run

# Skip confirmation prompts (non-interactive)
gq --yes
gq -y

# Show commit history
gq story

# Group by type (feat, fix, docs)
gq story --group-by type

# Export to markdown
gq story --format markdown > CHANGELOG.md

# Track time
gq time start
gq time stop
gq time report --all

# Sync all branches
gq sync
```

## AI Setup (Optional - git-quick works without it!)

**git-quick works immediately after install** with intelligent fallback messages based on file types.

**Ollama (Optional - Free, Local AI):**

```bash
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama3
gq  # Now uses AI!
```

**OpenAI (Optional - Paid):**

```bash
cat > ~/.gitquick.toml << 'EOF'
[quick]
ai_provider = "openai"
[ai]
openai_api_key = "sk-proj-YOUR-KEY"
EOF
```

**Force fallback mode (skip AI):**

```bash
gq --no-ai
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

## Command Structure

Primary command is `gq`:
```bash
gq              # Quick commit (main command)
gq story        # Commit history
gq time         # Time tracking
gq sync         # Sync branches
```

Legacy aliases still work:
```bash
git-quick       # Same as gq
git-story       # Same as gq story
git-time        # Same as gq time
git-sync-all    # Same as gq sync
```

## Troubleshooting

```bash
# Command not found?
export PATH="$HOME/.local/bin:$PATH"

# Check version
gq --version

# Get help
gq --help
```

## More Info

- Full docs: `cat README.md`
- Installation: `cat docs/INSTALLATION.md`
- AI setup: `cat AI_SETUP.md`
- Usage examples: `cat docs/USAGE.md`

---

**Made with ❤️ for developers who hate repetitive Git commands**
