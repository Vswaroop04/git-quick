# Documentation Structure

This document explains the organization of git-quick's documentation.

## 📁 Structure Overview

### Root Directory (Essential Files Only)
```
git-quick/
├── README.md              # Project overview & quick links
├── QUICKSTART.md          # 5-minute getting started guide
├── CONTRIBUTING.md        # How to contribute
└── LICENSE                # MIT license
```

**Purpose**: Keep the root clean with only the most essential files that users need immediately.

### docs/ Directory (All Documentation)
```
docs/
├── README.md                      # Documentation index & navigation
├── INSTALLATION.md                # Installation instructions
├── USAGE.md                       # Complete command reference
├── QUICK_REFERENCE.md             # Command cheat sheet
├── AI_INTEGRATION.md              # AI features deep dive
├── FIRST_RUN_EXPERIENCE.md        # First-time user guide
├── SETUP.md                       # Development setup
│
├── setup/                         # Setup & Configuration
│   ├── AI_SETUP.md                # AI provider configuration
│   ├── CONFIGURATION_GUIDE.md     # All config options
│   └── SETUP_WIZARD_IMPROVEMENTS.md  # Setup wizard docs
│
└── development/                   # Development Documentation
    ├── PROJECT_SUMMARY.md         # Architecture overview
    ├── PUBLISHING.md              # Release process
    ├── DISTRIBUTION_SUMMARY.md    # Multi-platform distribution
    ├── NEW_CLI_STRUCTURE.md       # CLI architecture
    └── UNIFIED_CLI_SUMMARY.md     # CLI design decisions
```

## 🎯 Documentation Categories

### 1. User Documentation (Root & docs/)
**For end users who want to use git-quick**

- **README.md** - First thing users see, project overview
- **QUICKSTART.md** - Get started in 5 minutes
- **docs/INSTALLATION.md** - How to install
- **docs/USAGE.md** - How to use all commands
- **docs/QUICK_REFERENCE.md** - Quick command lookup

### 2. Setup Documentation (docs/setup/)
**For users configuring git-quick**

- **AI_SETUP.md** - Configure Ollama, OpenAI, or Anthropic
- **CONFIGURATION_GUIDE.md** - All configuration options
- **SETUP_WIZARD_IMPROVEMENTS.md** - How the wizard works

### 3. Development Documentation (docs/development/)
**For contributors and maintainers**

- **PROJECT_SUMMARY.md** - Architecture and design
- **PUBLISHING.md** - How to publish releases
- **DISTRIBUTION_SUMMARY.md** - Multi-platform packaging
- **NEW_CLI_STRUCTURE.md** - CLI implementation
- **UNIFIED_CLI_SUMMARY.md** - CLI design rationale

### 4. Contributing (Root)
**For potential contributors**

- **CONTRIBUTING.md** - Contribution guidelines

## 🗺️ Navigation Paths

### New User Journey
```
1. README.md (overview)
   ↓
2. QUICKSTART.md (get started)
   ↓
3. docs/INSTALLATION.md (install)
   ↓
4. docs/setup/AI_SETUP.md (configure AI)
   ↓
5. docs/USAGE.md (learn commands)
```

### Configuration Journey
```
1. docs/setup/AI_SETUP.md (choose provider)
   ↓
2. docs/setup/CONFIGURATION_GUIDE.md (customize)
   ↓
3. docs/FIRST_RUN_EXPERIENCE.md (what to expect)
```

### Contributor Journey
```
1. CONTRIBUTING.md (guidelines)
   ↓
2. docs/SETUP.md (dev setup)
   ↓
3. docs/development/PROJECT_SUMMARY.md (architecture)
   ↓
4. docs/development/PUBLISHING.md (releases)
```

## 📋 File Purpose Reference

