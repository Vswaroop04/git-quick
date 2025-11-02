"""Tests for configuration management."""

import tempfile
from pathlib import Path
import pytest
from git_quick.config import Config, GITMOJI_MAP


def test_default_config():
    """Test default configuration."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "test_config.toml"
        config = Config(config_path)

        assert config.get("quick", "auto_push") is True
        assert config.get("quick", "emoji_style") == "gitmoji"
        assert config.get("quick", "ai_provider") == "ollama"


def test_config_save_load():
    """Test saving and loading configuration."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "test_config.toml"
        config = Config(config_path)

        # Set some values
        config.set("quick", "auto_push", False)
        config.set("quick", "ai_model", "gpt-4")
        config.save()

        # Load again
        config2 = Config(config_path)
        assert config2.get("quick", "auto_push") is False
        assert config2.get("quick", "ai_model") == "gpt-4"


def test_gitmoji_map():
    """Test gitmoji mappings."""
    config = Config(Path("/tmp/nonexistent"))

    assert config.get_gitmoji("feat") == "✨"
    assert config.get_gitmoji("fix") == "🐛"
    assert config.get_gitmoji("docs") == "📝"
    assert config.get_gitmoji("unknown") == "📦"


def test_merge_config():
    """Test merging user config with defaults."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "test_config.toml"
        config = Config(config_path)

        # Merge new config
        user_config = {"quick": {"auto_push": False, "new_key": "value"}}
        config._merge_config(user_config)

        assert config.get("quick", "auto_push") is False
        assert config.get("quick", "new_key") == "value"
        # Default values should still be there
        assert config.get("quick", "emoji_style") == "gitmoji"
