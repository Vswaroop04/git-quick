# Contributing to Git Quick

Thank you for your interest in contributing to Git Quick!

## Development Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/vswaroop04/git-quick.git
   cd git-quick
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install in development mode:

   ```bash
   pip install -e ".[dev]"
   ```

4. Run tests:
   ```bash
   pytest
   ```

## Project Structure

```
git-quick/
├── git_quick/              # Main Python package
│   ├── cli.py             # CLI commands
│   ├── config.py          # Configuration management
│   ├── git_utils.py       # Git operations
│   ├── ai_commit.py       # AI commit message generation
│   └── commands/          # Command implementations
│       ├── story.py       # git-story command
│       ├── time_tracker.py # git-time command
│       └── sync.py        # git-sync-all command
├── tests/                 # Tests
├── vscode-extension/      # VS Code extension
└── docs/                  # Documentation
```

## Code Style

We use:

- **Black** for code formatting
- **Ruff** for linting
- **MyPy** for type checking

Run formatters:

```bash
black git_quick tests
ruff check git_quick tests
mypy git_quick
```

## Commit Messages

Btw you can also use the same tool for commit msgs as well :>
We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

Types:

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `perf`: Performance
- `test`: Tests
- `chore`: Maintenance

Examples:

```
feat(ai): add support for Claude AI
fix(cli): handle empty git repositories
docs: update installation instructions
```

## Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Aim for >80% code coverage

Run tests:

```bash
pytest --cov=git_quick tests/
```

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feat/amazing-feature`)
3. Make your changes
4. Add tests
5. Run formatters and tests
6. Commit your changes (use conventional commits!)
7. Push to your fork
8. Open a Pull Request

### PR Checklist

- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] Code formatted with Black
- [ ] All tests passing
- [ ] Conventional commit messages
- [ ] CHANGELOG.md updated (for significant changes)

## VS Code Extension Development

1. Navigate to extension directory:

   ```bash
   cd vscode-extension
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Open in VS Code:

   ```bash
   code .
   ```

4. Press F5 to launch extension development host

5. Test your changes

6. Build for production:
   ```bash
   npm run compile
   ```

## Adding New Commands

To add a new command:

1. Create command implementation in `git_quick/commands/your_command.py`
2. Add CLI entry point in `git_quick/cli.py`
3. Register in `pyproject.toml` under `[project.scripts]`
4. Add tests in `tests/test_your_command.py`
5. Update documentation

Example:

```python
# git_quick/commands/your_command.py
def your_command(git: GitUtils):
    """Your command implementation."""
    pass

# git_quick/cli.py
@click.command()
def your_command():
    """Your command description."""
    git = GitUtils()
    your_command_impl(git)
```

## Adding AI Providers

To add a new AI provider:

1. Add provider method in `git_quick/ai_commit.py`:

   ```python
   def _generate_yourprovider(self, diff: str, files: list[str]) -> str:
       # Implementation
       pass
   ```

2. Update `generate()` method to call your provider
3. Add configuration options in `config.py`
4. Add tests
5. Update documentation

## Documentation

- Update README.md for user-facing changes
- Update docstrings for code changes
- Add examples for new features
- Keep CHANGELOG.md current

## Need Help?

- Open an issue for bugs
- Start a discussion for feature ideas
- Join our Discord (coming soon!)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
