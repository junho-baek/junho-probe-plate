"""Contracts for safely exposing Junho Plate to other Agent Skills hosts."""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "scripts" / "install_agent_skill_links.py"
SKILL_NAMES = (
    "junho-plate",
    "junho-plate-review",
    "junho-plate-refactor",
    "junho-plate-feature",
)


class AgentSkillInstallTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        temporary_root = Path(self.temporary_directory.name)
        self.source_root = temporary_root / "source"
        self.destination_root = temporary_root / "destination"
        for skill_name in SKILL_NAMES:
            skill_directory = self.source_root / skill_name
            skill_directory.mkdir(parents=True)
            (skill_directory / "SKILL.md").write_text(
                f"---\nname: {skill_name}\ndescription: test\n---\n",
                encoding="utf-8",
            )

    def run_installer(self, *extra_arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(INSTALLER),
                "--source-root",
                str(self.source_root),
                "--destination-root",
                str(self.destination_root),
                *extra_arguments,
            ],
            capture_output=True,
            text=True,
        )

    def test_install_creates_exact_links_and_is_idempotent(self) -> None:
        first = self.run_installer()
        second = self.run_installer()

        self.assertEqual(0, first.returncode, first.stderr)
        self.assertEqual(0, second.returncode, second.stderr)
        for skill_name in SKILL_NAMES:
            destination = self.destination_root / skill_name
            self.assertTrue(destination.is_symlink())
            self.assertEqual(
                (self.source_root / skill_name).resolve(),
                destination.resolve(strict=True),
            )

    def test_conflict_fails_before_creating_any_link(self) -> None:
        conflict = self.destination_root / "junho-plate-refactor"
        conflict.mkdir(parents=True)

        completed = self.run_installer()

        self.assertEqual(1, completed.returncode)
        self.assertIn("is not a symlink", completed.stderr)
        for skill_name in SKILL_NAMES:
            destination = self.destination_root / skill_name
            if destination != conflict:
                self.assertFalse(os.path.lexists(destination))

    def test_check_is_read_only_and_reports_missing_links(self) -> None:
        completed = self.run_installer("--check")

        self.assertEqual(1, completed.returncode)
        self.assertIn("destination link is missing", completed.stderr)
        self.assertFalse(self.destination_root.exists())

    def test_check_accepts_all_exact_links(self) -> None:
        installed = self.run_installer()
        checked = self.run_installer("--check")

        self.assertEqual(0, installed.returncode, installed.stderr)
        self.assertEqual(0, checked.returncode, checked.stderr)
        self.assertIn("verified 4", checked.stdout)


if __name__ == "__main__":
    unittest.main()
