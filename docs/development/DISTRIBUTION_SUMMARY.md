# Distribution Summary

## Installation Methods

Git Quick can be installed in **4 different ways** to support all platforms and user preferences.

### 1. Homebrew (macOS/Linux) 🍺

**Command:**

```bash
brew tap yourusername/git-quick
brew install git-quick
```

**How it works:**

- Homebrew formula: `Formula/git-quick.rb`
- Installs Python package in isolated virtualenv
- Adds commands to PATH automatically
- Includes shorter aliases: `gq`, `gs`, `gt`, `gsa`

**Files involved:**

- `Formula/git-quick.rb` - Homebrew formula definition

**Publishing:**

```bash
# Create tap repo: homebrew-git-quick
# Push formula
# Users install with: brew tap + brew install
```

**Best for:** Mac users who prefer Homebrew

---

### 2. npm (Cross-platform) 📦

**Command:**

```bash
npm install -g git-quick-cli
```

**How it works:**

- npm package wraps Python CLI
- Node.js scripts in `bin/` call Python
- Auto-installs Python package on first run
- Works on Windows, Mac, Linux

**Files involved:**

- `package.json` - npm package config
- `bin/git-quick.js` - Node wrapper script
- `bin/git-story.js` - Node wrapper script
- `bin/git-time.js` - Node wrapper script
- `bin/git-sync-all.js` - Node wrapper script
- `scripts/postinstall.js` - Post-install setup

**Publishing:**

```bash
npm publish
```

**Best for:** JavaScript developers, Windows users, cross-platform consistency

---

### 3. pip (Python) 🐍

**Command:**

```bash
pip install git-quick
```

**How it works:**

- Pure Python package
- Installs to Python's bin directory
- Uses setuptools entry points
- Smallest install footprint

**Files involved:**

- `pyproject.toml` - Python package config
- `git_quick/` - Python source code
- `setup.py` (optional) - Alternative setup

**Publishing:**

```bash
python -m build
python -m twine upload dist/*
```

**Best for:** Python developers, minimal installs, Linux servers

---

### 4. From Source (Development) 💻

**Command:**

```bash
git clone https://github.com/vswaroop04/git-quick.git
cd git-quick
pip install -e .
```

**How it works:**

- Editable install (`-e` flag)
- Changes immediately reflected
- Includes dev dependencies
- Git repo stays linked

**Files involved:**

- All source files
- `pyproject.toml[dev]` - Dev dependencies

**Best for:** Contributors, testing, development

---

## Architecture

### Python Core (Shared by All)

```
git_quick/
├── cli.py              # Entry points
├── config.py           # Configuration
├── git_utils.py        # Git operations
├── ai_commit.py        # AI integration
└── commands/           # Command implementations
```

**Entry points defined in `pyproject.toml`:**

```toml
[project.scripts]
git-quick = "git_quick.cli:quick"
git-story = "git_quick.cli:story"
git-time = "git_quick.cli:time_track"
git-sync-all = "git_quick.cli:sync_all"
```

### Wrapper Layers

**Homebrew:**

```
brew install → virtualenv → Python package → Commands
```

**npm:**

```
npm install → Node.js wrapper → Python package → Commands
```

**pip:**

```
pip install → Python package → Commands
```

**Source:**

```
pip install -e . → Python package (editable) → Commands
```

---

## File Structure for Distribution

```
git-quick/
├── pyproject.toml          # Python package config
├── package.json            # npm package config
├── Formula/
│   └── git-quick.rb        # Homebrew formula
├── bin/                    # npm wrapper scripts
│   ├── git-quick.js
│   ├── git-story.js
│   ├── git-time.js
│   └── git-sync-all.js
├── scripts/
│   └── postinstall.js      # npm post-install
├── git_quick/              # Python source
│   ├── __init__.py
│   ├── cli.py
│   ├── config.py
│   ├── git_utils.py
│   ├── ai_commit.py
│   └── commands/
└── docs/
    └── INSTALLATION.md     # User guide
```

---

## Comparison

| Method       | Platform    | Size   | Speed  | Updates          | Isolation         |
| ------------ | ----------- | ------ | ------ | ---------------- | ----------------- |
| **Homebrew** | macOS/Linux | Large  | Medium | `brew upgrade`   | High (virtualenv) |
| **npm**      | All         | Medium | Fast   | `npm update -g`  | Low (global)      |
| **pip**      | All         | Small  | Fast   | `pip install -U` | Low (global)      |
| **Source**   | All         | Small  | Fast   | `git pull`       | Dev mode          |

---

## Publishing Checklist

### Before Publishing

- [ ] Update version in:
  - [ ] `pyproject.toml`
  - [ ] `package.json`
  - [ ] `git_quick/__init__.py`
  - [ ] `Formula/git-quick.rb`
- [ ] Update `CHANGELOG.md`
- [ ] Run tests: `make test`
- [ ] Build documentation
- [ ] Create git tag: `git tag v0.1.0`

### Publish to PyPI

```bash
python -m build
python -m twine upload dist/*
```

### Publish to npm

