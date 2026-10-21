# Roadmap: what gets built, in what order, and who does each step

Status: plan for review. Date of research: 2026-10-21.
Labels: [VERIFIED] read on the official page this session · [SECONDARY] third-party source only, confirm before relying on it · [OPEN] not documented, must be tested live · [HUMAN] only the human can do this (protected file or a business decision).

## 1. Where things stand
- Kit 4.1.0 is in the repo. The guard CLI (`scripts/kit.py`), gates (`scripts/verify.sh`), skills and hooks all exist.
- FEAT-001 (guard test suite): 6 tests written and passing, mutation-checked. Blocked: the gate needs `VERIFY_TEST` set in `scripts/verify.config` [HUMAN].
- FEAT-002 to FEAT-004: planned in `agent/features.json`. Not started (dependency on FEAT-001).
- Known issue KI-001: the guard flags test-fixture text that looks like a skipped test. Decision needed [HUMAN].
- No LICENSE file. No product decision on open versus paid [HUMAN].

## 2. What the research changed (the findings that alter the plan)

### 2.1 Gemini config is stale [VERIFIED]
- Google's Code Assist deprecation page says Gemini CLI stopped serving consumer tiers (Code Assist for individuals, AI Pro, AI Ultra) on 2026-06-18. Migration target: Antigravity CLI.
- The kit's `.gemini/settings.json` still uses the event key `BeforeTool`. That is the old format. Antigravity's documented event key is `PreToolUse`.
- Consequence: the Gemini integration no longer works for consumer users. It is replaced by an Antigravity integration (Phase 4).

### 2.2 Antigravity hooks [VERIFIED schema, OPEN behavior]
Official page: `antigravity.google/docs/hooks/`
- Workspace file: `.agents/hooks.json`. Global: `~/.gemini/config/hooks.json`. Plugin: the plugin's own `hooks.json` (CLI only). Precedence between them is not documented.
- Events: `SessionStart`, `PreToolUse`, `PostToolUse`, `PreInvocation`, `PostInvocation`, `Stop`.
- `PreToolUse` and `PostToolUse` take a `matcher` (regex; `""` or `"*"` matches all). Other events ignore the matcher.
- Handler: `type` (default `command`), `command` (required), `timeout` (seconds, default 30).
- Stdin payload for `PreToolUse`: `toolCall` (`name`, `args`), `stepIdx`, plus `conversationId`, `workspacePaths`, `transcriptPath`, `artifactDirectoryPath`, `modelName`.
- Block: stdout JSON `{"decision": "deny", "reason": "..."}`. Other decisions exist: `allow`, `auto_approve`, `ask`, `force_ask`, `deny_unless_prior_grant`.
- [OPEN] Exit codes, and whether a crashed or timed-out hook fails open or closed. Not documented. Must be tested in the real CLI before the adapter claims blocking.

### 2.3 Copilot CLI [VERIFIED]
Official: `docs.github.com/en/copilot/reference/copilot-cli-reference/cli-hooks-reference`
- Loads `.github/hooks/*.json` and requires `"version": 1`. The kit's `.github/hooks/kit-guard.json` already has this. Correct.
- `preToolUse` deny: stdout JSON `permissionDecision: "deny"` plus `permissionDecisionReason`. Exit code 2 also denies. Other non-zero exits fail closed. Timeout fails open.
- Also reads `.claude/settings.json` (hooks). Risk: the Claude guard could run twice under Copilot. [OPEN] confirm, and dedupe if real.
- The kit's `protect.py --agent copilot` emits the `permissionDecision` JSON. Matches the docs.

