"""Check a commit message file against the commit-message skill's format.

Usage: python3 check_commit_msg.py <message-file> [--types feat,fix,...]
Pass --types when the repository allows fewer types than the default.
Prints "ok" and exits 0, or prints one problem per line and exits 1.
"""
import re
import sys

SUBJECT_MAX = 72  # Beams: 50 is the target, 72 the hard limit.
BODY_MAX = 72  # Pope: wrap the body at about 72 so `git log` reads on 80 columns.
TYPES = "feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert"
args = sys.argv[1:]
if "--types" in args:
    i = args.index("--types")
    TYPES = args[i + 1].replace(",", "|")
    del args[i : i + 2]
if len(args) != 1:
    sys.exit(__doc__)
SUBJECT_RE = re.compile(rf"^({TYPES})(\([a-z0-9._/-]+\))?!?: \S")

lines = open(args[0], encoding="utf-8").read().rstrip("\n").split("\n")
problems = []
subject = lines[0]

if not SUBJECT_RE.match(subject):
    problems.append(f"subject must start with type(scope): and one of {TYPES}")
if len(subject) > SUBJECT_MAX:
    problems.append(f"subject is {len(subject)} chars, limit {SUBJECT_MAX}")
if subject.endswith("."):
    problems.append("subject ends with a period")
if len(lines) > 1 and lines[1].strip():
    problems.append("line 2 must be blank")
for n, line in enumerate(lines[2:], start=3):
    if line.startswith("#"):
        problems.append(f"line {n} starts with '#'; git strips it on edit")
    if len(line) > BODY_MAX and not re.search(r"https?://", line):
        problems.append(f"line {n} is {len(line)} chars, wrap at {BODY_MAX}")

print("\n".join(problems) or "ok")
sys.exit(1 if problems else 0)
