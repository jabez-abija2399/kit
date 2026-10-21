# Approved dependencies
Every entry was checked with `python3 scripts/kit.py dep-check <name>` (exists, age, maintenance, downloads, license),
and compared with 2 alternatives. Install these without a new entry. Anything else: dep-check it and 2 alternatives ->
add a row here -> install. Prefer a well-known package over writing the code yourself.
New versions are only installed once they are a few days old (dependency cooldown: `python3 scripts/kit.py harden`).
(The pre-commit hook and the Claude Code hook block packages that are not listed here or in docs/decisions.md.)

| Package | Where | Purpose | Alternatives considered (why not) | License | Checked |
|---|---|---|---|---|---|

Binaries / services (not from a package registry): {{e.g. Docker, Postgres 17 image}}
