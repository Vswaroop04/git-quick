# Release Workflow - Quick Guide

## Automatic Publishing (Recommended)

### Setup Once

1. **Get API Tokens**:

   - PyPI: https://pypi.org/manage/account/token/
   - npm: https://www.npmjs.com/settings/YOUR_USERNAME/tokens

2. **Add to GitHub Secrets**:

   - Go to: `https://github.com/YOUR_USERNAME/git-quick/settings/secrets/actions`
   - Add `PYPI_API_TOKEN` (from PyPI)
   - Add `NPM_TOKEN` (from npm)

3. **First Manual Release**:

   ```bash
   # Publish to PyPI (first time)
   python -m build
   python -m twine upload dist/*

   # Publish to npm (first time)
   npm login
   npm publish
   ```

### Daily Usage

Just commit and push to main:

```bash
# Fix bugs (patch bump: 0.1.0 → 0.1.1)
git commit -m "fix: resolve config loading issue"
git push origin main
# ✨ Auto-publishes to npm and PyPI!

# Add features (minor bump: 0.1.0 → 0.2.0)
git commit -m "feat: add setup wizard"
git push origin main
# ✨ Auto-publishes to npm and PyPI!

# Breaking changes (major bump: 0.1.0 → 1.1.0)
git commit -m "feat!: redesign CLI interface"
git push origin main
# ✨ Auto-publishes to npm and PyPI!
```

**That's it!** The GitHub Action handles:

- ✅ Version bumping
- ✅ Git tagging
- ✅ PyPI publishing
- ✅ npm publishing
- ✅ GitHub release creation

## Manual Version Bump (Alternative)

Use the helper script:

```bash
# Patch bump (0.1.0 → 0.1.1)
./scripts/bump-version.sh patch

# Minor bump (0.1.0 → 0.2.0)
./scripts/bump-version.sh minor

# Major bump (0.1.0 → 1.1.0)
./scripts/bump-version.sh major

# Custom version
./scripts/bump-version.sh 2.5.0

# Push changes
git push origin main --tags
# ✨ Auto-publishes!
```

## Version Bump Rules

The workflow automatically determines the bump type from your commits:

| Commit Message                 | Bump Type | Example       |
| ------------------------------ | --------- | ------------- |
| `fix:`, `chore:`, `docs:`      | Patch     | 0.1.0 → 0.1.1 |
| `feat:`                        | Minor     | 0.1.0 → 0.2.0 |
| `feat!:` or `BREAKING CHANGE:` | Major     | 0.1.0 → 1.1.0 |

## Skip CI

To push without triggering a release:

```bash
git commit -m "docs: update README [skip ci]"
git push origin main
```

## Monitoring

Watch the release progress:

- Actions: `https://github.com/YOUR_USERNAME/git-quick/actions`
- PyPI: `https://pypi.org/project/git-quick/`
- npm: `https://www.npmjs.com/package/git-quick-cli`
- Releases: `https://github.com/YOUR_USERNAME/git-quick/releases`

## Troubleshooting

**Publish fails?**

- Check workflow logs in Actions tab
- Verify secrets are set correctly
- Make sure first manual release is done

**Wrong version bump?**

- Use correct commit message format
- Or use manual bump script

**Need to rollback?**

```bash
# Delete tag
git tag -d v1.2.3
git push origin :refs/tags/v1.2.3

# Revert commit
git revert HEAD
git push origin main
```

## Full Documentation

See [PUBLISHING_SETUP.md](PUBLISHING_SETUP.md) for complete setup instructions.

---

**Happy Releasing! 🚀**
