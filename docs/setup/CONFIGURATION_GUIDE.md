# Git Quick Configuration Guide

## How to Configure git-quick

There are **three ways** to configure git-quick, listed in order of precedence:

### 1. Environment Variables (Highest Priority)

Override any setting temporarily for a single command:

```bash
# Use different AI provider for one command
GITQUICK_AI_PROVIDER=openai gq

# Use different model
GITQUICK_AI_MODEL=gpt-4o gq

# Disable auto-push
GITQUICK_AUTO_PUSH=false gq
```

**Available Environment Variables:**

- `GITQUICK_AI_PROVIDER` - AI provider: `ollama`, `openai`, `anthropic`, `fallback`
- `GITQUICK_AI_MODEL` - Model name: `llama3`, `gpt-4o-mini`, `claude-3-5-sonnet-20241022`
- `GITQUICK_AUTO_PUSH` - Auto push after commit: `true`, `false`
- `GITQUICK_EMOJI_STYLE` - Emoji style: `gitmoji`, `none`
- `GITQUICK_CONVENTIONAL_COMMITS` - Use conventional format: `true`, `false`

### 2. Configuration File (User Settings)

Edit `~/.gitquick.toml` for persistent settings:

```bash
# Open in your editor
nano ~/.gitquick.toml
# or
code ~/.gitquick.toml
# or
vim ~/.gitquick.toml
```

**Full Configuration Example:**

```toml
[quick]
auto_push = true                # Automatically push after commit
emoji_style = "gitmoji"         # Use gitmoji emojis (✨ 🐛 📝)
ai_provider = "ollama"          # AI provider: ollama, openai, anthropic, fallback
ai_model = "llama3"             # Model to use
conventional_commits = true     # Use conventional commit format

[story]
default_range = "last-release"  # Show commits since: last-release, HEAD~10, v1.1.1
color_scheme = "dark"           # Color scheme: dark, light
group_by = "date"               # Group by: date, author, type
max_commits = 50                # Maximum commits to show

[time]
auto_track = true               # Auto-track time per branch
idle_threshold = 300            # Idle timeout in seconds
data_dir = "~/.gitquick/time"   # Where to store time data

[sync]
auto_stash = true               # Auto-stash before sync
prune = true                    # Prune deleted remote branches
fetch_all = true                # Fetch all remotes

[ai]
openai_api_key = ""             # Your OpenAI API key (if using OpenAI)
anthropic_api_key = ""          # Your Anthropic API key (if using Claude)
ollama_host = "http://localhost:11434"  # Ollama server URL

[setup]
completed = true                # Setup wizard completed
```

### 3. Setup Wizard (Interactive)

Run the interactive setup wizard anytime:

```bash
gq --setup
```

This will guide you through:

- Choosing AI provider
- Installing Ollama (if selected)
- Downloading models
- Entering API keys
- Configuring all settings

## Common Configuration Tasks

### Switch from Ollama to OpenAI

**Option 1: Edit config file**

```bash
nano ~/.gitquick.toml
```

Change:

```toml
[quick]
ai_provider = "openai"
ai_model = "gpt-4o-mini"

[ai]
openai_api_key = "sk-proj-your-key-here"
```

**Option 2: Run setup wizard**

```bash
gq --setup
# Choose option 2 (OpenAI)
```

### Change Ollama Model

```bash
# Edit config
nano ~/.gitquick.toml
```

Change:

```toml
[quick]
ai_model = "codellama"  # or "mistral", "llama3.2", etc.
```

Or use environment variable:

```bash
GITQUICK_AI_MODEL=codellama gq
```

### Disable Auto-Push

```bash
# Edit config
nano ~/.gitquick.toml
```

Change:

```toml
[quick]
auto_push = false
```

Or use flag:

```bash
gq --no-push
```

### Disable Emojis

```bash
# Edit config
nano ~/.gitquick.toml
```

Change:

```toml
[quick]
emoji_style = "none"
```

Or use flag:

```bash
gq --no-emoji
```

### Use Fallback Mode (No AI)

**Temporary:**

```bash
gq --no-ai
```

**Permanent:**

```bash
nano ~/.gitquick.toml
```

Change:

```toml
[quick]
ai_provider = "fallback"
```

## Managing Ollama

### Start Ollama Server

The setup wizard starts Ollama automatically, but if you need to start it manually:

```bash
ollama serve
```

This runs in the foreground. To run in background:

```bash
# macOS/Linux
nohup ollama serve > /dev/null 2>&1 &

# Or use the wizard which starts it automatically
gq --setup
```

### Stop Ollama Server

