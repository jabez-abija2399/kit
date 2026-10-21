# Design contract: {{PROJECT_NAME}}   (delete this file if the project has no UI)
Short on purpose: use one component library as-is; spend design effort only on the key screens.

## Direction: "{{name}}"
{{2-3 lines: the feeling, what it must NOT feel like, 2-3 reference products}}

## Tokens (CSS variables / theme file: {{path}}; never hard-code colors)
--bg · --surface · --border · --text · --muted · --accent · --success · --warning · --danger
Dark mode: {{values or "not in v1"}}. Font: {{UI font + mono}}. Radius {{n}} px. Spacing scale 4/8/12/16/24/32.

## Component inventory (build each once, reuse everywhere; add a row before creating a new shared component)
| Component | Path | Variants / props | Used by |
|---|---|---|---|
| {{Button}} | {{src/components/ui/button}} | {{primary, secondary, danger; loading}} | |
| {{Form field + error}} | | | |
| {{Data table with empty/loading/error}} | | | |
| {{Dialog / confirm}} | | | |

## The screens that matter (max 3; polish these, everything else is plain components)
1. {{screen: what is on it, the one primary action}}

## Rules
- Status is never color alone: icon + label.
- Every async action: loading, success feedback, error message that says what to do next.
- Empty states have one clear button. Destructive actions need confirmation.
- Check at 375 px and 1280 px. Keyboard: Tab order, visible focus ring, labels on all inputs.
- Anti-patterns: {{what to avoid, e.g. gradients, more than one primary button per view}}
