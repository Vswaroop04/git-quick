"""Git story command implementation."""

from datetime import datetime
from typing import List, Optional
from collections import defaultdict
import re

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from git_quick.git_utils import GitUtils
from git_quick.config import get_config

console = Console()


def parse_conventional_commit(message: str) -> tuple[str, str, str]:
    """Parse conventional commit message."""
    match = re.match(r"^(\w+)(?:\(([^)]+)\))?:\s*(.+)$", message)
    if match:
        return match.group(1), match.group(2) or "", match.group(3)
    return "other", "", message


def get_type_color(commit_type: str) -> str:
    """Get color for commit type."""
    colors = {
        "feat": "green",
        "fix": "red",
        "docs": "blue",
        "style": "magenta",
        "refactor": "yellow",
        "perf": "cyan",
        "test": "white",
        "build": "bright_black",
        "ci": "bright_black",
        "chore": "bright_black",
    }
    return colors.get(commit_type, "white")


def show_story(
    git: GitUtils,
    since: Optional[str] = None,
    group_by: Optional[str] = None,
    output_format: str = "console",
    max_commits: Optional[int] = None,
):
    """Show commit story."""
    config = get_config()

    # Get commits
    commits = git.get_commits_since_tag(since)

    # Apply max limit
    max_commits = max_commits or config.get("story", "max_commits", 50)
    commits = commits[:max_commits]

    if not commits:
        console.print("[yellow]No commits found[/yellow]")
        return

    # Get grouping preference
    group_by = group_by or config.get("story", "group_by", "date")

    if output_format == "markdown":
        _show_story_markdown(commits, group_by)
    else:
        _show_story_console(commits, group_by)


def _show_story_console(commits: list, group_by: str):
    """Show story in console format."""
    console.print(
        Panel(
            f"[bold]📖 Commit Story[/bold]\n{len(commits)} commits",
            border_style="blue",
        )
    )

    if group_by == "type":
        _show_grouped_by_type(commits)
    elif group_by == "author":
        _show_grouped_by_author(commits)
    else:
        _show_grouped_by_date(commits)


def _show_grouped_by_type(commits: list):
    """Show commits grouped by type."""
    grouped = defaultdict(list)

    for commit in commits:
        message = commit.message.split("\n")[0]
        commit_type, scope, description = parse_conventional_commit(message)
        grouped[commit_type].append((commit, scope, description))

    for commit_type in sorted(grouped.keys()):
        color = get_type_color(commit_type)
        console.print(f"\n[bold {color}]{commit_type.upper()}[/bold {color}]")

        for commit, scope, description in grouped[commit_type]:
            scope_str = f"({scope})" if scope else ""
            console.print(
                f"  • {commit.hexsha[:7]} {scope_str} {description}",
                style=color,
            )


def _show_grouped_by_author(commits: list):
    """Show commits grouped by author."""
    grouped = defaultdict(list)

    for commit in commits:
        author = commit.author.name
        grouped[author].append(commit)

    for author in sorted(grouped.keys()):
        console.print(f"\n[bold cyan]{author}[/bold cyan]")

        for commit in grouped[author]:
            message = commit.message.split("\n")[0]
            commit_type, scope, description = parse_conventional_commit(message)
            color = get_type_color(commit_type)

            scope_str = f"({scope})" if scope else ""
            console.print(
                f"  • {commit.hexsha[:7]} [{color}]{commit_type}[/{color}] {scope_str} {description}"
            )


def _show_grouped_by_date(commits: list):
    """Show commits grouped by date."""
    grouped = defaultdict(list)

    for commit in commits:
        date = datetime.fromtimestamp(commit.committed_date).strftime("%Y-%m-%d")
        grouped[date].append(commit)

    for date in sorted(grouped.keys(), reverse=True):
        console.print(f"\n[bold]{date}[/bold]")

        for commit in grouped[date]:
            message = commit.message.split("\n")[0]
            commit_type, scope, description = parse_conventional_commit(message)
            color = get_type_color(commit_type)

            scope_str = f"({scope})" if scope else ""
            time_str = datetime.fromtimestamp(commit.committed_date).strftime("%H:%M")
            console.print(
                f"  • {time_str} {commit.hexsha[:7]} [{color}]{commit_type}[/{color}] {scope_str} {description}"
            )


def _show_story_markdown(commits: list, group_by: str):
    """Show story in markdown format."""
    print("# Changelog\n")

    if group_by == "type":
        grouped = defaultdict(list)
        for commit in commits:
            message = commit.message.split("\n")[0]
            commit_type, scope, description = parse_conventional_commit(message)
            grouped[commit_type].append((commit, scope, description))

        for commit_type in sorted(grouped.keys()):
            print(f"\n## {commit_type.capitalize()}\n")
            for commit, scope, description in grouped[commit_type]:
                scope_str = f"**{scope}**: " if scope else ""
                print(f"- {scope_str}{description} ({commit.hexsha[:7]})")

    else:
        for commit in commits:
            message = commit.message.split("\n")[0]
            commit_type, scope, description = parse_conventional_commit(message)
            scope_str = f"**{scope}**: " if scope else ""
            print(f"- {scope_str}{description} ({commit.hexsha[:7]})")
