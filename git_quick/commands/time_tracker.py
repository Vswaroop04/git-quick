"""Time tracking for Git branches."""

import json
import time
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime, timedelta

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from git_quick.config import get_config

console = Console()


class TimeTracker:
    """Track time spent on branches."""

    def __init__(self):
        config = get_config()
        data_dir = config.get("time", "data_dir", "~/.gitquick/time")
        self.data_dir = Path(data_dir).expanduser()
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.data_file = self.data_dir / "time_data.json"
        self.data = self._load_data()

    def _load_data(self) -> Dict:
        """Load time tracking data."""
        if self.data_file.exists():
            try:
                with open(self.data_file) as f:
                    return json.load(f)
            except Exception:
                return {"branches": {}, "sessions": []}
        return {"branches": {}, "sessions": []}

    def _save_data(self):
        """Save time tracking data."""
        with open(self.data_file, "w") as f:
            json.dump(self.data, f, indent=2)

    def start_tracking(self, branch: str):
        """Start tracking time for a branch."""
        if branch not in self.data["branches"]:
            self.data["branches"][branch] = {"total_seconds": 0, "start_time": None, "sessions": []}

        # Start new session
        self.data["branches"][branch]["start_time"] = time.time()
        self._save_data()

    def stop_tracking(self, branch: str) -> Optional[float]:
        """Stop tracking time for a branch."""
        if branch not in self.data["branches"]:
            return None

        branch_data = self.data["branches"][branch]
        start_time = branch_data.get("start_time")

        if start_time is None:
            return None

        # Calculate duration
        duration = time.time() - start_time

        # Update total
        branch_data["total_seconds"] += duration
        branch_data["start_time"] = None

        # Add session
        branch_data["sessions"].append(
            {"start": start_time, "end": time.time(), "duration": duration}
        )

        self._save_data()
        return duration

    def get_branch_time(self, branch: str) -> float:
        """Get total time spent on a branch."""
        if branch not in self.data["branches"]:
            return 0

        total = self.data["branches"][branch]["total_seconds"]

        # Add current session if active
        start_time = self.data["branches"][branch].get("start_time")
        if start_time:
            total += time.time() - start_time

        return total

    def show_report(self, branch: str):
        """Show time report for a branch."""
        if branch not in self.data["branches"]:
            console.print(f"[yellow]No time tracking data for branch: {branch}[/yellow]")
            return

        total_seconds = self.get_branch_time(branch)
        branch_data = self.data["branches"][branch]

        # Format time
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)

        # Create report
        console.print(
            Panel(
                f"[bold]Branch:[/bold] {branch}\n"
                f"[bold]Total time:[/bold] {hours}h {minutes}m\n"
                f"[bold]Sessions:[/bold] {len(branch_data['sessions'])}",
                title="⏱️  Time Report",
                border_style="cyan",
            )
        )

        # Show recent sessions
        if branch_data["sessions"]:
            table = Table(title="Recent Sessions")
            table.add_column("Start", style="cyan")
            table.add_column("End", style="cyan")
            table.add_column("Duration", style="green")

            # Show last 10 sessions
            for session in branch_data["sessions"][-10:]:
                start_dt = datetime.fromtimestamp(session["start"])
                end_dt = datetime.fromtimestamp(session["end"])
                duration = timedelta(seconds=int(session["duration"]))

                table.add_row(
                    start_dt.strftime("%Y-%m-%d %H:%M"),
                    end_dt.strftime("%H:%M"),
                    str(duration),
                )

            console.print(table)

    def show_all_reports(self):
        """Show time reports for all branches."""
        if not self.data["branches"]:
            console.print("[yellow]No time tracking data[/yellow]")
            return

        table = Table(title="⏱️  Time Tracking Report")
        table.add_column("Branch", style="cyan")
        table.add_column("Total Time", style="green")
        table.add_column("Sessions", style="yellow")
        table.add_column("Status", style="magenta")

        for branch, data in sorted(
            self.data["branches"].items(), key=lambda x: x[1]["total_seconds"], reverse=True
        ):
            total_seconds = self.get_branch_time(branch)
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)

            status = "🟢 Active" if data.get("start_time") else "⚪ Stopped"

            table.add_row(
                branch, f"{hours}h {minutes}m", str(len(data["sessions"])), status
            )

        console.print(table)

    def auto_track(self, git):
        """Automatically track time based on branch switches."""
        # This would be called by a git hook
        current_branch = git.current_branch

        # Stop tracking on old branches
        for branch, data in self.data["branches"].items():
            if branch != current_branch and data.get("start_time"):
                self.stop_tracking(branch)

        # Start tracking on current branch
        if current_branch:
            self.start_tracking(current_branch)
