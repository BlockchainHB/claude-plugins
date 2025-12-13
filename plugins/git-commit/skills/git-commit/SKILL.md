---
name: git-commit
description: Create detailed, well-structured git commits with conventional commit format. Use when committing changes, staging files, or writing commit messages.
---

# Git Commit Helper

Create professional git commits with detailed messages that document what changed and why.

## When to Use

- Committing staged changes
- Writing commit messages
- Reviewing changes before commit

## Workflow

### 1. Verify Branch

**Never commit directly to protected branches.**

```bash
git branch --show-current
```

- If on `main` or `master`, create a feature branch first
- Branch naming: `feature/description` or `username/issue-id-description`

### 2. Review Changes

```bash
# View staged changes
git diff --staged

# View file list with stats
git diff --staged --stat

# List all staged files
git diff --staged --name-only
```

Verify only relevant files are staged. Exclude temp files, `node_modules`, `.env`, etc.

### 3. Write Commit Message

Use conventional commit format with detailed body:

```
type(scope): short summary (50 chars max)

Detailed description explaining what and why.

## What Changed
- Main accomplishment 1
- Main accomplishment 2

## Files Changed
- `path/to/file.ts` - +X/-Y lines
  - Specific changes made
- `path/to/new-file.ts` - Created (X lines)

## Affected Components
- Component or system affected

Related: ISSUE-ID
```

### Commit Types

| Type | Use For |
|------|---------|
| `feat` | New feature |
| `fix` | Bug fix |
| `refactor` | Code restructuring |
| `docs` | Documentation |
| `test` | Adding tests |
| `chore` | Maintenance |
| `style` | Formatting |
| `perf` | Performance |

### 4. Create Commit

```bash
git commit -m "$(cat <<'EOF'
feat(auth): add password reset flow

Implements complete password reset with email verification.

## What Changed
- Added reset request endpoint
- Created email template
- Added token validation

## Files Changed
- `src/auth/reset.ts` - +120/-0 lines
- `src/email/templates/reset.html` - Created

Related: AUTH-123
EOF
)"
```

### 5. Push to Remote

```bash
# First push (sets upstream)
git push -u origin branch-name

# Subsequent pushes
git push
```

## Best Practices

- **Present tense**: "add feature" not "added feature"
- **Explain why**: Not just what changed, but motivation
- **List all files**: Use `git diff --staged --name-only` to verify
- **Include stats**: Line counts help reviewers gauge scope
- **Never skip hooks**: Avoid `--no-verify` unless explicitly needed

## Safety Rules

- Never push to `main`/`master` without explicit confirmation
- Never force push to shared branches
- Never commit secrets (`.env`, credentials, API keys)
- Always verify staged files before committing
