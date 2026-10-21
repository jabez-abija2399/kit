# Strategy: AI Build Kit as a business, and a YC application plan

Status: draft for the founder. Labels: [VERIFIED] checked in this session · [ASSUME] my assumption, test it · [FOUNDER] only you can supply this.

## 1. What the kit is today
- Version 4.1.0. A stdlib-only Python CLI (`scripts/kit.py`, ~91 KB) plus shell gates, skills for 10+ agent tools, and guard hooks.
- The core idea: AI coding agents claim "done" too early, game tests, drift from scope, invent packages, and read secrets. The kit enforces against that: protected files, evidence-gated "pass", no deleting or skipping tests, package dependency checks, and session briefs so a fresh chat knows where it stopped.
- [VERIFIED] Smoke-tested in this session: `init`, `doctor`, `check`, and the documented fresh-repo flow pass. Guards block an agent editing `scripts/kit.py` (exit: 1 error, correct behavior).
- [VERIFIED] Gaps found:
  - No LICENSE file. Nobody can legally use, fork or pay for it until one exists.
  - No test suite for `kit.py` itself, even though the product is "trust the guards". A guard product that is not tested by its own guards is the first thing a critic will attack.
  - Fresh projects fail `verify.sh --quick` until a test command is set. That is by design, but the first-run experience should say so in one line.
  - Codex guard only works from the user's home folder, so setup has a manual step.
  - Docs say "kit-owned" and "KIT block" in many places; some are stale against 4.1.0 (check with `kit.py doctor` after each release).

## 2. Market reality [VERIFIED via web search, Oct 2026; figures are third-party blog numbers, treat as indicative]
- GitHub Spec Kit: roughly 90k–115k stars by mid-2026. Free, works across Claude Code, Copilot, Gemini CLI, Cursor.
- BMAD-METHOD: roughly 45k–46k stars. Multi-agent, free.
- Kiro (AWS), OpenSpec, Tessl, Task Master, and many others. Cursor rules are the lightweight option.
- Most of these sell **process** (write a spec, then a plan, then tasks). Few sell **enforcement** (blocking an agent from marking its own work done).

**The defensible wedge is enforcement with evidence, not templates.** Templates are free and commoditized. "The agent cannot mark a feature done without a log of passing acceptance tests, and cannot edit the tests that judge it" is rarer. It is only worth money if we prove it.

## 3. The problem to solve (the thing people pay for)
[ASSUME] Teams using AI agents on real codebases lose time to: false "done" claims, tests quietly weakened to pass, scope creep, and rework after a fresh chat loses context. The cost is review time and production bugs.

The product should be sold on one measurable outcome: **fewer agent-introduced defects that reach review, per feature shipped**. Without that number, the kit is a free-template comparison and loses to Spec Kit.

## 4. Path to profit (pick one lead, validate it in 30 days)
| Option | Who pays | Why it could work | Main risk |
|---|---|---|---|
| A. Team license for enforcement + CI guard | Engineering leads at 10–200 person companies using agents | Clear budget, clear pain, guards map to compliance | Long sales cycle; security reviews |
| B. Paid "strict mode" pack (evaluator sessions, held-out acceptance tests, audit reports) | Solo founders and small agencies shipping client work | Fast to sell, low support | Small ticket size |
| C. Consulting/setup for agencies, productized | Agencies building for clients | Revenue in weeks | Does not scale; not what YC funds |

[ASSUME] Start with B to get the first 10 paying users fast, use their failures to make the evidence for A. Test this, don't trust it.

Pricing hypotheses to test (not facts): free open-source core with the guards; paid pack around USD 19–49/month per seat for strict mode and reports; team plan with a CI backstop and audit log. [FOUNDER] decide the open/closed split.

## 5. The 30-day validation plan
1. **Add a LICENSE and fix the self-test gap.** Write tests for the guards (`kit.py check`, the protected-file logic, the pass/done evidence rules). This is cheap and makes the product credible.
2. **Build the proof.** Take 3 real small projects. Build the same 5 features twice: once with an agent alone, once with the kit. Count: false "done" claims, tests weakened, scope violations, defects found in review. Publish the numbers, good or bad. This is the single most important artifact, for customers and for YC.
3. **Talk to 15 users** who already use AI coding agents on paid work. Ask what they lost time on last week. Do not pitch first. Record exact phrases.
4. **Put a paid offer in front of 10 of them** (a pre-order or a pilot fee). If none pays, the wedge is wrong; change it before building more.
5. **Decide** at day 30 using the pilot numbers, not opinions.

## 6. YC application: what to do and what it needs
- [VERIFIED] Sources in this session say the Summer 2026 deadline (May 4) and Fall 2026 deadline (July 27) have **already passed** as of today (2026-10-21). Sources disagree on batch count. Check `apply.ycombinator.com` for the next batch and deadline before planning around any date.
- [VERIFIED] YC's form asks for founders, the company, what you are building, traction, and a short video. The exact question list changes each batch, so copy it from the live form, not from this doc.
- Realistic positioning: YC funds early traction and a founder who moves fast, not a finished product. The 30-day plan above is what turns this into a story: a named problem, a measured result, and paying or pilot users.

### Draft answers (replace bracketed items with facts; do not submit made-up numbers)
- **What are you building?** A guard layer that stops AI coding agents from declaring their own work done, weakening their own tests, or drifting out of scope, with evidence required for every "done".
- **Why now?** [FOUNDER] Agent use on paid code is growing, and agents' failure mode (confident false completion) is now the bottleneck, not generation speed.
- **Who has the problem?** [FOUNDER] Name 3 people or teams you spoke to, and what they lost time on, in their words.
- **What is your traction?** [FOUNDER] Pilot users, paying users, revenue, repo stars, and the defect-reduction numbers from step 2 above. If zero, say zero and state the next milestone.
- **Why you?** [FOUNDER] Your own history building with agents, and why you noticed the enforcement gap.
- **Competition?** Spec Kit, BMAD, Kiro, OpenSpec: free, process-focused, and they do not block the agent. Our difference is enforcement and measured evidence. Say it in one line; do not dismiss them.
- **Video:** 60 seconds: show the agent claiming "done", the guard blocking it, and the number from the experiment.

## 7. Risks, stated plainly
- **Platform risk:** the agent vendors could build enforcement into their own tools. Mitigation: be the cross-agent, measured layer, and move fast on evidence.
- **Hooks are fragile:** guards depend on each agent's hook system, which changes. Mitigation: keep the CI backstop as the real enforcement; the local hooks are convenience.
- **Honest limit already in the kit's own docs:** guards "don't judge whether code is good". Do not sell it as a quality guarantee. Sell it as "no false completion and no gamed tests", and back that with the experiment.
- **Not legal advice:** license choice, terms, and any paid-tier contracts need a lawyer before revenue.

## 8. Next concrete steps (in order)
1. Choose the license and the open/closed split. [FOUNDER]
2. Add guard tests for `kit.py` (the first engineering task).
3. Run the 3-project experiment and record the numbers in `docs/experiments/`.
4. Book 15 user conversations.
5. Re-check the YC batch dates on the live site and draft the application from section 6 with real numbers.
