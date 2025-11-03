# AI Setup Guide for Git Quick

## Where AI is Used

AI is used in **one place**: the `git-quick` command to automatically generate commit messages from your code changes.

**Flow:**
1. You run `git-quick`
2. It reads your git diff (changes)
3. Sends to AI provider
4. AI generates a commit message like: `feat(auth): add login support`
5. You confirm or edit the message
6. Commits and pushes

## Three Options (Pick One)

### Option 1: Ollama (Recommended - Free, Local, No API Keys!)

**Best for:** Everyone! No cost, runs on your machine, private.

```bash
# 1. Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# 2. Download a model (one-time, ~2GB)
ollama pull llama3.2

# 3. That's it! No configuration needed
git-quick  # Will automatically use Ollama
```

**How it works:**
- Ollama runs a local AI model on your computer
- No internet required after download
- No API keys needed
- Completely private

**Config (optional):**
```toml
# ~/.gitquick.toml (or ~/.gitquick/config.toml)
[quick]
ai_provider = "ollama"
ai_model = "llama3.2"  # or "codellama", "mistral", etc.

[ai]
ollama_host = "http://localhost:11434"  # default
```

### Option 2: OpenAI (Paid, Cloud, Best Quality)

**Best for:** If you want the highest quality commit messages and already have OpenAI credits.

```bash
# 1. Get API key from https://platform.openai.com/api-keys

# 2. Create config file
cat > ~/.gitquick.toml << 'EOF'
[quick]
ai_provider = "openai"
ai_model = "gpt-4o-mini"  # Cheap and good

[ai]
openai_api_key = "sk-proj-your-key-here"
EOF

# 3. Use it!
git-quick
```

**Cost:**
- gpt-4o-mini: ~$0.15 per 1M tokens (very cheap)
- gpt-4o: ~$2.50 per 1M tokens (best quality)
- Typical commit: ~0.0001 cents

**Where's the AI key used?**
- File: `git_quick/ai_commit.py`, lines 76-97
- Only called when generating commit messages
- Uses OpenAI Python SDK

### Option 3: Anthropic Claude (Paid, Cloud)

**Best for:** If you prefer Claude's writing style for technical commits.

```bash
# 1. Get API key from https://console.anthropic.com/

# 2. Create config file
cat > ~/.gitquick.toml << 'EOF'
[quick]
ai_provider = "anthropic"
ai_model = "claude-3-5-sonnet-20241022"

[ai]
anthropic_api_key = "sk-ant-your-key-here"
EOF

# 3. Use it!
git-quick
```

**Cost:**
- Claude 3.5 Sonnet: ~$3 per 1M input tokens
- Typical commit: ~0.0003 cents

**Where's the AI key used?**
- File: `git_quick/ai_commit.py`, lines 99-122
- Only called when generating commit messages
- Uses Anthropic Python SDK

### Option 4: No AI (Free, Instant)

**Best for:** If you don't want AI or just want to try the tool.

```bash
# Just use the --no-ai flag
git-quick --no-ai

# Or set as default in config
cat > ~/.gitquick.toml << 'EOF'
[quick]
ai_provider = "fallback"  # disables AI
EOF
```

**How it works:**
- Uses simple rules to generate messages
- Looks at file types and names
- Example: Changed `README.md` → `docs: update documentation`
- See code: `git_quick/ai_commit.py`, lines 124-140

## Configuration File Locations

Git Quick looks for config in these locations (in order):

1. `./.gitquick.toml` (project-specific)
2. `~/.gitquick.toml` (user config)
3. `~/.gitquick/config.toml` (also user config)

Create any of these files:

```toml
[quick]
auto_push = true           # Auto-push after commit
emoji_style = "gitmoji"    # Add emoji like ✨ 🐛 📝
ai_provider = "ollama"     # "ollama", "openai", "anthropic", or "fallback"
ai_model = "llama3.2"      # Model to use
conventional_commits = true # Use conventional format

[ai]
# Only needed if using paid services:
openai_api_key = ""        # Your OpenAI key (sk-proj-...)
anthropic_api_key = ""     # Your Anthropic key (sk-ant-...)
ollama_host = "http://localhost:11434"  # Ollama server
```

## Code Locations

AI integration is in these files:

1. **Main AI logic**: `git_quick/ai_commit.py`
   - Line 54-74: Ollama integration
   - Line 76-97: OpenAI integration
   - Line 99-122: Anthropic integration
   - Line 124-140: Fallback (no AI)

2. **Used by**: `git_quick/cli.py`
   - Line 38-47: Calls AI when you run `git-quick`

3. **Config**: `git_quick/config.py`
   - Line 44-49: AI configuration defaults

## Security Notes

### API Keys
- **Never commit API keys to git!**
- Keep them in `~/.gitquick.toml` (outside your repo)
- The tool reads from config file only
- Keys are never logged or printed

### What Data is Sent?
When using OpenAI or Anthropic:
- Git diff (your code changes)
- List of changed files
- Nothing else!

With Ollama:
- Everything stays on your computer
- No data sent to cloud

## Testing Your Setup

```bash
# Test Ollama
curl http://localhost:11434/api/version

# Test with dry-run
cd /path/to/git/repo
echo "test" >> README.md
git-quick --dry-run  # Won't actually commit

# Test without AI
git-quick --no-ai --dry-run

# See what AI provider is configured
cat ~/.gitquick.toml
```

## Troubleshooting

### "Ollama generation failed"
```bash
# Check if Ollama is running
curl http://localhost:11434/api/version

# Start Ollama (if needed)
ollama serve

# Check if model is downloaded
ollama list
```

### "OpenAI generation failed"
```bash
# Check API key is set
grep openai_api_key ~/.gitquick.toml

# Test API key
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer sk-proj-YOUR-KEY"
```

### "No module named 'openai'"
```bash
# Install the optional dependency
pip install openai
# or
pip install anthropic
```

### AI generates bad messages
```bash
# Try a different model
# For Ollama:
ollama pull codellama  # Better for code

# Update config:
[quick]
ai_model = "codellama"
```

### Want to disable AI temporarily?
```bash
# Just use the flag
git-quick --no-ai
```

## Comparison

| Provider | Cost | Speed | Quality | Privacy | Setup |
|----------|------|-------|---------|---------|-------|
| **Ollama** | Free | Fast | Good | 100% | Medium |
| **OpenAI** | ~$0.0001/commit | Fast | Best | No | Easy |
| **Anthropic** | ~$0.0003/commit | Fast | Great | No | Easy |
| **Fallback** | Free | Instant | Basic | 100% | None |

## Recommendations

1. **Start with Ollama** - Free, private, good quality
2. **Upgrade to OpenAI** - If you need perfect messages
3. **Use Fallback** - If you just want basic automation

## Need Help?

- Ollama docs: https://ollama.ai/
- OpenAI docs: https://platform.openai.com/docs
- Anthropic docs: https://docs.anthropic.com/
- Git Quick issues: [Your GitHub repo]

## Example Workflow

```bash
# One-time setup (choose your option)
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama3.2

# Daily usage
cd ~/my-project
# ... make changes ...
git-quick
# ✨ feat(api): add user endpoint
# Confirm? [Y/n]: y
# ✓ Committed and pushed!

# No AI version
git-quick --no-ai
# chore: update 3 files
# Confirm? [Y/n]: y
```

That's it! The AI setup is optional and flexible. Start simple (Ollama or no AI), upgrade later if needed.
