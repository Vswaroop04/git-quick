# AI Integration Architecture

## Visual Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                         User runs: git-quick                         │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     git_quick/cli.py (Line 38-47)                    │
│  - Stages all changes (git add .)                                    │
│  - Gets git diff and file list                                       │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                 git_quick/ai_commit.py - AICommitGenerator           │
│                                                                       │
│  def generate(diff, files):                                          │
│    ├─ Check config.ai_provider                                       │
│    │                                                                  │
│    ├─ "ollama" ────────────────────────┐                            │
│    ├─ "openai" ────────────────────────┼─────┐                      │
│    ├─ "anthropic" ─────────────────────┼─────┼────┐                 │
│    └─ else (fallback) ─────────────────┼─────┼────┼───┐             │
└────────────────────────────────────────┼─────┼────┼───┼─────────────┘
                                         │     │    │   │
         ┌───────────────────────────────┘     │    │   │
         │                                     │    │   │
         ▼                                     ▼    ▼   ▼
┌──────────────────┐  ┌──────────────┐  ┌────────────┐  ┌─────────────┐
│   Ollama (FREE)  │  │OpenAI (PAID) │  │Anthropic   │  │  Fallback   │
│   Line 54-74     │  │Line 76-97    │  │Line 99-122 │  │  Line 124   │
│                  │  │              │  │            │  │  (No AI)    │
│ Local AI model   │  │ Cloud API    │  │ Cloud API  │  │  Rule-based │
│ localhost:11434  │  │ api.openai   │  │ api.anthropic│ │  detection  │
│                  │  │              │  │            │  │             │
│ NO API KEY! ✓    │  │ API KEY ✗    │  │ API KEY ✗  │  │ NO API! ✓   │
└────────┬─────────┘  └──────┬───────┘  └─────┬──────┘  └──────┬──────┘
         │                   │                 │                │
         └───────────────────┴─────────────────┴────────────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │ Generated commit msg:  │
                    │ "feat: add feature"    │
                    └───────────┬────────────┘
                                │
                                ▼
                    ┌────────────────────────┐
                    │  Add emoji (optional)  │
                    │  Line 164-178          │
                    │ "✨ feat: add feature" │
                    └───────────┬────────────┘
                                │
                                ▼
                    ┌────────────────────────┐
                    │ Show to user for       │
                    │ confirmation           │
                    │ "Use this? [Y/n]"      │
                    └───────────┬────────────┘
                                │
                    ┌───────────┴────────────┐
                    │                        │
                   Yes                      No
                    │                        │
                    ▼                        ▼
            ┌──────────────┐      ┌──────────────────┐
            │ git commit   │      │ User enters own  │
            │ git push     │      │ message          │
            └──────────────┘      └──────────────────┘
```

## Code Files Involved

### 1. Entry Point: `git_quick/cli.py`

```python
# Line 38-47 (simplified)
@click.command()
def quick():
    git = GitUtils()

    # Get changes
    diff = git.get_diff(staged=True)
    files = git.get_files_changed()

    # Generate AI message
    ai_gen = AICommitGenerator()  # ← Creates AI instance
    commit_msg = ai_gen.generate(diff, files)  # ← Calls AI

    # Rest of commit logic...
```

### 2. AI Provider Selection: `git_quick/ai_commit.py`

```python
# Line 15-26
def generate(self, diff: str, files: list[str]) -> str:
    """Generate a commit message from diff."""
    provider = self.config.ai_provider  # ← Reads config

    if provider == "ollama":
        return self._generate_ollama(diff, files)  # ← Local AI
    elif provider == "openai":
        return self._generate_openai(diff, files)  # ← OpenAI API
    elif provider == "anthropic":
        return self._generate_anthropic(diff, files)  # ← Claude API
    else:
        return self._generate_fallback(diff, files)  # ← No AI
```

### 3. Ollama Integration (NO API KEY)

```python
# Line 54-74
def _generate_ollama(self, diff: str, files: list[str]) -> str:
    """Generate using Ollama."""
    try:
        host = self.config.get("ai", "ollama_host", "http://localhost:11434")
        model = self.config.ai_model  # e.g., "llama3.2"

        prompt = self._create_prompt(diff, files)

        # Call local Ollama server
        response = requests.post(
            f"{host}/api/generate",
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=30,
        )

        message = response.json()["response"].strip()
        return self._clean_message(message)

    except Exception as e:
        print(f"Warning: Ollama generation failed: {e}")
        return self._generate_fallback(diff, files)  # ← Falls back on error
```

**Where API is called:**
- URL: `http://localhost:11434/api/generate`
- Method: POST
- Data: `{"model": "llama3.2", "prompt": "..."}`
- **No authentication needed** - it's your local server!

### 4. OpenAI Integration (API KEY REQUIRED)

