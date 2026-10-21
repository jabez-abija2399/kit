"""Tests for the guards in scripts/kit.py (FEAT-001).

Each test copies the kit into a throwaway git repo and drives kit.py there,
so nothing here touches the kit repo itself. Standard library only.
Run: python3 -m unittest discover -s tests -v
"""
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

KIT = Path(__file__).resolve().parent.parent
GIT_ENV = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@example.com",
               GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@example.com")


def git(repo, *args):
    return subprocess.run(["git", "-c", "core.hooksPath=/dev/null", *args], cwd=repo,
                          capture_output=True, text=True, env=GIT_ENV)


def kit(repo, *args):
    """Run kit.py inside the scratch repo. Returns (exit code, combined output)."""
    r = subprocess.run(["python3", "scripts/kit.py", *args], cwd=repo,
                       capture_output=True, text=True, env=GIT_ENV)
    return r.returncode, r.stdout + r.stderr


class ScratchRepo(unittest.TestCase):
    """A fresh copy of the kit, committed once as the baseline."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="kit-test-"))
        self.repo = self.tmp / "project"
        shutil.copytree(KIT, self.repo, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        (self.repo / "agent" / "features.json").write_text('{"requirements": [], "features": []}\n')
        git(self.repo, "init", "-q")
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-q", "-m", "chore: add AI build kit")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def write(self, rel, text):
        p = self.repo / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)


class TestCleanInstall(ScratchRepo):
    def test_fresh_install_passes_check(self):
        code, out = kit(self.repo, "check")
        self.assertEqual(code, 0, out)
        self.assertIn("0 error(s)", out)


class TestProtectedFiles(ScratchRepo):
    def test_editing_protected_kit_script_is_blocked(self):
        with open(self.repo / "scripts" / "kit.py", "a") as f:
            f.write("\n# agent edit\n")
        code, out = kit(self.repo, "check")
        self.assertNotEqual(code, 0, out)
        self.assertIn("protected guard file changed", out)


class TestDoneNeedsEvidence(ScratchRepo):
    def test_done_fails_without_pass_evidence(self):
        code, out = kit(self.repo, "import", "agent/plan.example.json")
        self.assertEqual(code, 0, out)
        code, out = kit(self.repo, "start", "FEAT-001")
        self.assertEqual(code, 0, out)
        code, out = kit(self.repo, "done", "FEAT-001")
        self.assertNotEqual(code, 0, out)
        self.assertIn("cannot be marked done", out)


class TestTestTampering(ScratchRepo):
    def test_deleted_test_file_is_reported(self):
        self.write("tests/test_math.py", "def test_add():\n    assert 1 + 1 == 2\n")
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-q", "-m", "add test")
        git(self.repo, "rm", "-q", "tests/test_math.py")
        code, out = kit(self.repo, "check")
        self.assertNotEqual(code, 0, out)
        self.assertIn("test file deleted", out)

    def test_added_skip_is_reported(self):
        self.write("tests/math.test.js", "it('adds', () => { expect(1 + 1).toBe(2); });\n")
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-q", "-m", "add test")
        # Built by concatenation so this test file does not itself contain the skip pattern.
        skipped = "it" + "." + "skip" + "('adds', () => { expect(1 + 1).toBe(2); });\n"
        self.write("tests/math.test.js", skipped)
        code, out = kit(self.repo, "check")
        self.assertNotEqual(code, 0, out)
        self.assertIn("added test skip/disable", out)


class TestUnrecordedPackage(ScratchRepo):
    def test_new_dependency_without_record_is_blocked(self):
        self.write("package.json", '{"name": "app", "dependencies": {}}\n')
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-q", "-m", "add manifest")
        self.write("package.json", '{"name": "app", "dependencies": {"left-pad": "1.3.0"}}\n')
        code, out = kit(self.repo, "check")
        self.assertNotEqual(code, 0, out)
        self.assertIn("new dependency 'left-pad' has no entry", out)


if __name__ == "__main__":
    unittest.main()
