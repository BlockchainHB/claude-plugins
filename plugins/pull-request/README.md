# Pull Request Helper

Open pull requests that reviewers can read in a minute.

## What It Does

Claude uses this skill when it creates a PR. Each PR gets:

- **An outcome title**: `type(scope): plain-language outcome`, such as `fix(web): new threads no longer spike CPU`
- **A short body**: the problem, what the system does now, what did not change, and the risk
- **Honest evidence**: the checks that ran and what they showed, what did not run, and measured numbers kept apart from estimates
- **Your rules first**: it fills your repository's PR template when one exists

It leaves out file lists and test-plan checklists. The Files tab already shows the files.

## Usage

"Create a PR for this branch"
"Open a pull request"
"Prepare this for review"

Claude reads every commit on the branch, writes the title and body, and creates the PR.

## Author

[@hasaamb](https://x.com/hasaamb)
