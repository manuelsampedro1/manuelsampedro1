from __future__ import annotations

import importlib.util
import os
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

    def test_profile_intro_must_keep_positioning_and_cta(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "examples").mkdir()
            (root / "README.md").write_text(
                "\n".join(
                    [
                        "# Generic Builder",
                        "",
                        "I make software and AI demos.",
                        "",
                        "Find me online.",
                        "",
                        "## Current Focus",
                        "",
                        "## Reviewer Path",
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

        self.assertIn("README heading must be `# Manuel Sampedro`.", result.issues)
        self.assertIn("README intro is missing positioning phrase: agentic engineering tools.", result.issues)
        self.assertIn("README intro is missing positioning phrase: coding agents.", result.issues)
        self.assertIn(
            "README intro is missing positioning phrase: scoped, inspectable, and easier to trust.",
            result.issues,
        )
        self.assertIn(
            "README intro is missing public CTA target: https://x.com/manuelsampedrop.",
            result.issues,
        )

    def test_public_surface_rejects_external_validation_phrases(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "labs" / "2026").mkdir(parents=True)
            (root / "README.md").write_text("# Test Profile\n", encoding="utf-8")
            (root / "labs" / "2026" / "note.md").write_text(
                "This public note says they need to give me the prize.\n",
                encoding="utf-8",
            )

            result = profile_quality_audit.audit(root)

        self.assertIn(
            "Public surface contains external-validation or approval-chasing phrase `give me the prize` in labs/2026/note.md.",
            result.issues,
        )

    def test_public_surface_rejects_approval_chasing_phrases(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "recipes").mkdir()
            (root / "docs").mkdir()
            (root / "README.md").write_text("# Test Profile\n", encoding="utf-8")
            (root / "recipes" / "note.md").write_text(
                "A weak request says make reviewers approve this. It treats the profile as an approval signal.\n",
                encoding="utf-8",
            )
            (root / "docs" / "profile-strategy.md").write_text(
                "This doc should not say give me the award.\n",
                encoding="utf-8",
            )

            result = profile_quality_audit.audit(root)

        self.assertIn(
            "Public surface contains external-validation or approval-chasing phrase `make reviewers approve this` in recipes/note.md.",
            result.issues,
        )
        self.assertIn(
            "Public surface contains external-validation or approval-chasing phrase `approval signal` in recipes/note.md.",
            result.issues,
        )
        self.assertIn(
            "Public surface contains external-validation or approval-chasing phrase `give me the award` in docs/profile-strategy.md.",
            result.issues,
        )

    def test_public_surface_rejects_missing_relative_links(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "labs" / "2026").mkdir(parents=True)
            (root / "README.md").write_text("# Test Profile\n", encoding="utf-8")
            (root / "labs" / "2026" / "note.md").write_text(
                "See [missing recipe](../../recipes/missing.md).\n",
                encoding="utf-8",
            )

            result = profile_quality_audit.audit(root)

        self.assertIn(
            "Public surface relative link is missing in labs/2026/note.md: ../../recipes/missing.md.",
            result.issues,
        )

    def test_public_surface_relative_links_ignore_code_examples(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "labs" / "2026").mkdir(parents=True)
            (root / "README.md").write_text("# Test Profile\n", encoding="utf-8")
            (root / "labs" / "2026" / "note.md").write_text(
                "The upstream README contains `![Preview](docs/preview.svg)`.\n",
                encoding="utf-8",
            )

            result = profile_quality_audit.audit(root)

        self.assertNotIn(
            "Public surface relative link is missing in labs/2026/note.md: docs/preview.svg.",
            result.issues,
        )

    def test_public_surface_markdown_must_have_one_page_h1(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "recipes").mkdir()
            (root / "README.md").write_text("# Test Profile\n", encoding="utf-8")
            (root / "recipes" / "note.md").write_text(
                "# First Title\n\nSome useful body.\n\n# Second Title\n",
                encoding="utf-8",
            )

            result = profile_quality_audit.audit(root)

        self.assertIn(
            "Public surface Markdown has 2 page H1 headings in recipes/note.md; keep exactly one.",
            result.issues,
        )

    def test_public_surface_h1_audit_ignores_code_examples(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "recipes").mkdir()
            (root / "README.md").write_text("# Test Profile\n", encoding="utf-8")
            (root / "recipes" / "note.md").write_text(
                "\n".join(
                    [
                        "# Real Recipe Title",
                        "",
                        "```md",
                        "# Template Title",
                        "```",
                        "",
                    ]
                ),
                encoding="utf-8",
            )

            result = profile_quality_audit.audit(root)

        self.assertNotIn(
            "Public surface Markdown has 2 page H1 headings in recipes/note.md; keep exactly one.",
            result.issues,
        )

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
        self.assertIn("Verify This Repo is missing verification detail: latest-proof freshness.", result.issues)

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

    def test_reviewer_path_rejects_unapproved_targets(self) -> None:
        reviewer_path = "\n".join(
            [
                *profile_quality_audit.REVIEWER_PATH_TARGETS,
                "- Extra route: [extra-proof](https://github.com/manuelsampedro1/extra-proof)",
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
                        "| [repo-a](https://github.com/manuelsampedro1/repo-a) | proof | why |",
                        "",
                        "## Agent Safety Layer",
                        "",
                        "| Repo | What it proves | Why it matters |",
                        "| --- | --- | --- |",
                        "| [mcp-guard](https://github.com/manuelsampedro1/mcp-guard) | proof | why |",
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
            "Reviewer Path contains unapproved target: https://github.com/manuelsampedro1/extra-proof.",
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

    def test_focus_and_workbench_must_keep_profile_narrative(self) -> None:
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
                        "- Agent reliability and verification discipline.",
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
                        "| [mcp-guard](https://github.com/manuelsampedro1/mcp-guard) | proof | why |",
                        "",
                        "## How I Work With Codex",
                        "",
                        "## Public Workbench",
                        "- [AI lab notes](./labs/README.md)",
                        "- [Recipes](./recipes/README.md)",
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

        self.assertIn("Current Focus is missing narrative anchor: agent auditability.", result.issues)
        self.assertIn("Current Focus is missing narrative anchor: agent safety.", result.issues)
        self.assertIn("Current Focus is missing narrative anchor: product judgment.", result.issues)
        self.assertIn("Public Workbench is missing target: ./examples/README.md.", result.issues)
        self.assertIn("Public Workbench is missing target: ./radar/README.md.", result.issues)
        self.assertIn("Public Workbench is missing target: ./docs/README.md.", result.issues)
        self.assertIn("Public Workbench is missing target: ./docs/automation-runbook.md.", result.issues)

    def test_current_focus_must_stay_five_bullets(self) -> None:
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
                        "- Agent reliability.",
                        "- Verification discipline.",
                        "- Agent auditability.",
                        "- Agent safety.",
                        "- Product judgment.",
                        "- Extra focus that belongs in a recipe or example.",
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
                        "| [mcp-guard](https://github.com/manuelsampedro1/mcp-guard) | proof | why |",
                        "",
                        "## How I Work With Codex",
                        "",
                        "## Public Workbench",
                        "- [AI lab notes](./labs/README.md)",
                        "- [Recipes](./recipes/README.md)",
                        "- [Examples](./examples/README.md)",
                        "- [Tooling radar](./radar/README.md)",
                        "- [Automation runbook](./docs/automation-runbook.md)",
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
            "Current Focus has 6 bullets; keep exactly 5 first-read focus bullets.",
            result.issues,
        )

    def test_how_i_work_section_must_not_keep_growing(self) -> None:
        workflow_bullets = "\n".join(
            f"- Workflow route {index}"
            for index in range(profile_quality_audit.MAX_HOW_I_WORK_BULLETS + 1)
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
                        "- Agent reliability.",
                        "- Verification discipline.",
                        "- Agent auditability.",
                        "- Agent safety.",
                        "- Product judgment.",
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
                        "| [mcp-guard](https://github.com/manuelsampedro1/mcp-guard) | proof | why |",
                        "",
                        "## How I Work With Codex",
                        workflow_bullets,
                        "",
                        "## Public Workbench",
                        "- [AI lab notes](./labs/README.md)",
                        "- [Recipes](./recipes/README.md)",
                        "- [Examples](./examples/README.md)",
                        "- [Tooling radar](./radar/README.md)",
                        "- [Automation runbook](./docs/automation-runbook.md)",
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
            "How I Work With Codex has 19 bullets; keep it at 18 or fewer and move extra routes to recipes or examples.",
            result.issues,
        )

    def test_latest_proof_targets_must_be_indexed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            examples = root / "examples"
            labs = root / "labs"
            lab_year = labs / "2026"
            examples.mkdir()
            lab_year.mkdir(parents=True)
            (root / "recipes").mkdir()
            (root / "radar").mkdir()
            latest_lab = "2026-06-03-unindexed-proof.md"
            (lab_year / latest_lab).write_text("# Unindexed Proof\n", encoding="utf-8")
            (labs / "README.md").write_text("# AI Lab Notes\n\n## Entries\n\n", encoding="utf-8")
            (root / "recipes" / "README.md").write_text("# Recipes\n", encoding="utf-8")
            (root / "radar" / "README.md").write_text("# Tooling Radar\n", encoding="utf-8")
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
                        "| [mcp-guard](https://github.com/manuelsampedro1/mcp-guard) | proof | why |",
                        "",
                        "## How I Work With Codex",
                        "",
                        "## Public Workbench",
                        "",
                        "## Verify This Repo",
                        "The check validates shell scripts, python audit tools, python unit tests, commit-script shell fixture, and profile quality audit.",
                        "",
                        "## Latest Proof",
                        f"- Latest lab note: [Unindexed Proof](./labs/2026/{latest_lab})",
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
            f"Latest Proof target is not indexed in labs/README.md: ./labs/2026/{latest_lab}.",
            result.issues,
        )

    def test_latest_proof_must_keep_one_lab_and_three_recipes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            examples = root / "examples"
            labs = root / "labs"
            lab_year = labs / "2026"
            recipes = root / "recipes"
            radar = root / "radar"
            examples.mkdir()
            lab_year.mkdir(parents=True)
            recipes.mkdir()
            radar.mkdir()
            latest_lab = "2026-06-03-shape-proof.md"
            recipe_names = ["shape-one.md", "shape-two.md"]
            (lab_year / latest_lab).write_text("# Shape Proof\n", encoding="utf-8")
            for recipe_name in recipe_names:
                (recipes / recipe_name).write_text("# Recipe\n", encoding="utf-8")
            (labs / "README.md").write_text(f"- [{latest_lab}](./2026/{latest_lab})\n", encoding="utf-8")
            (recipes / "README.md").write_text(
                "\n".join(f"- [{recipe_name}](./{recipe_name})" for recipe_name in recipe_names),
                encoding="utf-8",
            )
            (radar / "README.md").write_text("# Tooling Radar\n", encoding="utf-8")
            (root / "README.md").write_text(
                "\n".join(
                    [
                        "# Test Profile",
                        "",
                        "## Current Focus",
                        "- Agent reliability.",
                        "- Verification discipline.",
                        "- Agent auditability.",
                        "- Agent safety.",
                        "- Product judgment.",
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
                        "| [mcp-guard](https://github.com/manuelsampedro1/mcp-guard) | proof | why |",
                        "",
                        "## How I Work With Codex",
                        "",
                        "## Public Workbench",
                        "- [AI lab notes](./labs/README.md)",
                        "- [Recipes](./recipes/README.md)",
                        "- [Examples](./examples/README.md)",
                        "- [Tooling radar](./radar/README.md)",
                        "- [Automation runbook](./docs/automation-runbook.md)",
                        "",
                        "## Verify This Repo",
                        "The check validates shell scripts, python audit tools, python unit tests, commit-script shell fixture, and profile quality audit.",
                        "",
                        "## Latest Proof",
                        f"- Latest lab note: [Shape Proof](./labs/2026/{latest_lab})",
                        f"- Latest recipe: [Shape One](./recipes/{recipe_names[0]})",
                        f"- Latest recipe: [Shape Two](./recipes/{recipe_names[1]})",
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
            "Latest Proof has 3 indexed lab, recipe, or radar links; keep exactly 4.",
            result.issues,
        )
        self.assertIn(
            "Latest Proof must include exactly 3 link(s) under ./recipes/; found 2.",
            result.issues,
        )

    def test_latest_proof_must_match_newest_public_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            examples = root / "examples"
            labs = root / "labs"
            lab_year = labs / "2026"
            recipes = root / "recipes"
            radar = root / "radar"
            examples.mkdir()
            lab_year.mkdir(parents=True)
            recipes.mkdir()
            radar.mkdir()

            old_lab = lab_year / "2026-06-03-old-proof.md"
            new_lab = lab_year / "2026-06-03-new-proof.md"
            old_lab.write_text("# Old Proof\n", encoding="utf-8")
            new_lab.write_text("# New Proof\n", encoding="utf-8")
            os.utime(old_lab, (1_000, 1_000))
            os.utime(new_lab, (2_000, 2_000))

            recipe_times = {
                "old-one.md": 1_000,
                "old-two.md": 1_100,
                "old-three.md": 1_200,
                "new-one.md": 2_300,
                "new-two.md": 2_200,
                "new-three.md": 2_100,
            }
            for recipe_name, timestamp in recipe_times.items():
                recipe_path = recipes / recipe_name
                recipe_path.write_text(f"# {recipe_name}\n", encoding="utf-8")
                os.utime(recipe_path, (timestamp, timestamp))

            (labs / "README.md").write_text(
                "\n".join(
                    [
                        f"- [Old Proof](./2026/{old_lab.name})",
                        f"- [New Proof](./2026/{new_lab.name})",
                    ]
                ),
                encoding="utf-8",
            )
            (recipes / "README.md").write_text(
                "\n".join(f"- [{recipe_name}](./{recipe_name})" for recipe_name in recipe_times),
                encoding="utf-8",
            )
            (radar / "README.md").write_text("# Tooling Radar\n", encoding="utf-8")
            (root / "README.md").write_text(
                "\n".join(
                    [
                        "# Test Profile",
                        "",
                        "## Current Focus",
                        "- Agent reliability.",
                        "- Verification discipline.",
                        "- Agent auditability.",
                        "- Agent safety.",
                        "- Product judgment.",
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
                        "| [mcp-guard](https://github.com/manuelsampedro1/mcp-guard) | proof | why |",
                        "",
                        "## How I Work With Codex",
                        "",
                        "## Public Workbench",
                        "- [AI lab notes](./labs/README.md)",
                        "- [Recipes](./recipes/README.md)",
                        "- [Examples](./examples/README.md)",
                        "- [Tooling radar](./radar/README.md)",
                        "- [Automation runbook](./docs/automation-runbook.md)",
                        "",
                        "## Verify This Repo",
                        "The check validates shell scripts, python audit tools, python unit tests, commit-script shell fixture, and profile quality audit.",
                        "",
                        "## Latest Proof",
                        f"- Latest lab note: [Old Proof](./labs/2026/{old_lab.name})",
                        "- Latest recipes:",
                        "  - [Old One](./recipes/old-one.md)",
                        "  - [Old Two](./recipes/old-two.md)",
                        "  - [Old Three](./recipes/old-three.md)",
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
            "Latest Proof targets are stale for ./labs/: expected ./labs/2026/2026-06-03-new-proof.md; found ./labs/2026/2026-06-03-old-proof.md.",
            result.issues,
        )
        self.assertIn(
            "Latest Proof targets are stale for ./recipes/: expected ./recipes/new-one.md, ./recipes/new-two.md, ./recipes/new-three.md; found ./recipes/old-one.md, ./recipes/old-two.md, ./recipes/old-three.md.",
            result.issues,
        )

    def test_public_indexes_must_link_every_markdown_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            docs = root / "docs"
            examples = root / "examples"
            docs.mkdir()
            examples.mkdir()
            (root / "README.md").write_text(
                "\n".join(
                    [
                        "# Test Profile",
                        "",
                        "## Current Focus",
                        "",
                        "## Reviewer Path",
                        "",
                        "## Selected Work",
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
            (docs / "README.md").write_text("# Docs\n\n## Entries\n", encoding="utf-8")
            (docs / "hidden-runbook.md").write_text("# Hidden Runbook\n", encoding="utf-8")
            (examples / "README.md").write_text(
                "\n".join(f"- [{Path(path).name}](./{Path(path).name})" for path in profile_quality_audit.REQUIRED_EXAMPLES),
                encoding="utf-8",
            )
            for path in profile_quality_audit.REQUIRED_EXAMPLES:
                (root / path).write_text("# Example\n", encoding="utf-8")
            (examples / "unindexed-proof.md").write_text("# Unindexed Proof\n", encoding="utf-8")
            (examples / "profile-evidence-map.md").write_text(
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
            "docs/README.md does not link public Markdown file: docs/hidden-runbook.md.",
            result.issues,
        )
        self.assertIn(
            "examples/README.md does not link public Markdown file: examples/unindexed-proof.md.",
            result.issues,
        )

    def test_profile_evidence_map_requires_canonical_repo_links(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            examples = root / "examples"
            examples.mkdir()
            (root / "README.md").write_text("# Test Profile\n", encoding="utf-8")
            (root / "DECISIONS.md").write_text("", encoding="utf-8")
            (root / "TODO.md").write_text("", encoding="utf-8")
            (examples / "README.md").write_text(
                "\n".join(f"- [{Path(path).name}](./{Path(path).name})" for path in profile_quality_audit.REQUIRED_EXAMPLES),
                encoding="utf-8",
            )
            for path in profile_quality_audit.REQUIRED_EXAMPLES:
                (root / path).write_text("# Example\n", encoding="utf-8")
            (examples / "profile-evidence-map.md").write_text(
                "# Profile Evidence Map\n\n"
                + "\n".join(profile_quality_audit.EVIDENCE_MAP_REPOS)
                + "\nagent-release-readiness-chain.md\n"
                + "agent-review-packet-to-ledger-chain.md\n"
                + "external-reviewer-navigation.md\n"
                + "profile-verification-proof-packet.md\n"
                + "profile-curation-guard-proof-packet.md\n",
                encoding="utf-8",
            )

            result = profile_quality_audit.audit(root)

        self.assertIn(
            "Profile evidence map is missing canonical repo link: https://github.com/manuelsampedro1/agent-start-gate.",
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

    def test_primary_repo_tables_must_link_repo_roots(self) -> None:
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
                        "| [repo-a](https://github.com/manuelsampedro1/repo-a/tree/main/docs) | proof | why |",
                        "",
                        "## Agent Safety Layer",
                        "",
                        "| Repo | What it proves | Why it matters |",
                        "| --- | --- | --- |",
                        "| [mcp-guard](https://github.com/manuelsampedro1/mcp-guard/issues) | proof | why |",
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
            "Selected Work target should point to repo root `https://github.com/manuelsampedro1/repo-a`, not `https://github.com/manuelsampedro1/repo-a/tree/main/docs`.",
            result.issues,
        )
        self.assertIn(
            "Agent Safety Layer target should point to repo root `https://github.com/manuelsampedro1/mcp-guard`, not `https://github.com/manuelsampedro1/mcp-guard/issues`.",
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

    def test_repo_table_rows_must_have_linked_repo_entries(self) -> None:
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
                        "- Agent reliability.",
                        "- Verification discipline.",
                        "- Agent auditability.",
                        "- Agent safety.",
                        "- Product judgment.",
                        "",
                        "## Reviewer Path",
                        "\n".join(profile_quality_audit.REVIEWER_PATH_TARGETS),
                        "",
                        "## Selected Work",
                        "",
                        "| Repo | What it proves | Why it matters |",
                        "| --- | --- | --- |",
                        "| [repo-a](https://github.com/manuelsampedro1/repo-a) | proof | why |",
                        "| repo-without-link | proof | why |",
                        "",
                        "## Agent Safety Layer",
                        "",
                        "| Repo | What it proves | Why it matters |",
                        "| --- | --- | --- |",
                        "| [mcp-guard](https://github.com/manuelsampedro1/mcp-guard) | proof | why |",
                        "| safety-without-link | proof | why |",
                        "",
                        "## How I Work With Codex",
                        "",
                        "## Public Workbench",
                        "- [AI lab notes](./labs/README.md)",
                        "- [Recipes](./recipes/README.md)",
                        "- [Examples](./examples/README.md)",
                        "- [Tooling radar](./radar/README.md)",
                        "- [Automation runbook](./docs/automation-runbook.md)",
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
            "Selected Work has 2 table rows but 1 linked repo entries; every row needs one repo link.",
            result.issues,
        )
        self.assertIn(
            "Agent Safety Layer has 2 table rows but 1 linked repo entries; every row needs one repo link.",
            result.issues,
        )

    def test_agent_safety_layer_growth_requires_post_saturation_decision(self) -> None:
        safety_rows = "\n".join(
            f"| [safety-repo-{index}](https://github.com/manuelsampedro1/safety-repo-{index}) | proof | why |"
            for index in range(profile_quality_audit.AGENT_SAFETY_LAYER_BASELINE_ROWS + 1)
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
                        "- Agent reliability.",
                        "- Verification discipline.",
                        "- Agent auditability.",
                        "- Agent safety.",
                        "- Product judgment.",
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
                        safety_rows,
                        "",
                        "## How I Work With Codex",
                        "",
                        "## Public Workbench",
                        "- [AI lab notes](./labs/README.md)",
                        "- [Recipes](./recipes/README.md)",
                        "- [Examples](./examples/README.md)",
                        "- [Tooling radar](./radar/README.md)",
                        "- [Automation runbook](./docs/automation-runbook.md)",
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
            "Agent Safety Layer has grown to 7 rows; document an explicit post-saturation growth decision before adding rows above 6.",
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

    def test_selected_work_growth_requires_post_saturation_decision(self) -> None:
        rows = "\n".join(
            f"| [repo-{index}](https://github.com/manuelsampedro1/repo-{index}) | proof | why |"
            for index in range(profile_quality_audit.SELECTED_WORK_SATURATION_BASELINE_ROWS + 1)
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
                        "| Repo | What it proves | Why it matters |",
                        "| --- | --- | --- |",
                        "| [mcp-guard](https://github.com/manuelsampedro1/mcp-guard) | proof | why |",
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
            (root / "DECISIONS.md").write_text(
                "\n".join(
                    [
                        "## 2026-06-02 - Pause Proof Repo Volume After Saturation",
                        "",
                        "Inline mention: Allow Selected Work Growth After Saturation.",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            (root / "TODO.md").write_text(
                "Pause new proof-repo creation by default\n",
                encoding="utf-8",
            )
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
            "Selected Work has grown to 47 rows; document an explicit post-saturation growth decision before adding rows above 46.",
            result.issues,
        )

    def test_external_reviewer_navigation_must_keep_review_route(self) -> None:
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
            (examples / "README.md").write_text(
                "\n".join(f"- [{Path(path).name}](./{Path(path).name})" for path in profile_quality_audit.REQUIRED_EXAMPLES),
                encoding="utf-8",
            )
            for path in profile_quality_audit.REQUIRED_EXAMPLES:
                (root / path).write_text("# Example\n", encoding="utf-8")
            (root / "examples" / "external-reviewer-navigation.md").write_text(
                "\n".join(
                    [
                        "# External Reviewer Navigation",
                        "",
                        "This page should not become a generic profile essay.",
                        "",
                    ]
                ),
                encoding="utf-8",
            )

            result = profile_quality_audit.audit(root)

        self.assertIn(
            "External reviewer navigation is missing review route detail: Five-Minute Path.",
            result.issues,
        )
        self.assertIn(
            "External reviewer navigation is missing review route detail: repo-flightcheck.",
            result.issues,
        )
        self.assertIn(
            "External reviewer navigation is missing review route detail: Review Prompt.",
            result.issues,
        )


if __name__ == "__main__":
    unittest.main()