```bash
npm publish
```

### Publish Homebrew Formula

```bash
# 1. Push tag to GitHub
git push origin v0.1.0

# 2. Get SHA256 of release tarball
curl -L https://github.com/user/git-quick/archive/refs/tags/v0.1.0.tar.gz -o release.tar.gz
shasum -a 256 release.tar.gz

# 3. Update Formula/git-quick.rb with SHA256

# 4. Push to homebrew-git-quick repo
cd homebrew-git-quick
cp ../git-quick/Formula/git-quick.rb Formula/
git add Formula/git-quick.rb
git commit -m "Update to v0.1.0"
git push
```

### Test Installations

```bash
# Test PyPI
pip install git-quick
git-quick --version

# Test npm
npm install -g git-quick-cli
git-quick --version

# Test Homebrew
brew tap yourusername/git-quick
brew install git-quick
git-quick --version
```

---

## User Installation Experience

### Homebrew User

```bash
$ brew tap yourusername/git-quick
$ brew install git-quick
🍺 Installing git-quick...
✓ Python virtualenv created
✓ Dependencies installed
✓ Commands linked to /usr/local/bin

$ git-quick --version
git-quick 0.1.0
```

### npm User

```bash
$ npm install -g git-quick-cli
+ git-quick-cli@0.1.0
✓ Node.js package installed
ℹ Installing Python dependencies...
✓ git-quick ready

$ git-quick --version
git-quick 0.1.0
```

### pip User

```bash
$ pip install git-quick
Collecting git-quick...
Installing collected packages: click, rich, gitpython, git-quick
Successfully installed git-quick-0.1.0

$ git-quick --version
git-quick 0.1.0
```

---

## Dependencies

### Runtime Dependencies (All Users)

From `pyproject.toml`:

```toml
dependencies = [
    "click>=8.0",
    "rich>=13.0",
    "gitpython>=3.1",
    "toml>=0.10",
    "openai>=1.0",      # Optional
    "anthropic>=0.25",  # Optional
    "requests>=2.31",
]
```

### Platform Dependencies

**Homebrew:**

- Python 3.11 (auto-installed)
- Git (assumed present)

**npm:**

- Node.js 14+ (user must have)
- Python 3.8+ (user must have)

**pip:**

- Python 3.8+ (user must have)
- Git (assumed present)

---

## Update Strategy

### For Users

**Homebrew:**

```bash
brew upgrade git-quick
```

**npm:**

```bash
npm update -g git-quick-cli
```

**pip:**

```bash
pip install --upgrade git-quick
```

### For Maintainers

1. Update version in all config files
2. Update CHANGELOG.md
3. Commit and tag
4. Publish to all platforms
5. Create GitHub release
6. Announce on social media

---

## Troubleshooting

### "command not found"

**Homebrew:**

```bash
brew link git-quick
```

**npm:**

```bash
npm install -g git-quick-cli --force
```

**pip:**

```bash
# Add to PATH
export PATH="$HOME/.local/bin:$PATH"
```

### Python not found (npm)

```bash
# npm wrapper needs Python
brew install python@3.11  # macOS
sudo apt install python3  # Linux
# Download from python.org (Windows)
```

### Version mismatch

```bash
# Force reinstall
brew reinstall git-quick
npm install -g git-quick-cli --force
pip install --force-reinstall git-quick
```

---

## Marketing Strategy

### Installation Badges for README

```markdown
[![PyPI](https://img.shields.io/pypi/v/git-quick)](https://pypi.org/project/git-quick/)
[![npm](https://img.shields.io/npm/v/git-quick-cli)](https://www.npmjs.com/package/git-quick-cli)
[![Homebrew](https://img.shields.io/badge/homebrew-git--quick-orange)](https://github.com/yourusername/homebrew-git-quick)
```

### Homepage Messaging

**Heading:** Install git-quick your way

**Subheading:** Choose your preferred package manager

**Tabs:**

- 🍺 Homebrew (for Mac)
- 📦 npm (for All)
- 🐍 pip (for Python)
- 💻 Source (for Dev)

---

## Success Metrics

### Downloads

- PyPI: Track on https://pypistats.org/
- npm: Track on https://npmcharts.com/
- Homebrew: `brew info git-quick` (installs)

### Goals

- Week 1: 100 installs
- Month 1: 1,000 installs
- Month 6: 10,000 installs

### Platforms

Target distribution:

- Homebrew: 40% (Mac developers)
- pip: 35% (Python developers)
- npm: 20% (JS developers)
- Source: 5% (Contributors)

---

## Summary

**Three distribution channels:**

1. ✅ PyPI (pip) - Ready to publish
2. ✅ npm - Ready to publish
3. ✅ Homebrew - Ready to publish

**All sharing the same Python core**, just different installation wrappers.

**Users get:**

- Their preferred package manager
- Same commands and features
- Platform-optimized experience
- Easy updates

**You maintain:**

- One codebase (Python)
- Three config files (pyproject.toml, package.json, Formula/\*.rb)
- Three publishing workflows
- Unified documentation
