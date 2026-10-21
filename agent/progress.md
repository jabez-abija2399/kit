# Progress (newest entry on top; <=8 lines per entry)

## YYYY-MM-DD | FEAT-xxx | status: in_progress | done
Changed (files + why; flag anything outside the plan):
Verified (command + result):
NOT VERIFIED:
Open questions for the human:
Next step:

## 2026-10-21 | FEAT-001 | status: in_progress | blocked on verify gate
Changed: tests/test_guards.py (6 tests, stdlib unittest, runs in throwaway copies of the kit); agent/known-issues.md (KI-001 guard false positive on test-fixture text).
Verified: python3 -m unittest discover -s tests -> 6 tests OK (this session). Mutation check: disabling the protected-file check fails test_editing_protected_kit_script_is_blocked; disabling the deleted-test check fails test_deleted_test_file_is_reported. kit.py check -> 0 errors.
NOT VERIFIED: scripts/verify.sh gate (VERIFY_TEST is empty in the protected verify.config), so kit.py pass / done cannot be recorded yet.
Open questions for the human: set VERIFY_TEST="python3 -m unittest discover -s tests" in scripts/verify.config (protected, human commits it); decide KI-001 (exclude string literals from the skip scan?).
Next step: after the gate passes, pass AC-001-01..05 and done FEAT-001; then FEAT-002/003 unlock (FEAT-004 needs a kit.py change).
