# Speed plan: why building with the kit is slow, and how to fix it

Status: plan for review. Date: 2026-11-05. Labels: [MEASURED] timed in this session · [READ] from the code · [PLAN] proposed change.

## 1. What is slow, measured
| Item | Cost | Verdict |
|---|---|---|
| `kit.py brief`, `status`, `check`, `doctor`, `dupes`, `stop-check`, `where` | 0.05–0.09 s each [MEASURED] | Not the problem |
| `verify.sh --quick` (with no test command) | 0.09 s [MEASURED] | Fast, but it fails by design, so nothing passes |
| Guard hook (`protect.py`) per tool call | 0.023 s [MEASURED] | Not the problem |
| Always-loaded docs (`docs/*.md`, `AGENTS.md`, progress) | ~31 KB [MEASURED] | Moderate; trim later |
| Skills (`.agents/skills/*/SKILL.md`) | ~20 KB, loaded only when used [MEASURED] | Fine |

The scripts are not slow. The time is spent waiting on people and on repeated ceremony.

## 2. The real causes [READ + MEASURED]

**Cause 1: the gate can't pass until a human sets a test command.** `verify.sh` fails with "no test command configured: tests are mandatory" until `VERIFY_TEST` is set in `scripts/verify.config`, which is protected. Every feature stalls on this. It happened here: FEAT-001 has six passing tests and still can't be marked done.

**Cause 2: many human-only stops.** `kit.py` has 21 places that name a human-only switch (`GUARD_ADMIN`, `SPEC_CHANGE_APPROVED`, `KIT_ALLOW_TEST_CHANGE`, `KIT_ALLOW_TEST_DELETE`). Any change to a protected file, which includes `kit.py`, the hooks, `verify.config`, and CI, needs a human to commit it. The kickoff has three mandatory STOPs. Import needs approval.

**Cause 3: evidence is recorded one criterion at a time.** Each acceptance criterion needs its own `kit.py pass` with evidence. Five criteria means five commands and five pieces of evidence, plus a progress entry, `start`, `done`, and a commit. The evidence is typed by hand, so it is slow and easy to get wrong.

**Cause 4: "one feature per fresh session" in fast mode.** Each new feature starts a new chat that re-reads the brief, the plan, and the progress log. This is right for large features and wasteful for small ones.

**Cause 5: no traceability from criterion to test.** `pass` trusts a typed note. The kit never checks which test proves which criterion. This is slower to review and weaker as a guarantee at the same time.

## 3. The plan (ordered by time saved per change)

### S1. Auto-detect the test command at `init` (removes the biggest stall)
- At `init` and `doctor`, detect the stack and write the matching command to `verify.config`: `python3 -m unittest` / `pytest` for Python, `npm test` for Node, `go test ./...`, `cargo test`.
- `doctor` says exactly which line to add when detection fails, instead of a generic error.
- Effect: no manual edit for new projects. Existing projects get one command: `python3 scripts/kit.py config --test-cmd "..."`.
- Protected: `kit.py` and `verify.config` [HUMAN commits].

### S2. Criteria point to tests (replaces hand-typed evidence)
- A criterion can name its test, for example `test: tests/test_guards.py::TestDoneNeedsEvidence::test_done_fails_without_pass_evidence`.
- `verify.sh` writes a per-test result file (for example JUnit XML or `unittest` output parsed to test ids).
- `kit.py pass` checks that the named test ran and passed on the current commit. No typed evidence needed for those criteria.
- Manual criteria (UI, judgement) keep the typed evidence path.
- Effect: fewer commands, and a stronger guarantee: a criterion cannot pass without a named passing test.
- Protected: `kit.py` [HUMAN commits].

### S3. One command to finish a feature: `kit.py finish FEAT-x`
- Runs the gate, passes every criterion that has a passing named test, runs `done`, and appends a progress entry from the gate result.
- Stops with one clear message for any criterion that still needs a human.
- Effect: `start` + N×`pass` + `done` + progress becomes `start` and `finish`.
- Protected: `kit.py` [HUMAN commits].

### S4. Batch the human steps into one script
- `scripts/human-setup.sh` (human runs once): sets the test command, installs hooks, and commits the protected files with the admin switch. Prints what it changed.
- Effect: a human makes one trip instead of several, and the agent never sees the switch.
- Note: the script itself is protected; it is created by the human, not by an agent.

### S5. Kickoff with one approval stop in fast mode
- Keep the three stages for strict mode. In fast mode, show the three results together and stop once: "approve defaults" or "change X".
- Effect: three round trips become one.

### S6. Allow small features per session in fast mode
- Let `feature` take 2–3 features with a combined size limit (for example, under 5 criteria total). Keep one feature per session in strict mode.
- Effect: fewer fresh sessions and less re-reading. Measure it: count sessions per feature before and after.

### S7. Trim always-loaded context
- Move the longest parts of `docs/` out of the always-read set and load them by reference. Target: under 15 KB always loaded.
- Effect: less to read each session. Small gain; do it last.

## 4. Order of work and who does what
| Step | Who | Blocked on |
|---|---|---|
| S1, S2, S3 (code in `kit.py`) | Agent writes; human commits | Human commit with the admin switch |
| S4 | Human creates the script | Nothing |
| S5 | Agent | Human approval of the plan |
| S6 | Agent | S3 |
| S7 | Agent | Nothing |

Start with S4 and the one-time test-command setting: that alone unblocks FEAT-001 today. Then S1 and S3 make every later feature faster.

## 5. How we'll measure the speed-up
- Baseline: FEAT-001 took several sessions and is still open because of the gate. Record the sessions and human stops per feature from now on.
- Target per feature: one agent session, zero mid-feature human stops, and one human commit at the end if protected files changed.
- Track in `agent/progress.md`: human stops, sessions, and minutes per feature.

## 6. Risks of speeding it up
- **Auto-passing could hide real failures.** Mitigation: S2 requires the named test to pass on the current commit; S3 never passes a criterion without that.
- **Auto-detecting the test command can pick the wrong one.** Mitigation: `doctor` prints the chosen command and asks for confirmation.
- **Fewer human stops means less human review.** Mitigation: keep strict mode as it is; fast mode still blocks protected-file edits and still needs a human commit for them.
- **Batching features per session can cause drift.** Mitigation: the size cap in S6 and the brief at session start.

## 7. What I can build now without asking
- The plan document (this file).
- Nothing in `kit.py`, `verify.sh`, or `verify.config` until a human commits those files.
- After the test command is set: run FEAT-001's gate, pass its criteria, and mark it done, to test the current process end to end.
