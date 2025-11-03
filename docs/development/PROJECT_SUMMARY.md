# Git Quick - Project Summary

A comprehensive CLI tool and VS Code extension for lightning-fast Git workflows.

## Overview

Git Quick is a Python-based CLI tool that combines repetitive Git commands into smart, one-line operations with AI-powered commit message generation. It includes a VS Code extension for seamless editor integration.

## Key Features

### 1. git-quick
- Combines `git add`, `commit`, and `push`
- AI-generated commit messages using Ollama/OpenAI/Anthropic
- Conventional commits format
- Gitmoji support
- Interactive confirmation
- Dry-run mode

### 2. git-story
- Beautiful commit history visualization
- Grouping by date/author/type
- Colorized output with Rich
- Markdown export for changelogs
- Since last release tracking

### 3. git-time
- Automatic time tracking per branch
- Session history
- Detailed reports
- Multi-branch overview
- Integration with git hooks

### 4. git-sync-all
- Update all local branches from remote
- Automatic stashing
- Safe fast-forward
- Conflict detection
- Progress tracking

### 5. VS Code Extension
- Command palette integration
- Keyboard shortcuts
- Status bar quick access
- SCM view buttons
- AI message generation in editor

## Architecture

```
git-quick/
├── git_quick/              # Python package
│   ├── cli.py             # CLI entry points (Click)
│   ├── config.py          # Configuration management (TOML)
│   ├── git_utils.py       # Git operations (GitPython)
│   ├── ai_commit.py       # AI integrations
│   └── commands/          # Command implementations
│       ├── story.py       # Commit history
│       ├── time_tracker.py # Time tracking
│       └── sync.py        # Branch syncing
├── vscode-extension/      # VS Code extension (TypeScript)
│   ├── src/
│   │   └── extension.ts   # Extension entry point
│   └── package.json       # Extension manifest
├── tests/                 # Pytest tests
├── docs/                  # Documentation
└── examples/              # Example configs & scripts
```

## Technology Stack

### CLI Tool
- **Python 3.8+**: Core language
- **Click**: CLI framework
- **Rich**: Terminal output & colors
- **GitPython**: Git operations
- **TOML**: Configuration files
- **OpenAI/Anthropic/Requests**: AI providers

### VS Code Extension
- **TypeScript**: Extension language
- **VS Code API**: Editor integration
- **Node.js**: Runtime environment

### Testing & Quality
- **pytest**: Test framework
- **pytest-cov**: Coverage reporting
- **Black**: Code formatting
- **Ruff**: Linting
- **MyPy**: Type checking

### CI/CD
- **GitHub Actions**: Automated testing
- **Codecov**: Coverage tracking
- **Multi-platform**: Linux, macOS, Windows

## Installation

### User Installation
```bash
pip install git-quick
```

### Development Installation
```bash
git clone <repo-url>
cd git-quick
pip install -e ".[dev]"
```

### VS Code Extension
```bash
cd vscode-extension
npm install
npm run compile
```

## Configuration

Configuration via `~/.gitquick.toml`:

```toml
[quick]
auto_push = true
emoji_style = "gitmoji"
ai_provider = "ollama"
ai_model = "llama3.2"

[story]
default_range = "last-release"
group_by = "date"

[time]
auto_track = true
idle_threshold = 300

[ai]
openai_api_key = ""
anthropic_api_key = ""
ollama_host = "http://localhost:11434"
```

## AI Integration

### Supported Providers

1. **Ollama** (Recommended)
   - Local, free, private
   - No API keys needed
   - Models: llama3.2, codellama, etc.

2. **OpenAI**
   - GPT-4o-mini, GPT-4
   - Requires API key
   - Best quality

3. **Anthropic (Claude)**
   - Claude 3.5 Sonnet
   - Requires API key
   - Great for technical commits

4. **Fallback**
   - Rule-based generation
   - No AI required
   - Always available

### Commit Message Generation

AI analyzes:
- Git diff
- Changed files
- File types
- Conventional commit patterns

