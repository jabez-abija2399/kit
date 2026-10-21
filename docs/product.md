# Product: {{PROJECT_NAME}}
Written during the kickoff. Labels: [USER] user requirement · [TECH] technical requirement · [ASSUME] assumption ·
[OPEN] open question (each [OPEN] has a recommended default so the human can answer "approve defaults").

## Purpose
- [USER] {{What result do users want, in one or two sentences? Why would they pick this over the alternative?}}
- Users: {{who, and in what situation}}

## Core flows (the whole first version; numbered, each one testable end to end)
1. {{...}}

## Requirements (each maps to features in agent/features.json; `kit.py check` fails on an unmapped requirement)
| ID | Label | Requirement |
|----|-------|-------------|
| REQ-001 | [USER] | {{...}} |

## Scope
In: agent/features.json. Nothing else.
Out (parked in agent/later.md): {{the things deliberately cut, so nobody builds them by accident}}

## Roles and permissions (delete if single-user)
| Action | {{Role A}} | {{Role B}} |
|---|---|---|

## Business rules (never violated; each one becomes a criterion or a project rule in AGENTS.md)
- {{e.g. [USER] Data is private by default}}

## Assumptions and open questions
- [ASSUME] {{...}}
- [OPEN] {{question}} Default: {{recommended answer}}

## Success criteria (numbers)
- {{e.g. a new user finishes the core flow in under 5 minutes}}
