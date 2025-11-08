# 🔀 Git Workflow & Safety - HidroCalc

Guía completa de uso de Git para desarrollo seguro y colaborativo.

---

## 🛡️ Git Safety Protocol

### **NUNCA hacer:**

- ❌ NEVER update the git config
- ❌ NEVER run destructive/irreversible git commands (push --force, hard reset) unless explicitly requested
- ❌ NEVER skip hooks (--no-verify, --no-gpg-sign) unless explicitly requested
- ❌ NEVER force push to main/master - warn the user if they request it
- ❌ NEVER commit changes unless explicitly asked
- ❌ Avoid `git commit --amend` unless explicitly requested or fixing pre-commit hook

---

## 📝 Committing Changes

**IMPORTANTE:** Solo crear commits cuando el usuario lo solicite explícitamente.

### **Git Commit Protocol:**

1. **Run multiple commands in parallel:**
```bash
git status  # Ver archivos sin trackear
git diff    # Ver cambios staged y unstaged
git log --oneline -5  # Ver estilo de mensajes recientes
```

2. **Analyze changes and draft commit message:**
   - Resumir naturaleza de cambios (feature, enhancement, bug fix, refactor, etc.)
   - No commitear archivos con secretos (.env, credentials.json)
   - Mensaje conciso (1-2 oraciones) enfocado en "why" no "what"
   - Asegurar que refleje cambios y su propósito

3. **Add files and create commit:**
```bash
git add <files>  # Agregar archivos relevantes

git commit -m "$(cat <<'EOF'
Commit message here.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

4. **If commit fails due to pre-commit hook:**
   - Verificar authorship: `git log -1 --format='%an %ae'`
   - Verificar no pushed: `git status` debe mostrar "Your branch is ahead"
   - Si ambos true: amend commit
   - Si no: crear NUEVO commit (nunca amend commits de otros developers)

---

## 💬 Commit Message Format

### **Template:**

```
<type>: <summary>

[optional body]

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

### **Types:**

- **feat:** Nueva funcionalidad
- **fix:** Bug fix
- **refactor:** Refactorización sin cambiar funcionalidad
- **docs:** Solo documentación
- **test:** Agregar o modificar tests
- **chore:** Cambios de build, dependencies, etc.
- **style:** Formateo, missing semi-colons, etc.

### **Examples:**

```
feat: Add API documentation with drf-spectacular

- Install and configure drf-spectacular (v0.29.0)
- Add Swagger UI at /api/docs/
- Add ReDoc at /api/redoc/

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

```
fix: Resolve authentication error in watershed creation

Users were unable to create watersheds due to missing
permission check. Added IsAuthenticated permission class
to WatershedViewSet.

Fixes #123

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

---

## 🌿 Branch Strategy

### **Main Branches:**

- `main` - Production-ready code
- `develop` - Integration branch for features

### **Supporting Branches:**

- `feature/*` - New features
- `bugfix/*` - Bug fixes
- `hotfix/*` - Critical production fixes
- `refactor/*` - Code refactoring

### **Naming Convention:**

```bash
feature/add-pdf-export
bugfix/fix-rational-calculation
hotfix/security-patch-jwt
refactor/optimize-database-queries
```

---

## 🔄 Workflow

### **1. Starting New Work:**

```bash
# Update main
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/my-feature

# Work on feature...
```

### **2. During Development:**

```bash
# Regular commits
git add .
git commit -m "feat: implement rational method calculator"

# Push to remote
git push -u origin feature/my-feature
```

### **3. Before Merging:**

```bash
# Update from main
git checkout main
git pull origin main
git checkout feature/my-feature
git merge main  # or git rebase main

# Run tests
python -m pytest

# Push updates
git push origin feature/my-feature
```

---

## 🔍 Pull Request Protocol

### **Creating PR using gh CLI:**

```bash
# Push branch
git push -u origin feature/my-feature

# Create PR
gh pr create --title "Add rational method calculator" --body "$(cat <<'EOF'
## Summary
- Implemented rational method calculator
- Added validation for input parameters
- Created tests with 95% coverage

## Test plan
- [ ] Manual testing of calculator interface
- [ ] Automated tests pass
- [ ] API endpoints work correctly

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

### **PR Description Template:**

```markdown
## Summary
- Bullet point 1
- Bullet point 2

## Test plan
- [ ] Test item 1
- [ ] Test item 2

## Screenshots (if UI changes)
[Add screenshots]

## Related Issues
Fixes #123
Related to #456

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

---

## 🚫 What NOT to Commit

### **.gitignore essentials:**

