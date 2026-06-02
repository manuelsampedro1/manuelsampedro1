from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "audit_github_automation_prompts.py"

spec = importlib.util.spec_from_file_location("audit_github_automation_prompts", MODULE_PATH)
assert spec is not None and spec.loader is not None
automation_audit = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = automation_audit
spec.loader.exec_module(automation_audit)


def write_automation(root: Path, automation_id: str, prompt: str) -> None:
    automation_dir = root / automation_id
    automation_dir.mkdir(parents=True)
    (automation_dir / "automation.toml").write_text(
        "\n".join(
            [
                "version = 1",
                f'id = "{automation_id}"',
                f'prompt = "{prompt}"',
            ]
        ),
        encoding="utf-8",
    )


class GitHubAutomationPromptAuditTests(unittest.TestCase):
    def test_prompts_with_exact_path_contract_pass(self) -> None:
        prompt = (
            "Run scripts/commit_daily_update.sh with a concise message and pass the "
            "exact changed paths after the commit message."
        )
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for automation_id in automation_audit.EXPECTED_AUTOMATIONS:
                write_automation(root, automation_id, prompt)

            report = automation_audit.audit_root(root)

        self.assertEqual(report.issues, [])

    def test_missing_exact_path_contract_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for automation_id in automation_audit.EXPECTED_AUTOMATIONS:
                write_automation(root, automation_id, "Run scripts/commit_daily_update.sh with a concise message.")

            report = automation_audit.audit_root(root)

        self.assertIn(
            "github-ai-lab-note: prompt missing required fragment: exact",
            report.issues,
        )
        self.assertIn(
            "github-ai-recipe: prompt missing required fragment: after the commit message",
            report.issues,
        )

    def test_missing_automation_file_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report = automation_audit.audit_root(Path(tmp))

        self.assertIn(
            "github-profile-maintenance: missing "
            + str(Path(tmp) / "github-profile-maintenance" / "automation.toml"),
            report.issues,
        )


if __name__ == "__main__":
    unittest.main()
