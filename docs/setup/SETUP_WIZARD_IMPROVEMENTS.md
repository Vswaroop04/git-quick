# Setup Wizard Improvements

## What Changed

I've enhanced git-quick with an **interactive first-run setup wizard** that makes onboarding seamless.

## Key Features

### 1. Automatic First-Run Detection
- When you run `git-quick` for the first time, it automatically prompts you to configure AI
- No manual configuration needed
- Smart detection: won't run in CI/CD or non-interactive environments

### 2. Four Setup Options

#### Option 1: Ollama (Recommended)
- **Automatic installation** on Linux
- **Browser-based installation** on macOS/Windows
- **Automatic model download** (llama3, ~4GB)
- **No API keys required**
- Completely free and private

#### Option 2: OpenAI
- Prompts for API key (with password masking)
- Validates key format (must start with `sk-`)
- Saves securely to `~/.gitquick.toml`

#### Option 3: Anthropic (Claude)
- Prompts for API key
- Saves securely to config

#### Option 4: No AI
- Uses smart fallback mode
- Works immediately without any setup
- Still generates good commit messages based on file changes

### 3. Manual Setup Command
```bash
git-quick --setup
```
- Run anytime to reconfigure
- Change AI providers
- Update API keys

### 4. Smart Detection

The wizard detects:
- ✅ If Ollama is already installed
- ✅ If Ollama is running
- ✅ What models are already downloaded
- ✅ If you're in a non-interactive environment (CI/CD)

### 5. Guided Installation

For Ollama:
1. Detects your OS (macOS/Linux/Windows)
2. Installs Ollama automatically (Linux) or opens download page (macOS/Windows)
3. Downloads the AI model with progress bar
4. Verifies installation
5. Configures git-quick automatically

## User Experience

### Before (Manual Setup)
```bash
# User had to manually:
1. Read documentation
2. Install Ollama separately
3. Download model separately
4. Create config file manually
5. Add API keys manually
```

### After (Automatic Setup)
```bash
# User just runs:
git-quick

# Wizard handles everything:
✓ Detects first run
✓ Shows options
✓ Installs Ollama (if chosen)
✓ Downloads model
✓ Saves configuration
✓ Ready to use!
```

## Technical Implementation

### Files Modified

1. **`git_quick/cli.py`**
   - Added `--setup` flag
   - Integrated `prompt_setup_if_needed()` in commit command
   - Runs wizard on first use

2. **`git_quick/config.py`**
   - Added `setup.completed` tracking
   - Prevents wizard from running multiple times

3. **`git_quick/setup_wizard.py`** (already existed, now integrated)
   - Interactive prompts with Rich UI
   - Platform detection
   - Ollama installation
   - Model downloading
   - API key input (with masking)

4. **`README.md`**
   - Added first-run setup section
   - Documented the wizard
   - Updated quick start guide

### Configuration Tracking

The wizard creates/updates `~/.gitquick.toml`:

```toml
[setup]
completed = true  # Prevents wizard from running again

[quick]
ai_provider = "ollama"  # User's choice
ai_model = "llama3"

[ai]
openai_api_key = ""  # Only if user chose OpenAI
anthropic_api_key = ""  # Only if user chose Anthropic
ollama_host = "http://localhost:11434"
```

## Benefits

### For Users
✅ **Zero configuration needed** - just install and run
✅ **Guided setup** - no need to read docs first
✅ **Flexible** - can reconfigure anytime
✅ **Smart defaults** - works immediately even without AI

### For Developers
✅ **Better onboarding** - users don't get stuck
✅ **Fewer support questions** - setup is automated
✅ **Professional UX** - matches modern CLI tools
✅ **CI/CD friendly** - auto-detects non-interactive mode

## Examples

### Example 1: New User with No Ollama
```bash
$ git-quick
# Wizard runs automatically
# Offers to install Ollama
# Downloads model
# Ready to use in 5 minutes
```

### Example 2: User with Ollama Already Installed
```bash
$ git-quick
# Wizard detects Ollama
# Detects existing models
# Just confirms and saves config
# Ready in 10 seconds
```

### Example 3: User Wants OpenAI
```bash
$ git-quick
# Wizard shows options
# User chooses OpenAI
# Enters API key (masked)
# Ready immediately
```

### Example 4: User Wants to Reconfigure
```bash
$ git-quick --setup
# Wizard runs again
# User can change provider
# New config saved
```

## CI/CD Compatibility

The wizard is smart about non-interactive environments:

```bash
# In CI/CD (non-interactive)
git-quick --no-ai -y
# Skips wizard, uses fallback, auto-confirms
```

## Security

- API keys are stored in `~/.gitquick.toml` (user's home directory)
- Keys are never committed to git
- Password masking during input
- File permissions respected

## Future Enhancements

Potential improvements:
- [ ] Test API keys before saving
- [ ] Support for custom Ollama hosts
- [ ] Model selection menu for Ollama
- [ ] Automatic model updates
- [ ] Setup profiles (work/personal)
- [ ] Import/export configurations

## Summary

The setup wizard transforms git-quick from "requires manual setup" to "works out of the box with guided configuration." Users can start using AI-powered commits in minutes, not hours.
