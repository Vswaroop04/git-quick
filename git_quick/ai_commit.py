"""AI-powered commit message generation."""

import re
from typing import Optional, Tuple
import requests
from git_quick.config import get_config, GITMOJI_MAP


class AICommitGenerator:
    """Generate commit messages using AI."""

    def __init__(self):
        self.config = get_config()

    def generate(self, diff: str, files: list[str]) -> str:
        """Generate a commit message from diff."""
        provider = self.config.ai_provider

        if provider == "ollama":
            return self._generate_ollama(diff, files)
        elif provider == "openai":
            return self._generate_openai(diff, files)
        elif provider == "anthropic":
            return self._generate_anthropic(diff, files)
        else:
            return self._generate_fallback(diff, files)

    def _create_prompt(self, diff: str, files: list[str]) -> str:
        """Create prompt for AI."""
        files_str = ", ".join(files[:5])
        if len(files) > 5:
            files_str += f" and {len(files) - 5} more"

        # Limit diff size to avoid token limits
        diff_excerpt = diff[:2000] if len(diff) > 2000 else diff

        prompt = f"""You are a git commit message generator. Analyze the changes and output ONLY the commit message in conventional commit format.

Files changed: {files_str}

Diff:
{diff_excerpt}

Format: type(scope): description

Types: feat, fix, docs, style, refactor, perf, test, build, ci, chore
Keep under 72 characters. Be specific and concise. No period at the end.

Example outputs:
- feat(auth): add OAuth2 login support
- fix(api): resolve null pointer in user endpoint
- docs(readme): update installation instructions

Output ONLY the commit message (no explanations, no quotes, no preamble):"""

        return prompt

    def _generate_ollama(self, diff: str, files: list[str]) -> str:
        """Generate using Ollama."""
        try:
            host = self.config.get("ai", "ollama_host", "http://localhost:11434")
            model = self.config.ai_model

            prompt = self._create_prompt(diff, files)

            response = requests.post(
                f"{host}/api/generate",
                json={"model": model, "prompt": prompt, "stream": False},
                timeout=30,
            )
            response.raise_for_status()

            message = response.json()["response"].strip()
            return self._clean_message(message)

        except Exception as e:
            print(f"Warning: Ollama generation failed: {e}")
            return self._generate_fallback(diff, files)

    def _generate_openai(self, diff: str, files: list[str]) -> str:
        """Generate using OpenAI."""
        try:
            import openai

            api_key = self.config.get("ai", "openai_api_key")
            if not api_key:
                return self._generate_fallback(diff, files)

            client = openai.OpenAI(api_key=api_key)
            prompt = self._create_prompt(diff, files)

            response = client.chat.completions.create(
                model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}], max_tokens=100
            )

            message = response.choices[0].message.content.strip()
            return self._clean_message(message)

        except Exception as e:
            print(f"Warning: OpenAI generation failed: {e}")
            return self._generate_fallback(diff, files)

    def _generate_anthropic(self, diff: str, files: list[str]) -> str:
        """Generate using Anthropic."""
        try:
            import anthropic

            api_key = self.config.get("ai", "anthropic_api_key")
            if not api_key:
                return self._generate_fallback(diff, files)

            client = anthropic.Anthropic(api_key=api_key)
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

    def _clean_message(self, message: str) -> str:
        """Clean and validate commit message."""
        # Remove any markdown formatting
        message = re.sub(r"```.*?```", "", message, flags=re.DOTALL)
        message = re.sub(r"`([^`]+)`", r"\1", message)

        # Extract first line if multi-line
        message = message.split("\n")[0].strip()

        # Remove quotes
        message = message.strip('"\'')

        # Remove common AI preambles
        preambles = [
            r"^Here is a (concise )?git commit message( for these changes)?:\s*",
            r"^Here's a (concise )?git commit message( for these changes)?:\s*",
            r"^Commit message:\s*",
            r"^The commit message is:\s*",
            r"^Output:\s*",
            r"^-\s*",  # Remove leading dash from bullet points
        ]
        for preamble in preambles:
            message = re.sub(preamble, "", message, flags=re.IGNORECASE)

        message = message.strip()

        # Fix common AI mistakes: "fix/docs:" -> "docs:"
        message = re.sub(r"^(?:feat|fix|docs|style|refactor|perf|test|build|ci|chore)/", "", message)

        # Ensure conventional commit format
        if not re.match(r"^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)", message):
            message = f"chore: {message}"

        # Limit length
        if len(message) > 72:
            message = message[:69] + "..."

        return message

    def add_emoji(self, message: str) -> str:
        """Add emoji to commit message."""
        if self.config.get("quick", "emoji_style") != "gitmoji":
            return message

        # Extract type
        match = re.match(r"^(\w+)(\([^)]+\))?:\s*(.+)$", message)
        if match:
            commit_type = match.group(1)
            scope = match.group(2) or ""
            description = match.group(3)
            emoji = self.config.get_gitmoji(commit_type)
            return f"{emoji} {commit_type}{scope}: {description}"

        return message

    def parse_type_scope(self, message: str) -> Tuple[Optional[str], Optional[str]]:
        """Parse commit type and scope from message."""
        match = re.match(r"^(\w+)(?:\(([^)]+)\))?:\s*(.+)$", message)
        if match:
            return match.group(1), match.group(2)
        return None, None
