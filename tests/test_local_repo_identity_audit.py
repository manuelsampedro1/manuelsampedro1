from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "audit_local_repo_identity.py"

spec = importlib.util.spec_from_file_location("audit_local_repo_identity", MODULE_PATH)
assert spec is not None and spec.loader is not None
identity_audit = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = identity_audit
spec.loader.exec_module(identity_audit)


def init_repo(path: Path, name: str, email: str) -> None:
    path.mkdir()
    subprocess.run(["git", "-C", str(path), "init", "-q"], check=True)
    subprocess.run(["git", "-C", str(path), "config", "user.name", name], check=True)
    subprocess.run(["git", "-C", str(path), "config", "user.email", email], check=True)


class LocalRepoIdentityAuditTests(unittest.TestCase):
    def test_expected_identity_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_repo(root / "repo", identity_audit.EXPECTED_NAME, identity_audit.EXPECTED_EMAIL)

            report = identity_audit.audit_root(root)

        self.assertEqual(report.issues, [])
        self.assertEqual(len(report.results), 1)

    def test_wrong_identity_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_repo(root / "repo", "Local User", "local@example.com")

            report = identity_audit.audit_root(root)

        self.assertIn("user.name is 'Local User', expected 'Manuel Sampedro'", report.issues[0])
        self.assertIn("user.email is 'local@example.com'", "\n".join(report.issues))

    def test_repo_root_itself_is_audited(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_repo(root / "repo", identity_audit.EXPECTED_NAME, identity_audit.EXPECTED_EMAIL)

            report = identity_audit.audit_root(root / "repo")

        self.assertEqual(report.issues, [])
        self.assertEqual(len(report.results), 1)


if __name__ == "__main__":
    unittest.main()
