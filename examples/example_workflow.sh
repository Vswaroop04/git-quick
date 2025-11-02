#!/bin/bash
# Example workflow using git-quick

set -e

echo "=== Git Quick Example Workflow ==="
echo ""

# 1. Start time tracking
echo "1. Starting time tracking for current branch..."
git-time start
echo ""

# 2. Make some changes
echo "2. Making changes to files..."
echo "# Example change" >> example.txt
echo ""

# 3. Quick commit with AI message
echo "3. Quick commit with AI-generated message..."
git-quick --dry-run  # Dry run first
echo ""

# 4. Show commit story
echo "4. Showing commit story..."
git-story --max 5
echo ""

# 5. Show time report
echo "5. Time report for current branch..."
git-time report
echo ""

# 6. Sync all branches
echo "6. Syncing all branches..."
git-sync-all --dry-run
echo ""

echo "=== Workflow complete! ==="
echo ""
echo "Tips:"
echo "  - Remove --dry-run flags to actually execute"
echo "  - Set up AI provider for better commit messages"
echo "  - Use git-quick aliases for faster workflow"
