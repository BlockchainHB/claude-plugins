---
name: feature-setup
description: Systematically set up new features from planning through implementation structure. Use when starting a new feature, creating feature branches, or planning technical approach.
---

# Feature Setup

Systematically set up new features from initial planning through implementation structure.

## When to Use

- Starting a new feature
- Creating feature branches
- Planning technical approach
- Setting up project structure

## Workflow

### 1. Define Requirements

Before writing code, clarify:

**Scope & Goals**
- What problem does this solve?
- What are the success criteria?
- What's explicitly out of scope?

**User Stories**
```
As a [user type]
I want to [action]
So that [benefit]
```

**Acceptance Criteria**
- [ ] Specific, testable requirement 1
- [ ] Specific, testable requirement 2
- [ ] Edge case handling

### 2. Create Feature Branch

```bash
# Fetch latest main
git fetch origin main

# Create branch from main
git checkout -b feature/feature-name origin/main

# Or with issue ID
git checkout -b username/ISSUE-123-feature-name origin/main
```

**Branch Naming Conventions**
| Pattern | Use For |
|---------|---------|
| `feature/name` | New features |
| `fix/name` | Bug fixes |
| `refactor/name` | Code restructuring |
| `chore/name` | Maintenance |

### 3. Plan Architecture

**Data Models**
- What entities are needed?
- What are the relationships?
- What fields and types?

**API Design**
- What endpoints are needed?
- Request/response shapes
- Error handling approach

**UI Components**
- Component hierarchy
- State management
- User interactions

**Testing Strategy**
- Unit test coverage
- Integration tests
- E2E scenarios

### 4. Set Up Structure

Create the directory structure:

```
src/
├── features/
│   └── feature-name/
│       ├── components/
│       │   ├── FeatureComponent.tsx
│       │   └── index.ts
│       ├── hooks/
│       │   └── useFeature.ts
│       ├── api/
│       │   └── featureApi.ts
│       ├── types/
│       │   └── index.ts
│       └── index.ts
└── ...
```

### 5. Configure Dependencies

```bash
# Install required packages
npm install package-name

# Or with specific version
npm install package-name@^1.0.0
```

Update configuration files as needed.

## Feature Setup Checklist

### Planning
- [ ] Requirements documented
- [ ] User stories written
- [ ] Acceptance criteria defined
- [ ] Technical approach planned

### Setup
- [ ] Feature branch created
- [ ] Directory structure set up
- [ ] Dependencies installed
- [ ] Configuration updated

### Ready to Develop
- [ ] Development environment works
- [ ] Can run tests
- [ ] Linting passes
- [ ] Team aligned on approach

## Best Practices

- **Start small**: Begin with core functionality
- **Document decisions**: Record why, not just what
- **Plan for testing**: Consider testability early
- **Keep scope tight**: Avoid scope creep
- **Communicate**: Share approach with team

## Output Artifacts

Consider creating:

- **Technical spec**: Architecture decisions
- **Task breakdown**: Implementation steps
- **Changelog entry**: For tracking progress
- **Documentation draft**: User-facing docs
