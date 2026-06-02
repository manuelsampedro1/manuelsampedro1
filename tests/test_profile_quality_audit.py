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

    def test_reviewer_path_must_stay_short(self) -> None:
        reviewer_path = "\n".join(
            [
                *profile_quality_audit.REVIEWER_PATH_TARGETS,
                "- extra route",
                "- extra safety route",
                "- extra proof route",
                "- extra automation route",
                "- extra closing route",
            ]
        )

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
                        "| [repo](https://example.com) | x | y |",
                        "",
                        "## Agent Safety Layer",
                        "",
                        "## How I Work With Codex",
                        "",
                        "## Public Workbench",
                        "",
                        "## Verify This Repo",
                        "The check validates shell scripts, python audit tools, python unit tests, commit-script shell fixture, and profile quality audit.",
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

        self.assertIn(
            "Reviewer Path has 5 bullets; keep it at 4 or fewer for first-read clarity.",
            result.issues,
        )

    def test_readme_sections_must_keep_canonical_order(self) -> None:
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
                        "\n".join(profile_quality_audit.REVIEWER_PATH_TARGETS),
                        "",
                        "## Selected Work",
                        "",
                        "| Repo | What it proves | Why it matters |",
                        "| --- | --- | --- |",
                        "| [repo-a](https://github.com/manuelsampedro1/repo-a) | proof | why |",
                        "",
                        "## How I Work With Codex",
                        "",
                        "## Agent Safety Layer",
                        "",
                        "| Repo | What it proves | Why it matters |",
                        "| --- | --- | --- |",
                        "| [mcp-guard](https://github.com/manuelsampedro1/mcp-guard) | proof | why |",
                        "",
                        "## Public Workbench",
                        "",
                        "## Verify This Repo",
                        "The check validates shell scripts, python audit tools, python unit tests, commit-script shell fixture, and profile quality audit.",
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

        self.assertIn(
            "README section order is wrong: Agent Safety Layer must appear before How I Work With Codex.",
            result.issues,
        )

    def test_selected_work_duplicate_repo_target_fails(self) -> None:
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
                        "\n".join(profile_quality_audit.REVIEWER_PATH_TARGETS),
                        "",
                        "## Selected Work",
                        "",
                        "| Repo | What it proves | Why it matters |",
                        "| --- | --- | --- |",
                        "| [repo-a](https://github.com/manuelsampedro1/repo-a) | proof | why |",
                        "| [repo-a again](https://github.com/manuelsampedro1/repo-a) | proof | why |",
                        "",
                        "## Agent Safety Layer",
                        "",
                        "## How I Work With Codex",
                        "",
                        "## Public Workbench",
                        "",
                        "## Verify This Repo",
                        "The check validates shell scripts, python audit tools, python unit tests, commit-script shell fixture, and profile quality audit.",
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

        self.assertIn(
            "Selected Work contains duplicate repo target: https://github.com/manuelsampedro1/repo-a.",
            result.issues,
        )

    def test_selected_work_external_repo_target_fails(self) -> None:
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
                        "\n".join(profile_quality_audit.REVIEWER_PATH_TARGETS),
                        "",
                        "## Selected Work",
                        "",
                        "| Repo | What it proves | Why it matters |",
                        "| --- | --- | --- |",
                        "| [external](https://github.com/other/big-ai-project) | proof | why |",
                        "",
                        "## Agent Safety Layer",
                        "",
                        "## How I Work With Codex",
                        "",
                        "## Public Workbench",
                        "",
                        "## Verify This Repo",
                        "The check validates shell scripts, python audit tools, python unit tests, commit-script shell fixture, and profile quality audit.",
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

        self.assertIn(
            "Selected Work target is not an owned GitHub repo: https://github.com/other/big-ai-project.",
            result.issues,
        )

    def test_selected_work_label_must_match_repo_slug(self) -> None:
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
                        "\n".join(profile_quality_audit.REVIEWER_PATH_TARGETS),
                        "",
                        "## Selected Work",
                        "",
                        "| Repo | What it proves | Why it matters |",
                        "| --- | --- | --- |",
                        "| [friendly-name](https://github.com/manuelsampedro1/actual-repo) | proof | why |",
                        "",
                        "## Agent Safety Layer",
                        "",
                        "## How I Work With Codex",
                        "",
                        "## Public Workbench",
                        "",
                        "## Verify This Repo",
                        "The check validates shell scripts, python audit tools, python unit tests, commit-script shell fixture, and profile quality audit.",
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

        self.assertIn(
            "Selected Work label `friendly-name` does not match repo target `actual-repo`.",
            result.issues,
        )

    def test_agent_safety_layer_repo_targets_are_audited(self) -> None:
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
                        "\n".join(profile_quality_audit.REVIEWER_PATH_TARGETS),
                        "",
                        "## Selected Work",
                        "",
                        "| Repo | What it proves | Why it matters |",
                        "| --- | --- | --- |",
                        "| [repo-a](https://github.com/manuelsampedro1/repo-a) | proof | why |",
                        "",
                        "## Agent Safety Layer",
                        "",
                        "| Repo | What it proves | Why it matters |",
                        "| --- | --- | --- |",
                        "| [agent-secret-sentinel](https://github.com/manuelsampedro1/agent-secret-sentinel) | proof | why |",
                        "| [friendly-name](https://github.com/manuelsampedro1/mcp-guard) | proof | why |",
                        "| [external-tool](https://github.com/other/external-tool) | proof | why |",
                        "| [agent-secret-sentinel](https://github.com/manuelsampedro1/agent-secret-sentinel) | proof | why |",
                        "",
                        "## How I Work With Codex",
                        "",
                        "## Public Workbench",
                        "",
                        "## Verify This Repo",
                        "The check validates shell scripts, python audit tools, python unit tests, commit-script shell fixture, and profile quality audit.",
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

        self.assertIn(
            "Agent Safety Layer contains duplicate repo target: https://github.com/manuelsampedro1/agent-secret-sentinel.",
            result.issues,
        )
        self.assertIn(
            "Agent Safety Layer target is not an owned GitHub repo: https://github.com/other/external-tool.",
            result.issues,
        )
        self.assertIn(
            "Agent Safety Layer label `friendly-name` does not match repo target `mcp-guard`.",
            result.issues,
        )

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
