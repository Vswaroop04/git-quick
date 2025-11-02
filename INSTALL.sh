#!/bin/bash
# Git Quick Installation Script

set -e

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║           Git Quick - Installation Script                 ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.8"

if [[ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]]; then
    echo "❌ Python 3.8+ required. Current: $python_version"
    exit 1
fi
echo "✓ Python $python_version detected"
echo ""

# Install Git Quick
echo "Installing Git Quick..."
pip install -e .
echo "✓ Git Quick installed"
echo ""

# Check if Ollama is installed
echo "Checking for AI providers..."
if command -v ollama &> /dev/null; then
    echo "✓ Ollama found"

    # Check if a model is available
    if ollama list | grep -q "llama"; then
        echo "✓ Ollama model available"
    else
        echo "⚠️  No Ollama model found. Installing llama3.2..."
        ollama pull llama3.2
        echo "✓ llama3.2 installed"
    fi
else
    echo "⚠️  Ollama not found"
    echo ""
    echo "Would you like to install Ollama? (recommended for AI features) [y/N]"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        echo "Installing Ollama..."
        curl -fsSL https://ollama.ai/install.sh | sh
        echo "Installing llama3.2 model..."
        ollama pull llama3.2
        echo "✓ Ollama installed"
    else
        echo "ℹ️  You can use --no-ai flag or configure OpenAI/Anthropic"
    fi
fi
echo ""

# Create default config
echo "Creating default configuration..."
config_dir="$HOME/.gitquick"
config_file="$config_dir/config.toml"

mkdir -p "$config_dir"

if [ ! -f "$config_file" ]; then
    cat > "$config_file" << 'EOF'
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

[ai]
openai_api_key = ""
anthropic_api_key = ""
ollama_host = "http://localhost:11434"
EOF
    echo "✓ Config created at $config_file"
else
    echo "ℹ️  Config already exists at $config_file"
fi
echo ""

# Create aliases
echo "Would you like to add shell aliases? [y/N]"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    shell_rc=""
    if [ -n "$BASH_VERSION" ]; then
        shell_rc="$HOME/.bashrc"
    elif [ -n "$ZSH_VERSION" ]; then
        shell_rc="$HOME/.zshrc"
    fi

    if [ -n "$shell_rc" ]; then
        echo "" >> "$shell_rc"
        echo "# Git Quick aliases" >> "$shell_rc"
        echo "alias gq='git-quick'" >> "$shell_rc"
        echo "alias gs='git-story'" >> "$shell_rc"
        echo "alias gt='git-time'" >> "$shell_rc"
        echo "alias gsa='git-sync-all'" >> "$shell_rc"
        echo "✓ Aliases added to $shell_rc"
        echo "ℹ️  Run 'source $shell_rc' to activate"
    fi
fi
echo ""

# Test installation
echo "Testing installation..."
if command -v git-quick &> /dev/null; then
    echo "✓ git-quick command available"
else
    echo "⚠️  git-quick not in PATH"
    echo "   Add to PATH: export PATH=\"\$HOME/.local/bin:\$PATH\""
fi
echo ""

# Success message
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║              ✨ Installation Complete! ✨                 ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
echo "Quick Start:"
echo "  cd /path/to/your/git/repo"
echo "  git-quick                  # Quick commit & push"
echo "  git-story                  # Show commit history"
echo "  git-time start             # Track time"
echo "  git-sync-all               # Sync all branches"
echo ""
echo "Documentation:"
echo "  cat QUICKSTART.md          # 5-minute guide"
echo "  cat README.md              # Full documentation"
echo ""
echo "Configuration:"
echo "  vim ~/.gitquick/config.toml"
echo ""
echo "Get Help:"
echo "  git-quick --help"
echo "  https://github.com/yourusername/git-quick"
echo ""
