# Architecture: {{PROJECT_NAME}}
Written during the kickoff; updated only when the structure changes. Keep it under ~150 lines.

## Stack and why
| Part | Choice | Why | Rejected (and why) |
|---|---|---|---|
| {{Language / runtime}} | | | |
| {{Framework}} | | | |
| {{Data store}} | | | |
| {{Auth}} | | | |
| {{Tests / lint}} | | | |
| {{Hosting}} | | | |

## Folder structure
```
{{tree with one-line purpose per folder}}
```
Layering: entry point -> service (rules) -> data. Modules import each other only through their public entry file.
Import rules that the gate enforces: docs/boundaries.txt.

## Reusable building blocks (build once, every feature uses them; agents check here before writing new code)
| Block | Where | Use it for |
|---|---|---|
| {{e.g. requireUser / requireRole}} | {{path}} | {{authorization in every entry point}} |
| {{e.g. validate(schema)}} | | {{input validation at the boundary}} |
| {{e.g. db / repository helpers}} | | {{all data access}} |
| {{e.g. apiClient, errors, logger}} | | |

## Runtime picture
```
{{who calls what: browser -> app -> db; background jobs; external APIs}}
```

## Data model
{{entities, key fields, constraints (unique / FK / not null), indexes for the filters and sorts the app uses}}

## Performance budget
{{expected scale (users, rows), page/endpoint targets (e.g. p95 < 300 ms), list page size max, bundle budget}}

## Authorization
{{where the check lives (one helper), what it returns, the role matrix lives in docs/product.md}}

## Key flows
{{the 2-4 flows where order, failure handling or concurrency matter}}

## Config and environment (validated at startup)
| Name | Purpose | Secret |
|---|---|---|

## Local development
{{exact commands to get from a fresh clone to a running app}}

## Build order
{{FEAT-001 walking skeleton first, then ...; which feature needs which external account/key}}

## Deployment
{{where it runs, how it is deployed, migrations, backups}}
