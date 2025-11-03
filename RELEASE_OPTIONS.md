# Release Options - Choose Your Workflow

You have **3 different workflows** to choose from. Pick the one that matches your needs!

## 🎯 Quick Comparison

| Method | When It Runs | Control Level | Best For |
|--------|--------------|---------------|----------|
| **Tag-Based** ⭐ | When you push a tag | High | Production releases |
| **Manual** | When you click "Run workflow" | Highest | Careful releases |
| **Auto** | Every push to main | Lowest | Fast iteration |

---

## Option 1: Tag-Based Publishing ⭐ (Recommended)

**File:** `.github/workflows/publish-on-tag.yml` ✅ **Active**

### When It Runs
Only when you create and push a version tag (e.g., `v1.2.3`)

### Usage

```bash
# Step 1: Bump version manually
./scripts/bump-version.sh minor   # or patch/major

# Step 2: Push (this triggers publish)
git push origin main --tags

# ✅ Publishes to npm and PyPI!
```

### Pros
- ✅ Full control over when releases happen
- ✅ Can batch multiple commits into one release
- ✅ Clean git history with version tags
- ✅ Won't accidentally publish work-in-progress

### Cons
- ⚠️ Need to remember to push tags
- ⚠️ Manual version management

### Best For
- Production releases
- When you want to batch changes
- When multiple people work on the project

---

## Option 2: Manual Trigger Publishing

**File:** `.github/workflows/publish-manual.yml` ✅ **Active**

### When It Runs
Only when you manually trigger it from GitHub Actions tab

### Usage

1. Go to: `https://github.com/YOUR_USERNAME/git-quick/actions`
2. Click "Manual Publish" workflow
3. Click "Run workflow"
4. Choose version bump type (patch/minor/major)
5. Click "Run workflow" button

![Manual Workflow](https://docs.github.com/assets/images/actions-workflow-dispatch-button.png)

### Pros
- ✅ Highest control - explicitly trigger releases
- ✅ Can choose version bump type in UI
- ✅ Can set custom version numbers
- ✅ Perfect for emergency releases
- ✅ Can release old commits

### Cons
- ⚠️ Need to use GitHub UI
- ⚠️ Can't script it easily

### Best For
- Testing releases
- Emergency hotfixes
- When you're not sure about automation

---

## Option 3: Automatic Publishing (Disabled by Default)

**File:** `.github/workflows/publish-auto.yml.disabled` ❌ **Disabled**

### When It Runs
**Every time** you push to main (except docs-only changes)

### How to Enable

```bash
# Rename to enable
mv .github/workflows/publish-auto.yml.disabled .github/workflows/publish-auto.yml
git add .github/workflows/publish-auto.yml
git commit -m "feat: enable auto-publish"
git push origin main
```

### Usage

```bash
# Just commit and push - that's it!
git commit -m "fix: resolve bug"
git push origin main
# ✅ Auto-publishes! (patch bump)

git commit -m "feat: add feature"
git push origin main
# ✅ Auto-publishes! (minor bump)
```

### Pros
- ✅ Zero manual work
- ✅ Releases happen instantly
- ✅ Version bumps based on commit messages
- ✅ Great for solo developers with CI/CD experience

### Cons
- ⚠️ Publishes on EVERY push
- ⚠️ Can create many releases quickly
- ⚠️ Hard to batch changes
- ⚠️ Accidents can happen

### Best For
- Solo developers
- Fast iteration projects
- When you're very careful with commits
- When you trust conventional commits

---

## 📊 Comparison Example

**Scenario:** You fix 3 bugs today

### Tag-Based (Recommended)
```bash
git commit -m "fix: bug 1"
git commit -m "fix: bug 2"
git commit -m "fix: bug 3"
git push origin main              # No publish yet

./scripts/bump-version.sh patch   # Bump version once
git push origin main --tags       # Publish once: v0.1.1
```
**Result:** 1 release with all 3 fixes ✅

### Manual
```bash
git commit -m "fix: bug 1"
git commit -m "fix: bug 2"
git commit -m "fix: bug 3"
git push origin main              # No publish yet

# Go to GitHub Actions → Run workflow manually
```
**Result:** 1 release when you're ready ✅

### Auto (if enabled)
```bash
git commit -m "fix: bug 1"
git push origin main              # Publishes v0.1.1
git commit -m "fix: bug 2"
git push origin main              # Publishes v0.1.2
git commit -m "fix: bug 3"
git push origin main              # Publishes v0.1.3
```
**Result:** 3 separate releases ⚠️

---

## 🎯 Recommendation

### For Most Users: **Tag-Based** ⭐

Use tag-based publishing because:
- You control when releases happen
- You can batch multiple commits
- Clean version history
- Safe for teams

```bash
# Daily workflow:
git commit -m "fix: something"
git commit -m "feat: something else"
git push origin main                    # Work is backed up

# When ready to release:
./scripts/bump-version.sh minor         # Bump version
git push origin main --tags             # Trigger publish
```

### For Solo Fast Iteration: **Auto**

Enable auto-publish if you:
- Work alone
- Want instant releases
- Trust your commit discipline
- Use conventional commits religiously

```bash
# Enable it
mv .github/workflows/publish-auto.yml.disabled .github/workflows/publish-auto.yml
git add .github/workflows/publish-auto.yml
git commit -m "feat: enable auto-publish"
git push origin main

# Then just:
git commit -m "feat: new thing"
git push origin main  # ✨ Auto-publishes!
```

---

## 🔧 Can I Use Multiple?

Yes! You can have multiple workflows enabled:

- **Tag-Based + Manual** ✅ Recommended combo
  - Use tags for normal releases
  - Use manual for emergency hotfixes

- **Auto + Manual** ⚠️ Not recommended
  - Confusing to have two publish methods
  - Risk of double-publishing

- **All Three** ❌ Don't do this
  - Too complex
  - High chance of conflicts

---

## 🛠 Current Setup

**Active Workflows:**
- ✅ `.github/workflows/publish-on-tag.yml` (Tag-based)
- ✅ `.github/workflows/publish-manual.yml` (Manual trigger)
- ✅ `.github/workflows/test.yml` (Tests on all branches)

**Disabled Workflows:**
- ❌ `.github/workflows/publish-auto.yml.disabled` (Auto-publish)

**Default Behavior:**
- Push to main → Nothing published
- Push tag v1.2.3 → Publishes to npm + PyPI
- Manual trigger → Publishes with chosen version

---

## 🚀 Quick Start

**Using Tag-Based (Recommended):**

```bash
# 1. Make changes
git add .
git commit -m "feat: awesome feature"
git push origin main

# 2. Ready to release?
./scripts/bump-version.sh minor   # Choose: patch/minor/major
git push origin main --tags       # Publish!

# 3. Watch it publish
# https://github.com/YOUR_USERNAME/git-quick/actions
```

**Using Manual:**

```bash
# 1. Make changes
git add .
git commit -m "feat: awesome feature"
git push origin main

# 2. Go to GitHub
# https://github.com/YOUR_USERNAME/git-quick/actions
# → Click "Manual Publish"
# → Click "Run workflow"
# → Choose version bump
# → Click green "Run workflow" button
```

---

## 📚 More Info

- **Full setup:** See [PUBLISHING_SETUP.md](PUBLISHING_SETUP.md)
- **Version bumping:** Run `./scripts/bump-version.sh --help`
- **Conventional commits:** https://www.conventionalcommits.org/

**Questions?** Choose Tag-Based and you'll be fine! ⭐
