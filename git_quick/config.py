"""Configuration management for Git Quick."""

import os
from pathlib import Path
from typing import Any, Dict, Optional
import toml


DEFAULT_CONFIG = {
    "quick": {
        "auto_push": True,
        "emoji_style": "gitmoji",
        "ai_provider": "ollama",
        "ai_model": "llama3",
        "conventional_commits": True,
    },
    "story": {
        "default_range": "last-release",
        "color_scheme": "dark",
        "group_by": "date",
        "max_commits": 50,
    },
    "time": {
        "auto_track": True,
        "idle_threshold": 300,
        "data_dir": "~/.gitquick/time",
    },
    "sync": {
        "auto_stash": True,
        "prune": True,
        "fetch_all": True,
    },
    "ai": {
        "openai_api_key": "",
        "anthropic_api_key": "",
        "ollama_host": "http://localhost:11434",
    },
    "setup": {
        "completed": False,
    },
}

# Gitmoji mappings
GITMOJI_MAP = {
    "feat": "✨",
    "fix": "🐛",
    "docs": "📝",
    "style": "💄",
    "refactor": "♻️",
    "perf": "⚡",
    "test": "✅",
    "build": "👷",
    "ci": "💚",
    "chore": "🔧",
    "revert": "⏪",
    "wip": "🚧",
    "init": "🎉",
    "security": "🔒",
    "deps": "⬆️",
}


class Config:
    """Configuration manager."""

    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or Path.home() / ".gitquick.toml"
        self._config: Dict[str, Any] = DEFAULT_CONFIG.copy()
        self.load()

    def load(self) -> None:
        """Load configuration from file."""
        if self.config_path.exists():
            try:
                user_config = toml.load(self.config_path)
                self._merge_config(user_config)
            except Exception as e:
                print(f"Warning: Could not load config: {e}")

    def _merge_config(self, user_config: Dict[str, Any]) -> None:
        """Merge user config with defaults."""
        for section, values in user_config.items():
            if section in self._config:
                self._config[section].update(values)
            else:
                self._config[section] = values

    def get(self, section: str, key: str, default: Any = None) -> Any:
        """Get configuration value with environment variable override support."""
        # Check for environment variable override
        env_key = f"GITQUICK_{key.upper()}"
        env_value = os.getenv(env_key)
        if env_value is not None:
            return env_value
        
        return self._config.get(section, {}).get(key, default)

    def set(self, section: str, key: str, value: Any) -> None:
        """Set configuration value."""
        if section not in self._config:
            self._config[section] = {}
        self._config[section][key] = value

    def save(self) -> None:
        """Save configuration to file."""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, "w") as f:
            toml.dump(self._config, f)

    def create_default(self) -> None:
        """Create default configuration file."""
        self.save()

    @property
    def ai_provider(self) -> str:
        """Get AI provider."""
        return self.get("quick", "ai_provider", "ollama")

    @property
    def ai_model(self) -> str:
        """Get AI model."""
        return self.get("quick", "ai_model", "llama3")

    def get_gitmoji(self, commit_type: str) -> str:
        """Get emoji for commit type."""
        return GITMOJI_MAP.get(commit_type, "📦")


# Global config instance
_config: Optional[Config] = None


def get_config() -> Config:
    """Get global config instance."""
    global _config
    if _config is None:
        _config = Config()
    return _config