```python
# Line 76-97
def _generate_openai(self, diff: str, files: list[str]) -> str:
    """Generate using OpenAI."""
    try:
        import openai

        # ← This is where API key is used!
        api_key = self.config.get("ai", "openai_api_key")
        if not api_key:
            return self._generate_fallback(diff, files)

        client = openai.OpenAI(api_key=api_key)  # ← API key here
        prompt = self._create_prompt(diff, files)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100
        )

        message = response.choices[0].message.content.strip()
        return self._clean_message(message)

    except Exception as e:
        print(f"Warning: OpenAI generation failed: {e}")
        return self._generate_fallback(diff, files)
```

**Where API key is stored:**
- File: `~/.gitquick.toml`
- Key: `[ai] openai_api_key = "sk-proj-..."`
- Read by: `config.py` → loaded into memory → used here

### 5. Anthropic Integration (API KEY REQUIRED)

```python
# Line 99-122
def _generate_anthropic(self, diff: str, files: list[str]) -> str:
    """Generate using Anthropic."""
    try:
        import anthropic

        # ← This is where API key is used!
        api_key = self.config.get("ai", "anthropic_api_key")
        if not api_key:
            return self._generate_fallback(diff, files)

        client = anthropic.Anthropic(api_key=api_key)  # ← API key here
        prompt = self._create_prompt(diff, files)

        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=100,
            messages=[{"role": "user", "content": prompt}],
        )

        message = response.content[0].text.strip()
        return self._clean_message(message)

    except Exception as e:
        print(f"Warning: Anthropic generation failed: {e}")
        return self._generate_fallback(diff, files)
```

**Where API key is stored:**
- File: `~/.gitquick.toml`
- Key: `[ai] anthropic_api_key = "sk-ant-..."`

### 6. Fallback (NO AI, NO API KEY)

```python
# Line 124-140
def _generate_fallback(self, diff: str, files: list[str]) -> str:
    """Generate a simple commit message without AI."""
    if not files:
        return "chore: update files"

    # Detect common patterns
    if any("test" in f.lower() for f in files):
        return "test: update tests"
    elif any("readme" in f.lower() or ".md" in f.lower() for f in files):
        return "docs: update documentation"
    elif any(".json" in f or ".toml" in f or ".yaml" in f for f in files):
        return "chore: update configuration"
    elif len(files) == 1:
        filename = files[0].split("/")[-1]
        return f"chore: update {filename}"
    else:
        return f"chore: update {len(files)} files"
```

**No external calls - just simple logic!**

## Configuration: `git_quick/config.py`

```python
# Line 16-49 (simplified)
DEFAULT_CONFIG = {
    "quick": {
        "ai_provider": "ollama",  # ← Controls which provider
        "ai_model": "llama3.2",
    },
    "ai": {
        "openai_api_key": "",      # ← OpenAI key stored here
        "anthropic_api_key": "",   # ← Anthropic key stored here
        "ollama_host": "http://localhost:11434",
    },
}

class Config:
    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or Path.home() / ".gitquick.toml"
        self._config = DEFAULT_CONFIG.copy()
        self.load()  # ← Loads from ~/.gitquick.toml
```

## What Data is Sent to AI?

### To Ollama (Local):
```python
# Line 60-64
prompt = """
Files changed: file1.py, file2.py
Diff:
+ def new_function():
+     pass
"""
```

### To OpenAI/Anthropic (Cloud):
Same prompt as above - **only your code diff and file names**. Nothing else!

## Security

### API Key Storage
```
~/.gitquick.toml  (your home directory)
├─ [ai]
│  ├─ openai_api_key = "sk-proj-..."      ← Stored here
│  └─ anthropic_api_key = "sk-ant-..."    ← Stored here
```

**Never stored in:**
- Git repository
- Command history
- Logs or output
- Environment variables (unless you set them)

### Reading API Keys
1. User creates `~/.gitquick.toml`
2. `config.py` reads file on startup (line 42-49)
3. Stores in memory as Python dict
4. AI providers read from config object
5. Passed to API client libraries

### What if API key is missing?
```python
if not api_key:
    return self._generate_fallback(diff, files)  # ← Graceful fallback
```

No crash! Just uses rule-based generation.

## Summary

| Component | File | Lines | API Key? |
|-----------|------|-------|----------|
| Entry point | `cli.py` | 38-47 | No |
| AI coordinator | `ai_commit.py` | 15-26 | No |
| Ollama | `ai_commit.py` | 54-74 | No |
| OpenAI | `ai_commit.py` | 76-97 | **Yes** |
| Anthropic | `ai_commit.py` | 99-122 | **Yes** |
| Fallback | `ai_commit.py` | 124-140 | No |
| Config | `config.py` | 16-49 | Stores keys |

## Quick Setup Reference

### No API Keys Needed (Ollama)
```bash
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama3.2
git-quick  # Just works!
```

### With API Keys (OpenAI/Anthropic)
```bash
# Create config
cat > ~/.gitquick.toml << 'EOF'
[quick]
ai_provider = "openai"

[ai]
openai_api_key = "sk-proj-your-key-here"
EOF

git-quick  # Will use OpenAI
```

### No AI At All
```bash
git-quick --no-ai  # Uses fallback
```

That's it! The integration is clean, secure, and optional.
