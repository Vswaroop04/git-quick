# First Run Experience

## What Happens When You First Run git-quick

### Scenario 1: User Chooses Ollama (Recommended)

```bash
$ gq

╔═══════════════════════════════════════════════════════════╗
║           Welcome to Git Quick! 🚀                        ║
║                                                           ║
║ Let's set up AI-powered commit messages.                 ║
║ You can change this later in ~/.gitquick.toml            ║
╚═══════════════════════════════════════════════════════════╝

┏━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┓
┃ Option ┃ Provider   ┃ Description               ┃ Cost  ┃
┡━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━┩
│ 1      │ Ollama     │ Local AI (recommended)    │ FREE  │
│ 2      │ OpenAI     │ GPT-4 via API             │ Paid  │
│ 3      │ Anthropic  │ Claude via API            │ Paid  │
│ 4      │ No AI      │ Smart fallback only       │ FREE  │
└────────┴────────────┴───────────────────────────┴───────┘

Choose your AI provider [1/2/3/4] (1): 1

Ollama is not installed
Install Ollama now? [Y/n]: y

Installing Ollama...
📥 Installing Ollama via install script...
✓ Ollama installed successfully!

Starting Ollama server...
Waiting for Ollama to start...... ✓
✓ Ollama server started successfully!

Download llama3 model (~4GB)? [Y/n]: y

Downloading llama3 model...
This may take a few minutes (model is ~4GB)

pulling manifest
pulling 6a0746a1ec1a... 100% ▕████████████████▏ 4.7 GB
pulling 4fa551d4f938... 100% ▕████████████████▏  12 KB
pulling 8ab4849b038c... 100% ▕████████████████▏  254 B
pulling 577073ffcc6c... 100% ▕████████████████▏  110 B
pulling ad1518640c43... 100% ▕████████████████▏  483 B
verifying sha256 digest
writing manifest
success

✓ llama3 model installed successfully!

============================================================
✨ Setup complete! You're ready to use gq
============================================================

Quick commands:
  gq                     # Quick commit & push
  gq story               # Show commit history
  gq time start          # Track time
  gq --help              # See all options

Note: git-quick still works as an alias

# Now gq proceeds with the commit...
```

### Scenario 2: User Chooses OpenAI

```bash
$ gq

╔═══════════════════════════════════════════════════════════╗
║           Welcome to Git Quick! 🚀                        ║
╚═══════════════════════════════════════════════════════════╝

Choose your AI provider [1/2/3/4] (1): 2

OpenAI Setup
Get your API key from: https://platform.openai.com/api-keys

Enter your OpenAI API key: ••••••••••••••••••••••••••••••••••

✓ OpenAI configured successfully!

============================================================
✨ Setup complete! You're ready to use gq
============================================================
```

### Scenario 3: User Skips Setup

```bash
$ gq

First time running gq!
Run setup wizard? [Y/n]: n

Skipping setup. Using fallback mode.
Run 'gq --setup' anytime to configure AI.

# Proceeds with smart fallback commit messages
```

### Scenario 4: User Already Has Ollama Installed

```bash
$ gq

╔═══════════════════════════════════════════════════════════╗
║           Welcome to Git Quick! 🚀                        ║
╚═══════════════════════════════════════════════════════════╝

Choose your AI provider [1/2/3/4] (1): 1

✓ Ollama is already installed!
✓ Found models: llama3:latest, codellama:latest

Use llama3:latest? [Y/n]: y

✓ Configuration saved!

============================================================
✨ Setup complete! You're ready to use gq
============================================================
```

## Changing Configuration Later

### Option 1: Run Setup Wizard Again

```bash
gq --setup
```

This will show the same wizard and let you:

- Switch AI providers (Ollama → OpenAI, etc.)
- Update API keys
- Download different models
- Reconfigure all settings

### Option 2: Edit Config File Manually

Edit `~/.gitquick.toml`:

```bash
# Open in your editor
nano ~/.gitquick.toml
# or
code ~/.gitquick.toml
```

Change any settings:

```toml
[quick]
ai_provider = "openai"  # Change to: "ollama", "anthropic", or "fallback"
ai_model = "gpt-4o-mini"  # Change model

[ai]
openai_api_key = "sk-proj-new-key"  # Update API key
```

Save and gq will use the new settings immediately.

### Option 3: Environment Variables (Temporary Override)

```bash
# Use different provider for one command
GITQUICK_AI_PROVIDER=openai gq

# Use different model
GITQUICK_AI_MODEL=gpt-4o gq
```

## What Gets Saved

The setup wizard creates `~/.gitquick.toml`:

```toml
[quick]
auto_push = true
emoji_style = "gitmoji"
ai_provider = "ollama"  # or "openai", "anthropic", "fallback"
ai_model = "llama3"
conventional_commits = true

[ai]
openai_api_key = "sk-proj-..."  # Only if you chose OpenAI
anthropic_api_key = ""
ollama_host = "http://localhost:11434"

[setup]
completed = true  # Prevents wizard from running again
```

## Skipping the Wizard in CI/CD

For automated environments, the wizard won't run if:

- stdin is not a TTY (non-interactive)
- You use `--no-ai` flag
- Config file already exists with `setup.completed = true`

Example for CI:

```bash
gq --no-ai -y  # Uses fallback, auto-confirms
```