Generates:
- Type (feat/fix/docs/etc.)
- Scope (optional)
- Description
- Emoji (optional)

Example: `✨ feat(auth): add OAuth2 login support`

## Key Differentiators

| Tool | Git Quick Advantage |
|------|-------------------|
| lazygit | Lighter, CLI-only, AI messages |
| git-extras | Modern, maintained, better UX |
| gh | Local workflows, time tracking |
| gitmoji-cli | Full automation, AI generation |

## Use Cases

1. **Solo Developer**
   - Quick commits without thinking
   - Time tracking per feature
   - Auto-sync all branches

2. **Team Projects**
   - Consistent commit messages
   - Conventional commits
   - Changelog generation

3. **Open Source**
   - Beautiful commit history
   - Time investment tracking
   - Easy contribution workflow

4. **Documentation Projects**
   - Smart commit detection
   - Markdown changelog export
   - No emoji mode

## Development Workflow

```bash
# Format code
make format

# Run tests
make test

# Lint
make lint

# Build package
make build

# Build VS Code extension
make vscode-build
```

## Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov=git_quick tests/

# Specific test
pytest tests/test_ai_commit.py
```

## Future Enhancements

### Planned Features
- [ ] Template system for commit messages
- [ ] Git hooks management
- [ ] Team collaboration features
- [ ] Plugin system
- [ ] Jira/Linear integration
- [ ] Slack notifications
- [ ] Custom AI models
- [ ] Web dashboard

### VS Code Extension
- [ ] Inline diff with AI suggestions
- [ ] Commit message templates
- [ ] Time tracking visualization
- [ ] Branch switcher with time info

### CLI Improvements
- [ ] Interactive mode for all commands
- [ ] Better error messages
- [ ] Shell completion
- [ ] Git flow integration

## Project Structure Details

### Core Modules

**config.py**
- TOML-based configuration
- Default values
- Per-project overrides
- Gitmoji mappings

**git_utils.py**
- GitPython wrapper
- Common operations
- Error handling
- Branch management

**ai_commit.py**
- Multi-provider support
- Prompt engineering
- Message validation
- Fallback generation

**cli.py**
- Click commands
- Rich terminal output
- Interactive prompts
- Error handling

### Commands

**story.py**
- Commit parsing
- Grouping logic
- Colorization
- Markdown export

**time_tracker.py**
- JSON-based storage
- Session tracking
- Report generation
- Auto-tracking hooks

**sync.py**
- Branch enumeration
- Safe updates
- Stash management
- Progress tracking

## Dependencies

### Core
- click >= 8.0
- rich >= 13.0
- gitpython >= 3.1
- toml >= 0.10
- openai >= 1.0
- anthropic >= 0.25
- requests >= 2.31

### Development
- pytest >= 7.0
- pytest-cov >= 4.0
- black >= 23.0
- mypy >= 1.0
- ruff >= 0.1

## Performance Considerations

- Lazy loading of AI providers
- Caching of git operations
- Parallel branch updates
- Optimized diff reading
- Rich terminal performance

## Security

- API keys in config file (file permissions)
- No credential storage in git
- Local AI option (Ollama)
- No telemetry
- Open source

## Maintenance

### Regular Tasks
- Update dependencies
- Fix security vulnerabilities
- Update AI provider APIs
- Add new emoji mappings
- Improve documentation

### Release Process
1. Update version in pyproject.toml
2. Update CHANGELOG.md
3. Run tests
4. Build package
5. Publish to PyPI
6. Build VS Code extension
7. Publish to marketplace
8. Tag release on GitHub

## Community

- GitHub Issues: Bug reports
- Discussions: Feature requests
- Pull Requests: Contributions welcome
- Discord: (coming soon)
- Twitter: (coming soon)

## License

MIT License - See LICENSE file

## Credits

Built with:
- GitPython
- Click
- Rich
- VS Code API

Inspired by:
- lazygit
- git-extras
- gitmoji-cli

---

**Made for developers who want to focus on coding, not Git commands.**
