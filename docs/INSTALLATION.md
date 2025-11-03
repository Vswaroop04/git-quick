# Installation Guide

Multiple ways to install Git Quick - choose what works best for you!

## Installation Options

### 1. Homebrew (macOS/Linux) - Recommended for Mac

```bash
# Add tap (when published)
brew tap yourusername/git-quick

# Install
brew install git-quick

# Verify
git-quick --version
```

**Advantages:**

- ✅ Automatic dependency management
- ✅ Easy updates (`brew upgrade git-quick`)
- ✅ Clean uninstall (`brew uninstall git-quick`)
- ✅ Includes shorter aliases (gq, gs, gt)

**Post-install (optional):**

```bash
# Install Ollama for AI features
brew install ollama
ollama pull llama3.2
```

### 2. npm (Cross-platform)

```bash
# Install globally
npm install -g git-quick-cli

# Verify
git-quick --version
```

**Advantages:**

- ✅ Works on all platforms (Windows, Mac, Linux)
- ✅ Familiar for JavaScript developers
- ✅ Automatic Python package installation
- ✅ Easy updates (`npm update -g git-quick-cli`)

**Note:** Requires Python 3.8+ installed on your system.

### 3. pip (Python package manager)

```bash
# Install from PyPI (when published)
pip install git-quick

# Or install from source
git clone https://github.com/vswaroop04/git-quick.git
cd git-quick
pip install -e .

# Verify
git-quick --version
```

**Advantages:**

- ✅ Direct Python installation
- ✅ Smallest install size
- ✅ Best for Python developers
- ✅ Easy to contribute (`-e` flag for development)

### 4. From Source (Development)

```bash
# Clone repository
git clone https://github.com/vswaroop04/git-quick.git
cd git-quick

# Install in development mode
pip install -e ".[dev]"

# Verify
git-quick --version
```

**Advantages:**

- ✅ Latest development version
- ✅ Easy to modify and contribute
- ✅ Includes development tools

## Comparison

| Method       | Platform    | Updates          | Dependencies | Best For     |
| ------------ | ----------- | ---------------- | ------------ | ------------ |
| **Homebrew** | macOS/Linux | `brew upgrade`   | Auto         | Mac users    |
| **npm**      | All         | `npm update -g`  | Auto         | JS devs      |
| **pip**      | All         | `pip install -U` | Manual       | Python devs  |
| **Source**   | All         | `git pull`       | Manual       | Contributors |

## Post-Installation

### 1. Verify Installation

```bash
# Check if commands are available
which git-quick
git-quick --version

# Test other commands
git-story --help
git-time --help
git-sync-all --help
```

### 2. Set Up AI Provider (Optional)

**Option A: Ollama (Free, Local)**

```bash
# macOS/Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Or with Homebrew
brew install ollama

# Download model
ollama pull llama3.2

# Test
git-quick
```

**Option B: OpenAI/Anthropic**

```bash
# Create config
cat > ~/.gitquick.toml << 'EOF'
[quick]
ai_provider = "openai"

[ai]
openai_api_key = "sk-proj-YOUR-KEY"
EOF
```

### 3. Create Shell Aliases (Optional)

**Bash/Zsh:**

```bash
# Add to ~/.bashrc or ~/.zshrc
cat >> ~/.bashrc << 'EOF'
# Git Quick aliases
alias gq='git-quick'
alias gs='git-story'
alias gt='git-time'
alias gsa='git-sync-all'
EOF

source ~/.bashrc
```

**Fish:**

```fish
# Add to ~/.config/fish/config.fish
abbr gq git-quick
abbr gs git-story
abbr gt git-time
abbr gsa git-sync-all
```

**PowerShell (Windows):**

```powershell
# Add to $PROFILE
Set-Alias -Name gq -Value git-quick
Set-Alias -Name gs -Value git-story
Set-Alias -Name gt -Value git-time
Set-Alias -Name gsa -Value git-sync-all
```

### 4. Test Installation

```bash
# Navigate to a git repo
cd /path/to/your/git/repo

# Test commands
git-quick --dry-run
git-story
git-time report
git-sync-all --dry-run
```

## Platform-Specific Instructions

### macOS

**Recommended: Homebrew**

```bash
brew tap yourusername/git-quick
brew install git-quick
brew install ollama
ollama pull llama3.2
```

**Alternative: pip**

```bash
# Install Python if needed
brew install python@3.11

# Install git-quick
pip3 install git-quick
```

### Linux (Ubuntu/Debian)

**Using pip:**

```bash
# Install Python
sudo apt update
sudo apt install python3 python3-pip

# Install git-quick
pip3 install git-quick

# Add to PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Install Ollama (optional)
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama3.2
```

**Using npm:**

```bash
# Install Node.js
sudo apt install nodejs npm

# Install git-quick
npm install -g git-quick-cli
```

### Windows

**Using pip:**

```powershell
# Install Python from https://python.org
# Make sure to check "Add Python to PATH"

# Install git-quick
pip install git-quick

# Or install Ollama
# Download from https://ollama.ai/download/windows
```

**Using npm:**

```powershell
# Install Node.js from https://nodejs.org

# Install git-quick
npm install -g git-quick-cli
```

## Updating

### Homebrew

```bash
brew upgrade git-quick
```

### npm

```bash
npm update -g git-quick-cli
```

### pip

```bash
pip install --upgrade git-quick
```

### From Source

```bash
cd git-quick
git pull
pip install -e .
```

## Uninstalling

### Homebrew

```bash
brew uninstall git-quick
```

### npm

```bash
npm uninstall -g git-quick-cli
```

### pip

```bash
pip uninstall git-quick
```

## Troubleshooting

### "command not found: git-quick"

**Check PATH:**

```bash
# For pip installations
echo $PATH | grep ".local/bin"

# If not in PATH, add it:
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

**Reinstall:**

```bash
# With pip
pip install --force-reinstall git-quick

# With npm
npm install -g --force git-quick-cli
```

### "Python 3.8+ required"

**macOS:**

```bash
brew install python@3.11
```

**Linux:**

```bash
sudo apt install python3.11
```

**Windows:**
Download from https://python.org

### Permission errors

**macOS/Linux:**

```bash
# Use --user flag
pip install --user git-quick

# Or fix permissions
sudo chown -R $USER ~/.local
```

**Windows:**
Run PowerShell as Administrator

### npm installation fails

```bash
# Clear cache
npm cache clean --force

# Reinstall
npm install -g git-quick-cli
```

## Development Installation

For contributors:

```bash
# Clone and install
git clone https://github.com/vswaroop04/git-quick.git
cd git-quick

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode with dev dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run tests
make test
```

## Publishing Checklist (For Maintainers)

### PyPI

```bash
# Build
python -m build

# Upload to TestPyPI (test first)
python -m twine upload --repository testpypi dist/*

# Upload to PyPI
python -m twine upload dist/*
```

### npm

```bash
# Update version in package.json
npm version patch  # or minor, major

# Publish
npm publish
```

### Homebrew

```bash
# Create tag
git tag v0.1.0
git push origin v0.1.0

# Update Formula/git-quick.rb with new SHA256
shasum -a 256 git-quick-0.1.0.tar.gz

# Submit to homebrew-core or host tap
```

## Next Steps

After installation:

1. Read the [Quick Start Guide](../QUICKSTART.md)
2. Configure AI provider ([AI Setup](../AI_SETUP.md))
3. Try it in a git repo
4. Join the community (coming soon)

## Getting Help

- Documentation: [README.md](../README.md)
- Issues: https://github.com/vswaroop04/git-quick/issues
- Discussions: https://github.com/vswaroop04/git-quick/discussions
