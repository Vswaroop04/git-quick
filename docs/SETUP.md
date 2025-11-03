# Setup Guide

Complete setup guide for Git Quick.

## Installation

### Via pip (Recommended)

```bash
pip install git-quick
```

### From Source

```bash
git clone https://github.com/vswaroop04/git-quick.git
cd git-quick
pip install -e .
```

## Configuration

### Basic Configuration

Create `~/.gitquick.toml`:

```toml
[quick]
auto_push = true
emoji_style = "gitmoji"
ai_provider = "ollama"
ai_model = "llama3.2"
conventional_commits = true

[story]
default_range = "last-release"
color_scheme = "dark"
group_by = "date"
max_commits = 50

[time]
auto_track = true
idle_threshold = 300
data_dir = "~/.gitquick/time"

[sync]
auto_stash = true
prune = true
fetch_all = true
```

Or use the CLI to create default config:

```bash
git-quick --init-config
```

### AI Provider Setup

#### Ollama (Local, Free)

1. Install Ollama:

   ```bash
   curl -fsSL https://ollama.ai/install.sh | sh
   ```

2. Pull a model:

   ```bash
   ollama pull llama3.2
   ```

3. Configure Git Quick:

   ```toml
   [quick]
   ai_provider = "ollama"
   ai_model = "llama3.2"

   [ai]
   ollama_host = "http://localhost:11434"
   ```

#### OpenAI

1. Get API key from https://platform.openai.com/api-keys

2. Configure:

   ```toml
   [quick]
   ai_provider = "openai"
   ai_model = "gpt-4o-mini"

   [ai]
   openai_api_key = "sk-..."
   ```

#### Anthropic (Claude)

1. Get API key from https://console.anthropic.com/

2. Configure:

   ```toml
   [quick]
   ai_provider = "anthropic"
   ai_model = "claude-3-5-sonnet-20241022"

   [ai]
   anthropic_api_key = "sk-ant-..."
   ```

## VS Code Extension

### Installation

1. Install from VS Code marketplace:

   - Search for "Git Quick"
   - Click Install

2. Or install from VSIX:
   ```bash
   code --install-extension git-quick-vscode-1.1.1.vsix
   ```

### Configuration

Open VS Code settings (Cmd/Ctrl + ,) and search for "Git Quick":

```json
{
  "gitQuick.autoPush": true,
  "gitQuick.emojiStyle": "gitmoji",
  "gitQuick.aiProvider": "ollama",
  "gitQuick.aiModel": "llama3.2",
  "gitQuick.cliPath": "git-quick",
  "gitQuick.conventionalCommits": true
}
```

## Git Hooks (Optional)

### Auto Time Tracking

Add to `.git/hooks/post-checkout`:

```bash
#!/bin/bash
git-time start
```

Make executable:

```bash
chmod +x .git/hooks/post-checkout
```

### Commit Message Validation

Add to `.git/hooks/commit-msg`:

```bash
#!/bin/bash
# Validate conventional commit format
commit_msg=$(cat "$1")

if ! echo "$commit_msg" | grep -qE "^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\(.+\))?: .{1,}$"; then
    echo "Error: Commit message must follow conventional commits format"
    echo "Example: feat(auth): add login support"
    exit 1
fi
```

Make executable:

```bash
chmod +x .git/hooks/commit-msg
```

## Verification

Test your installation:

```bash
# Check CLI installation
git-quick --version

# Test in a git repo
cd /path/to/git/repo
git-quick --dry-run

# Test other commands
git-story
git-time report
git-sync-all --dry-run
```

## Troubleshooting

### Command not found

Make sure Python scripts directory is in PATH:

```bash
# Add to ~/.bashrc or ~/.zshrc
export PATH="$HOME/.local/bin:$PATH"
```

### AI generation fails

Check your AI provider is running:

```bash
# For Ollama
curl http://localhost:11434/api/version

# Test manually
git-quick --no-ai  # Use fallback generation
```

### Permission errors

```bash
# Fix permissions
chmod +x ~/.local/bin/git-quick
```

### Git extension not found (VS Code)

Make sure Git extension is enabled:

1. Open Extensions (Cmd/Ctrl + Shift + X)
2. Search for "Git"
3. Enable if disabled

## Next Steps

- Read [Usage Guide](USAGE.md) for examples
- Check [Configuration Guide](CONFIG.md) for advanced options
- See [Contributing Guide](../CONTRIBUTING.md) to contribute
