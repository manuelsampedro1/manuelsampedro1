from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "profile_quality_audit.py"

spec = importlib.util.spec_from_file_location("profile_quality_audit", MODULE_PATH)
assert spec is not None and spec.loader is not None
profile_quality_audit = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = profile_quality_audit
spec.loader.exec_module(profile_quality_audit)


class ProfileQualityAuditTests(unittest.TestCase):
    def test_current_profile_passes_quality_gate(self) -> None:
        result = profile_quality_audit.audit(ROOT)

        self.assertEqual(result.score, 100)
        self.assertEqual(result.issues, [])
        self.assertEqual(result.warnings, [])
        self.assertGreaterEqual(result.selected_work_rows, 45)

    def test_missing_reviewer_path_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "examples").mkdir()
            (root / "README.md").write_text(
                "\n".join(
                    [
                        "# Test Profile",
                        "",
                        "## Current Focus",
                        "",
                        "## Selected Work",
                        "",
                        "| Repo | What it proves | Why it matters |",
                        "| --- | --- | --- |",
                        "| [repo](https://example.com) | x | y |",
                        "",
                        "## Agent Safety Layer",
                        "",
                        "## How I Work With Codex",
                        "",
                        "## Public Workbench",
                        "",
                        "## Verify This Repo",
                        "",
                        "## Latest Proof",
                        "",
                        "## Principles",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            (root / "DECISIONS.md").write_text("", encoding="utf-8")
            (root / "TODO.md").write_text("", encoding="utf-8")
            (root / "examples" / "README.md").write_text("", encoding="utf-8")

            result = profile_quality_audit.audit(root)

        self.assertLess(result.score, 100)
        self.assertIn("README is missing required section: Reviewer Path.", result.issues)

    def test_verify_section_must_describe_real_gates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "examples").mkdir()
            (root / "README.md").write_text(
                "\n".join(
                    [
                        "# Test Profile",
                        "",
                        "## Current Focus",
                        "",
                        "## Reviewer Path",
                        "\n".join(profile_quality_audit.REVIEWER_PATH_TARGETS),
                        "",
                        "## Selected Work",
                        "",
                        "| Repo | What it proves | Why it matters |",
                        "| --- | --- | --- |",
                        "| [repo](https://example.com) | x | y |",
                        "",
                        "## Agent Safety Layer",
                        "",
                        "## How I Work With Codex",
                        "",
                        "## Public Workbench",
                        "",
                        "## Verify This Repo",
                        "The check validates shell scripts and indexes.",
                        "",
                        "## Latest Proof",
                        "",
                        "## Principles",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            (root / "DECISIONS.md").write_text("", encoding="utf-8")
            (root / "TODO.md").write_text("", encoding="utf-8")
            (root / "examples" / "README.md").write_text("", encoding="utf-8")

            result = profile_quality_audit.audit(root)

        self.assertIn("Verify This Repo is missing verification detail: python unit tests.", result.issues)
        self.assertIn("Verify This Repo is missing verification detail: python audit tools.", result.issues)
        self.assertIn("Verify This Repo is missing verification detail: commit-script shell fixture.", result.issues)
        self.assertIn("Verify This Repo is missing verification detail: profile quality audit.", result.issues)

    def test_saturated_selected_work_requires_curation_decision(self) -> None:
        rows = "\n".join(
            f"| [repo-{index}](https://example.com/{index}) | proof | why |"
            for index in range(45)
        )
        reviewer_path = "\n".join(profile_quality_audit.REVIEWER_PATH_TARGETS)

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            examples = root / "examples"
            examples.mkdir()
            (root / "README.md").write_text(
                "\n".join(
                    [
                        "# Test Profile",
                        "",
                        "## Current Focus",
                        "",
                        "## Reviewer Path",
                        reviewer_path,
                        "",
                        "## Selected Work",
                        "",
                        "| Repo | What it proves | Why it matters |",
                        "| --- | --- | --- |",
                        rows,
                        "",
                        "## Agent Safety Layer",
                        "",
                        "## How I Work With Codex",
                        "",
                        "## Public Workbench",
                        "",
                        "## Verify This Repo",
                        "",
                        "## Latest Proof",
                        "",
                        "## Principles",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            (root / "DECISIONS.md").write_text("", encoding="utf-8")
            (root / "TODO.md").write_text("", encoding="utf-8")
            (examples / "README.md").write_text(
                "\n".join(f"- [{Path(path).name}](./{Path(path).name})" for path in profile_quality_audit.REQUIRED_EXAMPLES),
                encoding="utf-8",
            )
            for path in profile_quality_audit.REQUIRED_EXAMPLES:
                (root / path).write_text("# Example\n", encoding="utf-8")
            (root / "examples" / "profile-evidence-map.md").write_text(
                "\n".join(profile_quality_audit.EVIDENCE_MAP_REPOS)
                + "\n"
                + "\n".join(
                    [
                        "agent-release-readiness-chain.md",
                        "agent-review-packet-to-ledger-chain.md",
                        "external-reviewer-navigation.md",
                        "profile-verification-proof-packet.md",
                        "profile-curation-guard-proof-packet.md",
                    ]
                ),
                encoding="utf-8",
            )

            result = profile_quality_audit.audit(root)

        self.assertIn("Selected Work is saturated but DECISIONS.md lacks the curation decision.", result.issues)
        self.assertIn("Selected Work is saturated but TODO.md lacks the pause-new-repo rule.", result.issues)


if __name__ == "__main__":
    unittest.main()
