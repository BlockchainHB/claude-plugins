---
name: pull-request
description: Opens a pull request with a plain-language outcome title and a short problem, change, and verification body. Follows the repository's PR template and rules first. Use when creating a PR, opening a merge request, or preparing a branch for review.
---

# Pull request

## 1. Find the rules

Read `.github/pull_request_template.md`, the PR section of `AGENTS.md` or `CLAUDE.md`, and `CONTRIBUTING.md`. If the repository has a template, keep its headings and their order, and apply the guidance below inside them.

## 2. Prepare the branch

```bash
git status
git fetch origin main
git log origin/main..HEAD --oneline
git diff origin/main...HEAD --stat
git push -u origin "$(git branch --show-current)"
```

- Commit any uncommitted changes first.
- Read every commit on the branch, not only the latest.
- Keep what you observed apart from what you infer. Never say a test or check passed unless it ran on this head.

## 3. Title

Write `type(scope): plain-language outcome`. State the behavior after the merge, as a changelog reader would see it. Keep it to 72 characters.

- fix: say what no longer goes wrong. "fix(web): new threads no longer spike CPU"
- perf: give the number only if you measured it on this change. Otherwise state the effect. "perf(server): background launcher uses 75% less memory"
- feat: say what the user can now do. "feat(tasks): tasks link to their thread"

## 4. Body

For a small PR with one behavior change, write two or three paragraphs and no headings: the problem, then what the system does now, then the proof.

For a larger PR, use these sections, in this order. Leave out a section that would be empty.

- **Problem**: What was wrong, and for whom, in one to three sentences. Give the real case and its numbers if you have them.
- **Change**: What the system does now, as behavior. Give one bullet to each component that changed. End with **Not changed:** and the nearby things a reviewer could think you touched.
- **Risk**: Write this section only if a risk exists. Give the failure mode, who it affects, and how to roll back.
- **Verification**: Give the exact commands and checks you ran, and what you saw. Name the test that fails on the base branch. Say what you did not run, and why. Label each number as **Measured** or **Modeled, not measured**.
- **Related**: `Closes #123`, and linked PRs, each with one line on how it relates.

For UI changes, put before and after screenshots in a two-column table. For motion or timing, add a short recording. Upload them to GitHub. Never commit them.

Do not add a file-by-file list, line counts, a test-plan checklist, or a summary that repeats the sections. The Files tab already shows the files.

Write short sentences with one fact each. Use active voice and no semicolons. Put code names in code font.

## 5. Create the PR

Write the body to a temp file, then:

```bash
gh pr create --title "<title>" --body-file <body-file>
```

Add labels or reviewers only if the repository uses them: `gh pr edit --add-label <label>`, `gh pr edit --add-reviewer <user>`.

## Example

```markdown
Title: fix(web): tagging a thread by drag no longer scrolls the sidebar

Dragging a thread from the sidebar into the composer scrolled the
sidebar, often to the bottom. The drag crossed the autoscroll edge zone
while it was still a reorder drag.

The sidebar now saves its scroll position when a drag starts. It puts
that position back when the drag leaves the list, and again on drop.
Reordering inside the list still autoscrolls.

Verification: a slow drag in the dev app with 500 threads. Measured
sidebar `scrollTop` over the composer: 217px before, 0 after. No
automated test: no harness renders the full sidebar with a long list.
```
