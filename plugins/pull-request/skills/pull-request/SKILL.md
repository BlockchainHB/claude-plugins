---
name: pull-request
description: Create well-structured pull requests with proper descriptions, labels, and review setup. Use when creating PRs, opening merge requests, or preparing code for review.
---

# Pull Request Helper

Create professional pull requests with comprehensive descriptions and proper setup.

## When to Use

- Creating a new pull request
- Opening a merge request
- Preparing code for review

## Workflow

### 1. Prepare Branch

```bash
# Ensure all changes are committed
git status

# Push branch to remote
git push -u origin branch-name

# Check if up to date with main
git fetch origin main
git log origin/main..HEAD --oneline
```

### 2. Gather Context

```bash
# View all commits in this branch
git log main..HEAD --oneline

# View complete diff from main
git diff main...HEAD

# Get stats
git diff main...HEAD --stat
```

### 3. Write PR Description

Structure your PR description clearly:

```markdown
## Summary

Brief overview of what this PR does and why.

- Key change 1
- Key change 2
- Key change 3

## Changes

### Feature/Component Name
- Specific implementation detail
- Another detail

### Files Modified
- `path/to/file.ts` - What changed
- `path/to/new-file.ts` - New file purpose

## Breaking Changes

List any breaking changes, or "None" if backwards compatible.

## Screenshots

Include screenshots for UI changes.

## Test Plan

- [ ] Unit tests pass
- [ ] Manual testing completed
- [ ] Edge cases verified

## Related Issues

Closes #123
Related: #456
```

### 4. Create PR with GitHub CLI

```bash
gh pr create \
  --title "feat(scope): description" \
  --body "$(cat <<'EOF'
## Summary

Brief description of changes.

- Change 1
- Change 2

## Test Plan

- [ ] Tests pass
- [ ] Manual verification complete

Closes #123
EOF
)"
```

### 5. Set Up PR

After creation:

```bash
# Add labels
gh pr edit --add-label "feature,needs-review"

# Request reviewers
gh pr edit --add-reviewer username

# Link to project
gh pr edit --add-project "Project Name"
```

## PR Title Format

Follow conventional commit format:

| Type | Example |
|------|---------|
| Feature | `feat(auth): add OAuth2 login` |
| Bug fix | `fix(api): handle null response` |
| Refactor | `refactor(db): optimize queries` |
| Docs | `docs(readme): update installation` |

## Best Practices

- **Cover all commits**: Review every commit, not just the latest
- **Explain motivation**: Why this change, not just what
- **Link issues**: Connect to related tickets
- **Add context**: Screenshots, examples, migration steps
- **Keep focused**: One feature/fix per PR

## Checklist Before Creating

- [ ] All commits are meaningful
- [ ] Branch is up to date with main
- [ ] Tests pass locally
- [ ] No debug code or console.logs
- [ ] Documentation updated if needed
- [ ] Breaking changes documented
