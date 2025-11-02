"""Tests for AI commit message generation."""

import pytest
from git_quick.ai_commit import AICommitGenerator


def test_clean_message():
    """Test message cleaning."""
    ai_gen = AICommitGenerator()

    # Test removing markdown
    assert "feat: add feature" == ai_gen._clean_message("```feat: add feature```")

    # Test removing quotes
    assert "fix: bug fix" == ai_gen._clean_message('"fix: bug fix"')

    # Test adding prefix
    assert ai_gen._clean_message("add new file").startswith("chore:")

    # Test length limiting
    long_msg = "feat: " + "a" * 100
    cleaned = ai_gen._clean_message(long_msg)
    assert len(cleaned) <= 72


def test_parse_type_scope():
    """Test parsing commit type and scope."""
    ai_gen = AICommitGenerator()

    # Test with scope
    commit_type, scope = ai_gen.parse_type_scope("feat(auth): add login")
    assert commit_type == "feat"
    assert scope == "auth"

    # Test without scope
    commit_type, scope = ai_gen.parse_type_scope("fix: bug fix")
    assert commit_type == "fix"
    assert scope is None

    # Test invalid format
    commit_type, scope = ai_gen.parse_type_scope("invalid message")
    assert commit_type is None
    assert scope is None


def test_add_emoji():
    """Test adding emoji to commit message."""
    ai_gen = AICommitGenerator()

    message = "feat: add feature"
    with_emoji = ai_gen.add_emoji(message)
    assert "✨" in with_emoji

    message = "fix: bug fix"
    with_emoji = ai_gen.add_emoji(message)
    assert "🐛" in with_emoji


def test_fallback_generation():
    """Test fallback message generation."""
    ai_gen = AICommitGenerator()

    # Test with test files
    message = ai_gen._generate_fallback("", ["test_file.py"])
    assert "test" in message.lower()

    # Test with markdown files
    message = ai_gen._generate_fallback("", ["README.md"])
    assert "docs" in message.lower()

    # Test with config files
    message = ai_gen._generate_fallback("", ["config.json"])
    assert "chore" in message.lower()
