#!/bin/bash
# Version bumping script for git-quick
# Usage: ./scripts/bump-version.sh [major|minor|patch|VERSION]

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get current version from pyproject.toml
get_current_version() {
    python3 -c "import tomllib; f = open('pyproject.toml', 'rb'); data = tomllib.load(f); print(data['project']['version'])"
}

# Calculate new version
calculate_new_version() {
    local current=$1
    local bump_type=$2

    IFS='.' read -r MAJOR MINOR PATCH <<< "$current"

    case $bump_type in
        major)
            MAJOR=$((MAJOR + 1))
            MINOR=0
            PATCH=0
            ;;
        minor)
            MINOR=$((MINOR + 1))
            PATCH=0
            ;;
        patch)
            PATCH=$((PATCH + 1))
            ;;
        *)
            echo "$bump_type"
            return
            ;;
    esac

    echo "${MAJOR}.${MINOR}.${PATCH}"
}

# Update version in files
update_version() {
    local old_version=$1
    local new_version=$2

    echo -e "${BLUE}Updating version from ${old_version} to ${new_version}${NC}"

    # Update pyproject.toml
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s/version = \"${old_version}\"/version = \"${new_version}\"/" pyproject.toml
    else
        sed -i "s/version = \"${old_version}\"/version = \"${new_version}\"/" pyproject.toml
    fi
    echo -e "${GREEN}✓${NC} Updated pyproject.toml"

    # Update package.json
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s/\"version\": \"${old_version}\"/\"version\": \"${new_version}\"/" package.json
    else
        sed -i "s/\"version\": \"${old_version}\"/\"version\": \"${new_version}\"/" package.json
    fi
    echo -e "${GREEN}✓${NC} Updated package.json"

    # Update cli.py
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s/@click.version_option(version=\"${old_version}\"/@click.version_option(version=\"${new_version}\"/" git_quick/cli.py
    else
        sed -i "s/@click.version_option(version=\"${old_version}\"/@click.version_option(version=\"${new_version}\"/" git_quick/cli.py
    fi
    echo -e "${GREEN}✓${NC} Updated git_quick/cli.py"
}

# Main script
main() {
    # Check if we're in the right directory
    if [ ! -f "pyproject.toml" ]; then
        echo -e "${RED}Error: pyproject.toml not found. Run this script from the project root.${NC}"
        exit 1
    fi

    # Get bump type from argument
    BUMP_TYPE=${1:-patch}

    # Get current version
    CURRENT_VERSION=$(get_current_version)
    echo -e "${BLUE}Current version: ${CURRENT_VERSION}${NC}"

    # Calculate new version
    NEW_VERSION=$(calculate_new_version "$CURRENT_VERSION" "$BUMP_TYPE")
    echo -e "${BLUE}New version: ${NEW_VERSION}${NC}"

    # Confirm
    echo ""
    read -p "Proceed with version bump? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}Aborted${NC}"
        exit 0
    fi

    # Update version in files
    update_version "$CURRENT_VERSION" "$NEW_VERSION"

    # Check if git is clean
    if ! git diff-index --quiet HEAD --; then
        echo ""
        echo -e "${BLUE}Staging changes...${NC}"
        git add pyproject.toml package.json git_quick/cli.py

        echo -e "${BLUE}Creating commit...${NC}"
        git commit -m "chore: bump version to ${NEW_VERSION}"

        echo -e "${BLUE}Creating tag...${NC}"
        git tag -a "v${NEW_VERSION}" -m "Release v${NEW_VERSION}"

        echo ""
        echo -e "${GREEN}✨ Version bumped successfully!${NC}"
        echo ""
        echo "Next steps:"
        echo "  1. Review the changes: git show HEAD"
        echo "  2. Push to GitHub: git push origin main --tags"
        echo "  3. The workflow will automatically publish to npm and PyPI"
        echo ""
        echo "Or to publish manually:"
        echo "  - PyPI: python -m build && python -m twine upload dist/*"
        echo "  - npm: npm publish"
    else
        echo -e "${GREEN}✓ Version updated in files${NC}"
        echo ""
        echo -e "${YELLOW}Note: No git commit created (no changes detected)${NC}"
    fi
}

# Show usage if --help
if [[ "$1" == "--help" ]] || [[ "$1" == "-h" ]]; then
    cat << EOF
Usage: ./scripts/bump-version.sh [TYPE|VERSION]

Arguments:
  TYPE     - major, minor, or patch (default: patch)
  VERSION  - Explicit version number (e.g., 1.2.3)

Examples:
  ./scripts/bump-version.sh patch     # 0.1.0 → 0.1.1
  ./scripts/bump-version.sh minor     # 0.1.0 → 0.2.0
  ./scripts/bump-version.sh major     # 0.1.0 → 1.1.0
  ./scripts/bump-version.sh 2.0.0     # Set explicit version

EOF
    exit 0
fi

main "$@"
