# Git Commit Helper

Write git commits that say why, in Conventional Commits format.

## What It Does

Claude uses this skill when it commits changes. Each commit gets:

- **A short subject**: `type(scope): imperative summary`, 50 characters as the aim and 72 at most
- **A body that says why**: the old behavior, what was wrong, and what the system does now, wrapped at 72
- **A checker**: `scripts/check_commit_msg.py` checks the format before the commit
- **Safety checks**: branch checks, no secrets, no force push

It follows your repository's own commit rules first. The format comes from [Tim Pope](https://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html) and [Chris Beams](https://cbea.ms/git-commit/).

## Usage

"Commit these changes"
"Create a commit for the auth updates"
"Stage and commit the new feature"

Claude reads the staged change, writes the message, checks it, and commits.

## Author

[@hasaamb](https://x.com/hasaamb)
