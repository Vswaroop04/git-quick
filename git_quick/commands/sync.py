"""Sync all branches command implementation."""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from git_quick.git_utils import GitUtils
from git_quick.config import get_config

console = Console()


def sync_all_branches(git: GitUtils, dry_run: bool = False, prune: bool = True):
    """Sync all local branches with remote."""
    config = get_config()
    current_branch = git.current_branch

    console.print(
        Panel(
            "[bold]🔄 Syncing all branches[/bold]",
            border_style="blue",
        )
    )

    # Stash changes if needed
    stashed = False
    if git.has_changes():
        console.print("[yellow]Stashing uncommitted changes...[/yellow]")
        if not dry_run:
            stashed = git.stash()
        console.print("[green]✓[/green] Changes stashed")

    # Fetch all remotes
    console.print("\n[bold]📥 Fetching from remote...[/bold]")
    if not dry_run:
        git.repo.git.fetch("--all", "--prune" if prune else None)
    console.print("[green]✓[/green] Fetched latest changes")

    # Get all branches
    branches = git.get_all_branches()
    console.print(f"\n[bold]Found {len(branches)} local branches[/bold]\n")

    # Track results
    results = {"updated": [], "up_to_date": [], "failed": [], "no_tracking": []}

    # Update each branch
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Syncing branches...", total=len(branches))

        for branch in branches:
            progress.update(task, description=f"Syncing {branch}...")

            # Check if branch has tracking branch
            tracking = git.get_tracking_branch(branch)
            if not tracking:
                results["no_tracking"].append(branch)
                progress.advance(task)
                continue

            try:
                # Check if branch is behind
                if not dry_run:
                    git.checkout(branch)

                is_behind = git.is_branch_behind(branch)

                if is_behind:
                    if not dry_run:
                        # Try to fast-forward
                        try:
                            git.pull(branch)
                            results["updated"].append(branch)
                        except Exception as e:
                            results["failed"].append((branch, str(e)))
                    else:
                        results["updated"].append(branch)
                else:
                    results["up_to_date"].append(branch)

            except Exception as e:
                results["failed"].append((branch, str(e)))

            progress.advance(task)

    # Return to original branch
    if not dry_run and current_branch != git.current_branch:
        git.checkout(current_branch)

    # Restore stashed changes
    if stashed and not dry_run:
        console.print("\n[yellow]Restoring stashed changes...[/yellow]")
        git.stash_pop()
        console.print("[green]✓[/green] Changes restored")

    # Show results
    console.print("\n[bold]📊 Results:[/bold]\n")

    table = Table()
    table.add_column("Status", style="bold")
    table.add_column("Count", style="cyan")
    table.add_column("Branches", style="white")

    if results["updated"]:
        table.add_row(
            "✅ Updated",
            str(len(results["updated"])),
            ", ".join(results["updated"][:5])
            + (f" and {len(results['updated']) - 5} more" if len(results["updated"]) > 5 else ""),
        )

    if results["up_to_date"]:
        table.add_row(
            "✓ Up to date",
            str(len(results["up_to_date"])),
            ", ".join(results["up_to_date"][:5])
            + (
                f" and {len(results['up_to_date']) - 5} more"
                if len(results["up_to_date"]) > 5
                else ""
            ),
        )

    if results["no_tracking"]:
        table.add_row(
            "⚠️  No tracking",
            str(len(results["no_tracking"])),
            ", ".join(results["no_tracking"][:5])
            + (
                f" and {len(results['no_tracking']) - 5} more"
                if len(results["no_tracking"]) > 5
                else ""
            ),
        )

    if results["failed"]:
        table.add_row(
            "❌ Failed",
            str(len(results["failed"])),
            ", ".join([b for b, _ in results["failed"][:3]]),
        )

    console.print(table)

    # Show failures in detail
    if results["failed"]:
        console.print("\n[bold red]Failed branches:[/bold red]")
        for branch, error in results["failed"]:
            console.print(f"  • {branch}: {error}")

    if dry_run:
        console.print("\n[yellow]This was a dry run. No changes were made.[/yellow]")
    else:
        console.print("\n[bold green]✨ Sync complete![/bold green]")
