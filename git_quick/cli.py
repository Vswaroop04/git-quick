"""Main CLI interface for Git Quick."""

import sys
import click
from rich.console import Console
from rich.prompt import Confirm, Prompt
from rich.panel import Panel

from git_quick.config import get_config
from git_quick.git_utils import GitUtils
from git_quick.ai_commit import AICommitGenerator
from git_quick.commands.story import show_story
from git_quick.commands.time_tracker import TimeTracker
from git_quick.commands.sync import sync_all_branches
from git_quick.setup_wizard import run_setup_wizard, prompt_setup_if_needed

console = Console()


class DefaultGroup(click.Group):
    """A Click group that uses a default command when no subcommand is given."""

    def __init__(self, *args, **kwargs):
        self.default_cmd_name = kwargs.pop('default_command', None)
        super().__init__(*args, **kwargs)

    def parse_args(self, ctx, args):
        # If no args or only options (not subcommands), use default command
        # But skip this if it's a global option like --version, --help, or --setup
        if not args or (args and args[0].startswith('-') and args[0] not in ['--version', '--help', '-h', '--setup']):
            args.insert(0, self.default_cmd_name or 'commit')
        return super().parse_args(ctx, args)


def setup_callback(ctx, param, value):
    """Callback to handle --setup flag."""
    if value:
        run_setup_wizard()
        ctx.exit(0)


@click.group(cls=DefaultGroup, default_command='commit')
@click.version_option(version="1.1.1", prog_name="gq")
@click.option('--setup', is_flag=True, is_eager=True, expose_value=False,
              callback=setup_callback, help='Run the setup wizard')
def cli():
    """Lightning-fast Git workflows with AI-powered commit messages.

    \b
    Commands:
      gq              Quick commit and push (default)
      gq story        Show commit history
      gq time         Time tracking commands
      gq sync         Sync all branches

    \b
    Examples:
      gq                    # Quick commit & push
      gq story              # Show commits
      gq time start         # Track time
      gq sync               # Sync branches
      gq --setup            # Run setup wizard
    """
    pass


@cli.command(name="commit")
@click.option("--message", "-m", help="Commit message (skip AI generation)")
@click.option("--no-push", is_flag=True, help="Don't push after commit")
@click.option("--no-ai", is_flag=True, help="Use fallback message generation")
@click.option("--emoji/--no-emoji", default=True, help="Add emoji to commit message")
@click.option("--dry-run", is_flag=True, help="Show what would be done without doing it")
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation prompts")
def commit_cmd(message, no_push, no_ai, emoji, dry_run, yes):
    """Quick commit and push with AI-generated message.

    This is the default command when you run 'gq' without subcommands.
    Combines git add, commit, and push with smart defaults.
    """
    try:
        # Run setup wizard on first use
        prompt_setup_if_needed()
        
        config = get_config()
        git = GitUtils()

        # Check if there are changes
        if not git.has_changes():
            console.print("[yellow]No changes to commit[/yellow]")
            return

        # Show status
        console.print("\n[bold]📋 Current status:[/bold]")
        console.print(git.get_status())

        # Stage all changes
        console.print("\n[bold]📦 Staging all changes...[/bold]")
        if not dry_run:
            git.stage_all()

        # Get files changed
        files = git.get_files_changed()
        console.print(f"[green]✓[/green] Staged {len(files)} file(s)")

        # Generate or use provided message
        if message:
            commit_msg = message
        else:
            console.print("\n[bold]🤖 Generating commit message...[/bold]")
            diff = git.get_diff(staged=True)

            if no_ai:
                ai_gen = AICommitGenerator()
                commit_msg = ai_gen._generate_fallback(diff, files)
            else:
                ai_gen = AICommitGenerator()
                commit_msg = ai_gen.generate(diff, files)

            # Add emoji if enabled
            if emoji:
                commit_msg = ai_gen.add_emoji(commit_msg)

            # Show generated message
            console.print(
                Panel(commit_msg, title="[bold]Generated Message[/bold]", border_style="green")
            )

            # Ask for confirmation (only if interactive)
            if not yes and sys.stdin.isatty():
                if not Confirm.ask("\nUse this message?", default=True):
                    commit_msg = Prompt.ask("Enter commit message")
            elif not yes:
                console.print("[yellow]Non-interactive mode: using generated message[/yellow]")

        # Commit
        console.print(f"\n[bold]💾 Committing...[/bold]")
        if not dry_run:
            commit_hash = git.commit(commit_msg)
            console.print(f"[green]✓[/green] Committed: {commit_hash}")
        else:
            console.print(f"[yellow]Would commit with message:[/yellow] {commit_msg}")

        # Push
        should_push = config.get("quick", "auto_push", True) and not no_push
        if should_push:
            branch = git.current_branch
            console.print(f"\n[bold]🚀 Pushing to {branch}...[/bold]")

            if not dry_run:
                try:
                    git.push(branch)
                    console.print(f"[green]✓[/green] Pushed to origin/{branch}")
                except Exception as e:
                    console.print(f"[red]✗[/red] Push failed: {e}")
                    console.print("[yellow]Run 'git push' manually to push changes[/yellow]")
            else:
                console.print(f"[yellow]Would push to origin/{branch}[/yellow]")

        console.print("\n[bold green]✨ Done![/bold green]")

    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        console.print("\n[yellow]Aborted[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected error:[/red] {e}")
        sys.exit(1)


