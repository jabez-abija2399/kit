# Known issues (never delete; set Status from open to fixed with the commit)
| ID | Sev | Feature | Description | Repro | Workaround | Status | Next action |
|----|-----|---------|-------------|-------|------------|--------|-------------|
| KI-001 | medium | FEAT-001 | kit check flags test-skip patterns that appear as text inside test files (e.g. a fixture string containing `it.skip(`), so a guard test trips the guard | write a test fixture containing `it.skip(` and run kit.py check | build the literal by concatenation in the fixture | open | decide: exclude string literals in test files from the skip scan, or accept |
