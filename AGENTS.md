# AGENTS.md
<!-- PROJECT:BEGIN  (filled during the kickoff; yours to edit; `kit.py upgrade` never touches this block) -->
Project: {{PROJECT_NAME}}: {{ONE_LINE_PURPOSE}}
Stack: {{STACK_SUMMARY}}. Start the app: `bash scripts/dev.sh`. One test: `{{ONE_TEST}}`
Project rules (max 10; only what the code can't tell you):
- {{e.g. "Every route calls requireUser(); never trust ids from the client"}}
<!-- PROJECT:END -->

<!-- KIT:BEGIN v4.1.0  (replaced by `kit.py upgrade`; keep it short: every line here costs tokens in every session) -->
## Every session
1. Read the SESSION BRIEF (Claude Code injects it; otherwise run `python3 scripts/kit.py brief`). Obey its USER DIRECTIVES.
2. When the user states a preference or changed requirement, append one dated line to `agent/directives.md` first.
3. One feature or task per session. Workflows: skills `feature`, `bugfix`, `change`, `kickoff`, `security`, `perf`,
   `evaluate`, `peer-review`, `audit`, `prove`, `state` (in `.agents/skills/`; `/name` in Claude Code).
4. Find code with `python3 scripts/kit.py where <FEAT-x|AC-x|symbol>` and `rg -n`; open only the lines you need.
   Criteria: `kit.py show FEAT-x`. Never read agent/features.json whole.

## Hard rules (guards enforce most of them)
- Build only what the acceptance criteria require; ideas go to `agent/later.md`. Reuse before creating (where/rg).
- Before editing, list the files in `agent/scope.txt`. Commits outside it fail.
- Server-side authorization and input validation on every entry point; secrets only via env; never read .env files.
- New package: `kit.py dep-check <name>` + row in docs/dependencies.md first.
- Mark criteria only with `kit.py pass` / `kit.py done`. Never edit agent/features.json, never delete, skip or weaken
  a test, never reword a criterion (changes go through agent/plan.json + the human).
- Never say "fixed", "done" or "tests pass" unless you ran it in THIS session. Not checked = NOT VERIFIED.
- Human-only: protected files (scripts/kit.py, verify.sh, verify.config, hook files) and the override variables.
- Ask first: schema-breaking migrations, deleting files, auth changes outside the current feature, large new packages.
- Gate: `bash scripts/verify.sh --quick` while working, `bash scripts/verify.sh` once at the end.
<!-- KIT:END -->