```gitignore
# Environment variables
.env
.env.*
!.env.example

# Database
*.db
*.sqlite
*.sqlite3

# Python
__pycache__/
*.pyc
*.pyo
.Python
venv/
.venv/

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Django
/media
/staticfiles
db.sqlite3

# Secrets
*credentials*
*secrets*
*.pem
*.key
```

---

## 🔐 Handling Secrets

### **If secret accidentally committed:**

```bash
# WARNING: This rewrites history - coordinate with team!

# Remove from last commit
git rm --cached .env
echo ".env" >> .gitignore
git add .gitignore
git commit --amend -m "Remove .env file"

# If already pushed - NOTIFY TEAM
git push --force origin feature/my-feature

# Rotate the exposed secret immediately!
```

### **Prevention:**

```bash
# Use git hooks
# .git/hooks/pre-commit

#!/bin/sh
if git diff --cached --name-only | grep -E '\.(env|pem|key)$'; then
    echo "ERROR: Attempting to commit secret file!"
    exit 1
fi
```

---

## 🔀 Merge vs Rebase

### **When to use merge:**

```bash
# Integrating feature into main
git checkout main
git merge feature/my-feature
```

**Pros:**
- Preserves complete history
- Shows when feature was integrated
- Safer for shared branches

### **When to use rebase:**

```bash
# Updating feature branch with main changes
git checkout feature/my-feature
git rebase main
```

**Pros:**
- Linear history
- Cleaner log
- Easier to understand

**NEVER rebase:**
- Public/shared branches
- Commits already pushed to main

---

## 🏷️ Tags and Releases

### **Creating version tags:**

```bash
# Semantic versioning: MAJOR.MINOR.PATCH
git tag -a v3.0.0 -m "Release version 3.0.0 - Django migration complete"
git push origin v3.0.0

# Create GitHub release
gh release create v3.0.0 --title "v3.0.0 - Django Migration" --notes "
## What's New
- Complete migration to Django 5.2.8
- API documentation with Swagger/ReDoc
- 30+ REST API endpoints

## Breaking Changes
- Migrated from FastAPI to Django

## Bug Fixes
- Fixed authentication flow
"
```

---

## 🧹 Cleanup

### **Delete merged branches:**

```bash
# Local
git branch -d feature/my-feature

# Remote
git push origin --delete feature/my-feature

# Clean up remote-tracking references
git fetch --prune
```

### **Stashing uncommitted work:**

```bash
# Save work temporarily
git stash save "WIP: implementing calculator"

# List stashes
git stash list

# Apply and remove
git stash pop

# Apply and keep
git stash apply stash@{0}

# Clear all stashes
git stash clear
```

---

## 📊 Useful Git Commands

### **Inspection:**

```bash
# View file history
git log --follow -- path/to/file

# See who changed what
git blame path/to/file

# View changes between branches
git diff main..feature/my-feature

# View commits on feature branch
git log main..feature/my-feature

# Visual history
git log --graph --oneline --all
```

### **Undoing Changes:**

```bash
# Discard local changes to file
git checkout -- path/to/file

# Unstage file
git reset HEAD path/to/file

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes) - DANGEROUS!
git reset --hard HEAD~1  # Use with caution!
```

---

## 🤝 Collaboration Best Practices

### **1. Pull before push:**
```bash
git pull --rebase origin main
git push origin feature/my-feature
```

### **2. Small, focused commits:**
```bash
# Good: Small, focused
git commit -m "feat: add email validation"

# Bad: Large, unfocused
git commit -m "feat: add multiple features and fix bugs"
```

### **3. Regular pushes:**
```bash
# Push at end of day or after significant progress
git push origin feature/my-feature
```

### **4. Keep branches up-to-date:**
```bash
# Regularly merge/rebase main
git checkout feature/my-feature
git merge main
```

---

## 🚨 Emergency Procedures

### **Revert a bad commit:**

```bash
# Create revert commit
git revert <commit-hash>

# Revert multiple commits
git revert <oldest-hash>..<newest-hash>
```

### **Recover deleted branch:**

```bash
# Find the commit
git reflog

# Recreate branch
git checkout -b recovered-branch <commit-hash>
```

### **Fix detached HEAD:**

```bash
# Create branch from detached state
git checkout -b recovery-branch

# Or return to main
git checkout main
```

---

## ✅ Pre-Push Checklist

- [ ] All tests pass: `python -m pytest`
- [ ] No secrets in commits
- [ ] Commit messages are clear
- [ ] Branch is up-to-date with main
- [ ] Code follows style guidelines
- [ ] No debug code or console.logs
- [ ] Documentation updated if needed

---

**Última actualización:** 2025-11-08