@cli.command()
@click.option("--since", "-s", help="Show commits since tag/commit (default: last release)")
@click.option("--group-by", "-g", type=click.Choice(["date", "author", "type"]), help="Group commits by")
@click.option("--format", "-f", type=click.Choice(["console", "markdown"]), default="console", help="Output format")
@click.option("--max", "-n", type=int, help="Maximum number of commits to show")
def story(since, group_by, format, max):
    """Show compact, colorized commit summary.

    Displays commits since last release with grouping and formatting options.

    \b
    Examples:
      gq story
      gq story --group-by type
      gq story --format markdown > CHANGELOG.md
    """
    try:
        git = GitUtils()
        show_story(git, since=since, group_by=group_by, output_format=format, max_commits=max)

    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        console.print("\n[yellow]Aborted[/yellow]")
        sys.exit(1)


@cli.group()
def time():
    """Track development time per branch/feature.

    \b
    Examples:
      gq time start         # Start tracking
      gq time stop          # Stop tracking
      gq time report        # Show report
      gq time report --all  # All branches
    """
    pass


@time.command()
@click.option("--branch", "-b", help="Branch to track (default: current)")
def start(branch):
    """Start tracking time for current branch."""
    try:
        git = GitUtils()
        tracker = TimeTracker()
        branch = branch or git.current_branch

        tracker.start_tracking(branch)
        console.print(f"[green]✓[/green] Started tracking time for branch: [bold]{branch}[/bold]")

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@time.command()
@click.option("--branch", "-b", help="Branch to stop (default: current)")
def stop(branch):
    """Stop tracking time for current branch."""
    try:
        git = GitUtils()
        tracker = TimeTracker()
        branch = branch or git.current_branch

        duration = tracker.stop_tracking(branch)
        if duration:
            hours = int(duration // 3600)
            minutes = int((duration % 3600) // 60)
            console.print(
                f"[green]✓[/green] Stopped tracking. Time spent: {hours}h {minutes}m"
            )
        else:
            console.print("[yellow]No active tracking session[/yellow]")

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@time.command()
@click.option("--branch", "-b", help="Show report for specific branch")
@click.option("--all", "-a", is_flag=True, help="Show report for all branches")
def report(branch, all):
    """Show time tracking report."""
    try:
        git = GitUtils()
        tracker = TimeTracker()

        if all:
            tracker.show_all_reports()
        else:
            branch = branch or git.current_branch
            tracker.show_report(branch)

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@cli.command()
@click.option("--dry-run", is_flag=True, help="Show what would be done without doing it")
@click.option("--prune", is_flag=True, default=True, help="Prune deleted remote branches")
def sync(dry_run, prune):
    """Update all local branches from remote.

    Safely fast-forward all local branches that track a remote branch.

    \b
    Examples:
      gq sync              # Sync all branches
      gq sync --dry-run    # Preview changes
    """
    try:
        git = GitUtils()
        sync_all_branches(git, dry_run=dry_run, prune=prune)

    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        console.print("\n[yellow]Aborted[/yellow]")
        sys.exit(1)


# For backward compatibility, keep old entry points
def quick():
    """Entry point for git-quick (commit command)."""
    sys.argv.insert(1, "commit")
    cli()


def story_cmd():
    """Entry point for git-story."""
    sys.argv.insert(1, "story")
    cli()


def time_track():
    """Entry point for git-time."""
    sys.argv.insert(1, "time")
    cli()


def sync_all():
    """Entry point for git-sync-all."""
    sys.argv.insert(1, "sync")
    cli()


if __name__ == "__main__":
    cli()