### 2.4 Codex CLI [VERIFIED, with a trust step]
Official: `learn.chatgpt.com/docs/hooks` (the developers.openai.com URLs now redirect there).
- Hooks load from `~/.codex/hooks.json`, `~/.codex/config.toml`, `<repo>/.codex/hooks.json`, `<repo>/.codex/config.toml`. Project hooks load only when the project `.codex/` layer is trusted.
- Non-managed hooks must be reviewed and trusted (`/hooks` in the CLI). Trust is tied to a hash of the hook, so any change makes it untrusted again. This means the installer must tell the user to trust the hook after every edit.
- Block: stdout `hookSpecificOutput` with `hookEventName: "PreToolUse"`, `permissionDecision: "deny"`, `permissionDecisionReason`. Also accepted: `decision: "block"` with `reason`. Exit code 2 with a stderr reason also blocks.
- Stdin fields for `PreToolUse`: `session_id`, `transcript_path`, `cwd`, `hook_event_name`, `model`, `turn_id`, `permission_mode`, `tool_name`, `tool_use_id`, `tool_input`.
- Impact: `protect.py --agent codex` must read `tool_input` (not Claude's shape). [OPEN] confirm the field names it reads actually match.
- The earlier claim that the Codex hook is "user-level only" came from the kit's own text. The official page shows project-level hooks are also supported, once trusted. Update the kit's text.

### 2.5 Claude Code [VERIFIED]
- `protect.py` blocks with exit code 2 and a message on stderr, which matches the docs.

### 2.6 OpenCode [VERIFIED docs, OPEN runtime]
- Plugins in `.opencode/plugins/` (project) or `~/.config/opencode/plugins/` (global), loaded at startup.
- `tool.execute.before(input, output)`: `input.tool`, `output.args`. Throwing blocks the call.
- [OPEN] whether the thrown error is shown to the agent, and whether `sessionID` exists. Not documented.

### 2.7 PR comments from forks [SECONDARY, consistent with GitHub's documented model]
- On a `pull_request` run from a fork, `GITHUB_TOKEN` is read-only and secrets are not passed. A comment step will fail there unless guarded.
- Do not use `pull_request_target` to check out untrusted code. That is the known way to leak secrets. Confirm against GitHub's official docs before implementing (the search did not return them).

## 3. Problems to solve (ranked by how much they block a real user)
1. **Trust is not enforced where it matters most.** Local hooks can be bypassed; CI is the only backstop, and only where it runs. Fix: make CI the required check and show the result on the PR (Phase 3).
2. **The guard can't be tested by its own rules.** It has no test suite until FEAT-001 passes the gate (Phase 1).
3. **Consumer Gemini users have no working integration.** Migrate to Antigravity (Phase 4).
4. **Setup is manual for Codex, and trust must be re-approved on every change.** Installer plus a clear trust step (Phase 5).
5. **The guard for file edits does not cover shell commands.** An agent can write a protected file through `bash`. Needs a shell-command check and its own tests (Phase 6).
6. **`protect.py` itself has no tests.** The hook that enforces everything is the least-tested file. Phase 6.
7. **False positive KI-001.** Decide and fix (Phase 1 or 6) [HUMAN decision].
8. **No evidence that it works.** The product claim ("fewer false done claims") is unmeasured. Phase 7.

## 4. Architecture (decided)
- Engine: `scripts/kit.py` and `protect.py`. One rule set, shared by every adapter.
- Adapters, one per agent, thin: Claude Code, Cursor, Copilot CLI (existing), Antigravity and OpenCode (new), Codex (existing, with installer).
- Backstop: CI workflow as the required check, plus a PR comment showing the evidence result. Fork-safe.
- Platform (dashboard, hosted GitHub App, billing): not started. Only after Phases 3 and 7 produce evidence.

## 5. Work packages

### Phase 1: finish FEAT-001 (guard test suite)
- Files: `tests/test_guards.py` (done).
- Remaining: set `VERIFY_TEST="python3 -m unittest discover -s tests"` [HUMAN, `scripts/verify.config`]; run `bash scripts/verify.sh`; then `kit.py pass` for AC-001-01..05 with evidence, `kit.py done FEAT-001`.
- Decide KI-001 [HUMAN]. If "exclude string literals in test files from the skip scan": implement in `kit.py` [HUMAN commits], add a test that a real skip is still caught.
- Done when: gate PASS, FEAT-001 done, no protected file changed by the agent.

### Phase 2: FEAT-002 OpenCode plugin
- Draft exists (scratch folder, matching logic checked in Node: 8/8 cases).
- Steps: install into `.opencode/plugins/kit-guard.js`; run OpenCode with the plugin loaded; attempt an edit to `scripts/kit.py` and confirm the call is blocked and the error reaches the agent; confirm an ordinary edit passes. Record results in `docs/decisions.md`.
- Protected-path list must match `PROTECTED` in `kit.py`. Add a test that compares the two lists, so they cannot drift.
- Known gap to document: shell commands (`bash`) are not checked by this plugin (see Phase 6).
- Done when: AC-002-01..03 pass in a live OpenCode run, not only in Node.

### Phase 3: FEAT-003 PR evidence comment (fork-safe)
- File: `.github/workflows/verify.yml` [HUMAN review; CI file].
- Design:
  - Trigger: `pull_request` (not `pull_request_target`).
  - Run `kit.py check` and `verify.sh`. The required status check is the pass/fail.
  - Comment step runs only when the head repo equals the base repo. Forks still get the status result, just no comment.
  - Comment is updated in place using a hidden marker, not re-posted on every push.
  - Permissions set per job: `pull-requests: write` only on the comment job.
- Done when: AC-003-01..03 pass on a same-repo PR and a fork PR (fork case: no failure, no comment, status still set).

### Phase 4: Antigravity adapter (replaces Gemini)
- New: `.agents/hooks.json` with `PreToolUse` matcher covering file-edit tools, command `python3 .claude/hooks/protect.py --agent antigravity`.
- `protect.py`: add `--agent antigravity` that prints `{"decision": "deny", "reason": ...}` on stdout.
- Remove or migrate `.gemini/settings.json` [HUMAN, protected file].
- Live test is mandatory [OPEN]: confirm the deny reaches the agent, and measure what happens on exit code 2, on a crash, and on a timeout. Document the result. Do not claim blocking until this is tested.
- Done when: a live Antigravity session is blocked from editing `scripts/kit.py`, and the fail-mode is recorded.

### Phase 5: Codex installer (FEAT-004)
- `kit.py hooks --install` [HUMAN, `kit.py` is protected]: writes the hook into `~/.codex/hooks.json` (merge, never overwrite; idempotent), shows the diff first, and tells the user to trust it with `/hooks`.
- Verify `protect.py --agent codex` reads `tool_input` correctly against the documented Codex payload. Add a test with a Codex-shaped payload.
- Done when: AC-004-01..03 pass; the trust step is in the output; a Codex session is blocked from editing a protected file.

### Phase 6: close the coverage gaps
- Shell-command check: block `bash`/`shell` commands that write to protected paths (redirects, `tee`, `sed -i`, `cp`, `mv`, `rm` on those files). Heuristic, so state that it's heuristic.
- Tests for `protect.py`: one test per agent payload shape (Claude, Cursor, Gemini→Antigravity, Copilot, Codex) and per decision format.
- Check for double-running hooks under Copilot (it also reads `.claude/settings.json`).
- Done when: each adapter has a test, and the shell-bypass cases are covered with a stated limit.

### Phase 7: prove it works (the evidence)
- Three real small projects. Same five features, built twice: agent alone, agent with the kit.
- Measure: false "done" claims, weakened or skipped tests, scope violations, protected-file attempts blocked, defects found in review.
- Publish the numbers in `docs/experiments/`, including the bad ones.
- Done when: the table exists and has been reviewed by someone other than the author.

### Phase 8: platform (only after Phase 3 and Phase 7 show value)
- Hosted GitHub App that runs the checks and stores evidence; web dashboard for teams; per-active-developer pricing to test.
- Not started. Needs a decision on hosting and open versus paid [HUMAN].

## 6. Human decisions and actions (I cannot do these)
| # | Item | Why only the human |
|---|---|---|
| H1 | Set `VERIFY_TEST` in `scripts/verify.config`, commit with the admin override | protected file |
| H2 | Decide KI-001 (ignore skip-like text in test files, or not) | product decision on guard behavior |
| H3 | Choose license and open versus paid split | business decision |
| H4 | Approve the Antigravity migration and remove `.gemini/settings.json` | protected file, and a user-visible change |
| H5 | Review `.github/workflows/verify.yml` and `kit.py` changes | protected files |
| H6 | Confirm merge strategy to `main` once the gate passes | outward-facing |
| H7 | Run the Phase 7 experiment time or supply the three projects | needs real projects and time |

## 7. Milestones
- M1: gate passes, FEAT-001 done (after H1, H2).
- M2: OpenCode blocking verified live (Phase 2).
- M3: PR evidence comment works on same-repo and fork PRs (Phase 3, after H5).
- M4: Antigravity and Codex blocking verified live, Gemini retired (Phases 4 and 5, after H4, H5).
- M5: shell-bypass coverage and `protect.py` tests (Phase 6).
- M6: experiment numbers published (Phase 7).
- M7: decision on the platform (Phase 8), based on M3 and M6.

## 8. Risks
- Agent vendors change hook formats. Mitigation: adapter tests run in CI against the documented payloads; re-verify each release.
- Fail-open behavior: a hook that times out lets the call through (Copilot and Antigravity documentation says so or is unclear). Mitigation: CI is the real gate; local hooks are convenience. Say this plainly to customers.
- Shell-command bypass is heuristic. Mitigation: state the limit; treat CI as the gate.
- Copilot may run the Claude hook as well. Mitigation: Phase 6 check.
- Market: Spec Kit and BMAD are free and far larger. The product must win on measured results, not features.

## 9. Sources
- Antigravity hooks (official): https://antigravity.google/docs/hooks/
- Copilot CLI hooks reference (official): https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-hooks-reference
- Codex hooks (official, via redirect): https://learn.chatgpt.com/docs/hooks
- Codex advanced config (official, via redirect): https://learn.chatgpt.com/docs/config-file/config-advanced
- Claude Code hooks (official): https://docs.anthropic.com/en/docs/claude-code/hooks
- OpenCode plugins (official): https://opencode.ai/docs/plugins/
- Gemini Code Assist deprecation (official): https://developers.google.com/gemini-code-assist/docs/deprecations/code-assist-individuals
- Spec-driven landscape (secondary): https://medium.com/@visrow/comprehensive-guide-to-spec-driven-development-kiro-github-spec-kit-and-bmad-method-5d28ff61b9b1