| File | Audience | Purpose |
|------|----------|---------|
| README.md | Everyone | Project overview, quick links |
| QUICKSTART.md | New users | Fast onboarding |
| CONTRIBUTING.md | Contributors | How to contribute |
| docs/README.md | Everyone | Documentation index |
| docs/INSTALLATION.md | Users | Installation guide |
| docs/USAGE.md | Users | Command reference |
| docs/QUICK_REFERENCE.md | Users | Quick lookup |
| docs/AI_INTEGRATION.md | Users | AI features |
| docs/FIRST_RUN_EXPERIENCE.md | New users | First-run guide |
| docs/SETUP.md | Developers | Dev environment |
| docs/setup/AI_SETUP.md | Users | AI configuration |
| docs/setup/CONFIGURATION_GUIDE.md | Users | All config options |
| docs/setup/SETUP_WIZARD_IMPROVEMENTS.md | Developers | Wizard internals |
| docs/development/PROJECT_SUMMARY.md | Developers | Architecture |
| docs/development/PUBLISHING.md | Maintainers | Release process |
| docs/development/DISTRIBUTION_SUMMARY.md | Maintainers | Packaging |
| docs/development/NEW_CLI_STRUCTURE.md | Developers | CLI design |
| docs/development/UNIFIED_CLI_SUMMARY.md | Developers | CLI rationale |

## 🔍 Finding Documentation

### "I want to..."

- **...install git-quick** → `docs/INSTALLATION.md`
- **...get started quickly** → `QUICKSTART.md`
- **...configure AI** → `docs/setup/AI_SETUP.md`
- **...change settings** → `docs/setup/CONFIGURATION_GUIDE.md`
- **...learn commands** → `docs/USAGE.md`
- **...contribute code** → `CONTRIBUTING.md`
- **...understand architecture** → `docs/development/PROJECT_SUMMARY.md`
- **...publish a release** → `docs/development/PUBLISHING.md`

## 📝 Documentation Principles

### 1. Keep Root Clean
- Only essential files in root directory
- Everything else goes in `docs/`

### 2. Organize by Audience
- User docs in `docs/`
- Setup docs in `docs/setup/`
- Dev docs in `docs/development/`

### 3. Clear Navigation
- Every doc has clear purpose
- `docs/README.md` provides navigation
- Main `README.md` links to key docs

### 4. Progressive Disclosure
- Quick start for beginners
- Detailed guides for advanced users
- Technical docs for developers

## 🔄 Maintenance

### Adding New Documentation

1. **User documentation** → Add to `docs/`
2. **Setup/config documentation** → Add to `docs/setup/`
3. **Development documentation** → Add to `docs/development/`
4. **Update** `docs/README.md` with link
5. **Update** main `README.md` if essential

### Updating Documentation

1. Keep file in same location
2. Update cross-references if needed
3. Update `docs/README.md` if title changes

### Removing Documentation

1. Remove file
2. Update `docs/README.md`
3. Update any cross-references
4. Check for broken links

## ✅ Benefits of This Structure

### For Users
✅ Easy to find what they need
✅ Not overwhelmed by dev docs
✅ Clear learning path

### For Contributors
✅ Dev docs separate from user docs
✅ Easy to find technical information
✅ Clear contribution guidelines

### For Maintainers
✅ Clean root directory
✅ Organized documentation
✅ Easy to maintain and update

## 📊 Before vs After

### Before (Cluttered Root)
```
git-quick/
├── README.md
├── AI_SETUP.md
├── CONFIGURATION_GUIDE.md
├── CONTRIBUTING.md
├── DISTRIBUTION_SUMMARY.md
├── PROJECT_SUMMARY.md
├── PUBLISHING.md
├── QUICKSTART.md
├── QUICK_REFERENCE.md
├── SETUP_WIZARD_IMPROVEMENTS.md
├── NEW_CLI_STRUCTURE.md
├── UNIFIED_CLI_SUMMARY.md
└── docs/
    ├── AI_INTEGRATION.md
    ├── FIRST_RUN_EXPERIENCE.md
    ├── INSTALLATION.md
    ├── SETUP.md
    └── USAGE.md
```
**Problem**: 12 markdown files in root, hard to navigate

### After (Organized)
```
git-quick/
├── README.md
├── QUICKSTART.md
├── CONTRIBUTING.md
└── docs/
    ├── README.md (navigation hub)
    ├── [5 user docs]
    ├── setup/ (3 setup docs)
    └── development/ (5 dev docs)
```
**Solution**: 3 files in root, everything else organized in docs/

## 🎯 Summary

The documentation is now organized into:
- **Root**: Essential files only (README, QUICKSTART, CONTRIBUTING)
- **docs/**: All user documentation
- **docs/setup/**: Setup and configuration guides
- **docs/development/**: Development and maintenance docs

This structure makes it easy for users to find what they need without being overwhelmed by development documentation.
