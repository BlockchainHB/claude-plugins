---
name: git-commit
description: Writes and makes git commits in Conventional Commits format with Tim Pope and Chris Beams formatting (50/72, imperative, why over how), after branch and secret checks. Follows the repository's own commit rules first. Use when committing changes, staging files, or writing a commit message.
---

# Git commit

## 1. Find the rules

Repository rules win. Check the commit section of `AGENTS.md` or `CLAUDE.md`, then `CONTRIBUTING.md`, `.gitmessage`, any commitlint config, and the last 20 subjects (`git log --no-merges -20 --format=%s`). Use this skill only where they are silent.

## 2. Check the branch and the staged change

- Run `git branch --show-current`. Never commit to `main` or `master` without explicit confirmation. Create a feature branch first.
- Stage specific files. Do not stage `.env` files, credentials, `node_modules`, or temp files.
- Run `git diff --staged --stat`, then `git diff --staged`.
- One logical change is one reason someone could revert it. Tests and docs that exist only for that change belong to it. A subject that needs "and" is a sign of two changes. Split two changes into two commits.

## 3. Write the message

```text
type(scope): imperative summary of the effect

Why the change is needed: the old behavior, and what was wrong with
it. Then what the system does now. Leave the how to the diff.

Closes #123
```

Subject:

- Write `type(scope): `, then a summary that completes "If applied, this commit will ...".
- Aim for 50 characters. The hard limit is 72, prefix included.
- Use lowercase after the colon. Do not end with a period.
- Use one of these types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`. If the repository allows fewer, use only those, and pass them to the checker with `--types`.
- Describe the effect, not the file: "fix(auth): keep users signed in across tabs", not "fix(auth): update session.ts".

Body:

- The body is optional. Leave it out when the subject says everything.
- Take the why from the diff and the conversation. If neither shows it, ask the user. Never invent a reason.
- Put a blank line after the subject. Wrap every line at 72 characters. A URL can run longer.
- Write prose or `- ` bullets. Do not use Markdown headings. Git deletes lines that start with `#` when someone edits the message in an editor, for example with `git commit --amend`.
- Do not list files or line counts. `git show --stat` already shows them.
- Write short sentences with one fact each. Use active voice and no semicolons.

Footers go after a blank line, one per line: `BREAKING CHANGE: <what breaks>`, `Closes #123`.

## 4. Check and commit

Write the message to a file. Run the checker in this skill's directory, fix each problem it reports, and run it again:

```bash
python3 <skill-dir>/scripts/check_commit_msg.py <message-file>
git commit -F <message-file>
```

Commit only when the checker prints `ok`. Never skip hooks with `--no-verify` unless the user asks.

## 5. Push

```bash
git push -u origin "$(git branch --show-current)"
```

Never force-push a shared branch.

## Example

```text
fix(sync): stop a failed window from retrying on every run

A failed window reused its job's retry time after that time had
passed, so the scheduler picked the window up on every run. The window
now reuses the retry time only while it is still ahead. Otherwise it
waits the normal idle day.
```