```bash
# macOS/Linux
killall ollama

# Or find and kill the process
ps aux | grep ollama
kill <PID>
```

### Check Ollama Status

```bash
# Check if running
curl http://localhost:11434/api/version

# List installed models
ollama list

# Pull a new model
ollama pull codellama
```

### Change Ollama Model

```bash
# Pull new model
ollama pull mistral

# Update config
nano ~/.gitquick.toml
```

Change:

```toml
[quick]
ai_model = "mistral"
```

## API Key Management

### Add OpenAI API Key

**Option 1: Setup wizard**

```bash
gq --setup
# Choose option 2 (OpenAI)
# Enter your API key when prompted
```

**Option 2: Edit config**

```bash
nano ~/.gitquick.toml
```

Add:

```toml
[quick]
ai_provider = "openai"
ai_model = "gpt-4o-mini"

[ai]
openai_api_key = "sk-proj-your-key-here"
```

### Add Anthropic API Key

**Option 1: Setup wizard**

```bash
gq --setup
# Choose option 3 (Anthropic)
# Enter your API key when prompted
```

**Option 2: Edit config**

```bash
nano ~/.gitquick.toml
```

Add:

```toml
[quick]
ai_provider = "anthropic"
ai_model = "claude-3-5-sonnet-20241022"

[ai]
anthropic_api_key = "sk-ant-your-key-here"
```

### Security Best Practices

1. **Never commit API keys to git**

   - Config file is in `~/.gitquick.toml` (outside your repos)
   - Add to `.gitignore` if you create project-specific configs

2. **Use environment variables for CI/CD**

   ```bash
   export GITQUICK_AI_PROVIDER=fallback
   gq --no-ai -y
   ```

3. **Rotate keys regularly**
   - Update keys in config file
   - Or run `gq --setup` to enter new keys

## Project-Specific Configuration

You can override settings per project by creating `.gitquick.toml` in your project root:

```bash
cd /path/to/your/project
nano .gitquick.toml
```

Example project config:

```toml
[quick]
auto_push = false  # Don't auto-push in this project
emoji_style = "none"  # No emojis for this project
```

**Note:** Add `.gitquick.toml` to `.gitignore` if it contains sensitive data!

## Configuration Priority

Settings are loaded in this order (later overrides earlier):

1. Default config (built-in)
2. User config (`~/.gitquick.toml`)
3. Project config (`./.gitquick.toml`)
4. Environment variables (`GITQUICK_*`)
5. Command-line flags (`--no-push`, `--no-ai`, etc.)

## Troubleshooting Configuration

### Check Current Configuration

```bash
# View your config file
cat ~/.gitquick.toml

# Test with dry-run to see what would happen
gq --dry-run
```

### Reset to Defaults

```bash
# Delete config file
rm ~/.gitquick.toml

# Run setup wizard again
gq --setup
```

### Verify AI Provider

```bash
# Test Ollama
curl http://localhost:11434/api/version

# Test OpenAI (replace with your key)
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer sk-proj-YOUR-KEY"

# Test Anthropic (replace with your key)
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: sk-ant-YOUR-KEY" \
  -H "anthropic-version: 2023-06-01"
```

## Examples

### Example 1: Use OpenAI for One Commit

```bash
GITQUICK_AI_PROVIDER=openai \
GITQUICK_AI_MODEL=gpt-4o \
gq
```

### Example 2: Disable AI for CI/CD

```bash
# In your CI/CD pipeline
export GITQUICK_AI_PROVIDER=fallback
gq --no-ai -y
```

### Example 3: Different Settings for Work vs Personal

**Work projects:**

```bash
# ~/.gitquick-work.toml
[quick]
ai_provider = "openai"
emoji_style = "none"
conventional_commits = true
```

**Personal projects:**

```bash
# ~/.gitquick.toml
[quick]
ai_provider = "ollama"
emoji_style = "gitmoji"
conventional_commits = true
```

Use with:

```bash
# Work
GITQUICK_CONFIG=~/.gitquick-work.toml gq

# Personal (default)
gq
```

## Getting Help

- Run setup wizard: `gq --setup`
- View all options: `gq --help`
- Check version: `gq --version`
- View config: `cat ~/.gitquick.toml`

## Summary

**Quick Start:**

1. Run `gq --setup` for interactive configuration
2. Or edit `~/.gitquick.toml` manually
3. Use environment variables for temporary overrides
4. Use command-line flags for one-off changes

**Most Common:**

- Change AI provider: `gq --setup`
- Disable auto-push: `gq --no-push`
- Disable AI: `gq --no-ai`
- Change model: Edit `ai_model` in `~/.gitquick.toml`
