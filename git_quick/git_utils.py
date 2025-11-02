"""Git utility functions."""

import subprocess
from pathlib import Path
from typing import List, Optional, Tuple
import git
from git import Repo, GitCommandError


class GitUtils:
    """Git utility class."""

    def __init__(self, repo_path: Optional[Path] = None):
        self.repo_path = repo_path or Path.cwd()
        try:
            self.repo = Repo(self.repo_path, search_parent_directories=True)
        except git.InvalidGitRepositoryError:
            raise ValueError(f"Not a git repository: {self.repo_path}")

    @property
    def current_branch(self) -> str:
        """Get current branch name."""
        return self.repo.active_branch.name

    @property
    def remote(self) -> str:
        """Get remote name."""
        return "origin"

    def has_changes(self) -> bool:
        """Check if there are uncommitted changes."""
        return self.repo.is_dirty() or len(self.repo.untracked_files) > 0

    def get_diff(self, staged: bool = False) -> str:
        """Get diff of changes."""
        if staged:
            return self.repo.git.diff("--cached")
        return self.repo.git.diff("HEAD")

    def get_status(self) -> str:
        """Get git status."""
        return self.repo.git.status("--short")

    def stage_all(self) -> None:
        """Stage all changes."""
        self.repo.git.add("-A")

    def commit(self, message: str) -> str:
        """Create a commit."""
        commit = self.repo.index.commit(message)
        return commit.hexsha[:7]

    def push(self, branch: Optional[str] = None, force: bool = False) -> None:
        """Push to remote."""
        branch = branch or self.current_branch
        args = ["--force"] if force else []
        self.repo.git.push(self.remote, branch, *args)

    def get_commits_since_tag(self, tag: Optional[str] = None) -> List[git.Commit]:
        """Get commits since a tag."""
        if tag is None:
            tags = sorted(self.repo.tags, key=lambda t: t.commit.committed_datetime, reverse=True)
            if not tags:
                # No tags, get all commits
                return list(self.repo.iter_commits(self.current_branch))
            tag = tags[0].name

        try:
            return list(self.repo.iter_commits(f"{tag}..{self.current_branch}"))
        except GitCommandError:
            return list(self.repo.iter_commits(self.current_branch))

    def get_all_branches(self) -> List[str]:
        """Get all local branch names."""
        return [branch.name for branch in self.repo.branches]

    def get_remote_branches(self) -> List[str]:
        """Get all remote branch names."""
        self.repo.git.fetch("--all")
        remote_refs = self.repo.remote().refs
        return [ref.remote_head for ref in remote_refs if ref.remote_head != "HEAD"]

    def checkout(self, branch: str) -> None:
        """Checkout a branch."""
        self.repo.git.checkout(branch)

    def pull(self, branch: Optional[str] = None) -> None:
        """Pull from remote."""
        branch = branch or self.current_branch
        self.repo.git.pull(self.remote, branch)

    def stash(self) -> bool:
        """Stash changes. Returns True if anything was stashed."""
        if self.has_changes():
            self.repo.git.stash("push", "-u")
            return True
        return False

    def stash_pop(self) -> None:
        """Pop stashed changes."""
        try:
            self.repo.git.stash("pop")
        except GitCommandError:
            pass  # No stash to pop

    def get_last_commit_message(self) -> str:
        """Get the last commit message."""
        return self.repo.head.commit.message.strip()

    def get_files_changed(self) -> List[str]:
        """Get list of changed files."""
        status = self.repo.git.status("--porcelain")
        files = []
        for line in status.split("\n"):
            if line.strip():
                # Format: "XY filename"
                files.append(line[3:].strip())
        return files

    def get_commit_stats(self, commit: git.Commit) -> Tuple[int, int]:
        """Get additions and deletions for a commit."""
        stats = commit.stats.total
        return stats.get("insertions", 0), stats.get("deletions", 0)

    def is_branch_ahead(self, branch: str) -> bool:
        """Check if local branch is ahead of remote."""
        try:
            local = self.repo.commit(branch)
            remote = self.repo.commit(f"{self.remote}/{branch}")
            return local != remote
        except (GitCommandError, ValueError):
            return False

    def is_branch_behind(self, branch: str) -> bool:
        """Check if local branch is behind remote."""
        try:
            local = self.repo.commit(branch)
            remote = self.repo.commit(f"{self.remote}/{branch}")
            # Check if remote is ahead
            return self.repo.is_ancestor(local, remote) and local != remote
        except (GitCommandError, ValueError):
            return False

    def get_tracking_branch(self, branch: str) -> Optional[str]:
        """Get the tracking branch for a local branch."""
        try:
            branch_obj = self.repo.branches[branch]
            tracking = branch_obj.tracking_branch()
            return tracking.name if tracking else None
        except (IndexError, AttributeError):
            return None
