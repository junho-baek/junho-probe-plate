"""Tests for the deterministic Wemake history evidence index."""

from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_wemake_index.py"
JSON_PATH = ROOT / "references" / "wemake-commit-index.json"
MARKDOWN_PATH = ROOT / "references" / "wemake-commit-index.md"
PINNED_HEAD = "21ceb5d55c608772ed374a651eaf1639eaec6d5c"
SOURCE_URL = "https://github.com/nomadcoders/wemake"


def load_module():
    spec = importlib.util.spec_from_file_location("build_wemake_index", SCRIPT)
    if spec is None or spec.loader is None:
        raise AssertionError("could not load index builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def record(number: str, commit_hash: str, **overrides: object) -> dict[str, object]:
    value: dict[str, object] = {
        "number": number,
        "hash": commit_hash,
        "author_date": "2026-01-02T03:04:05+00:00",
        "subject": "Record audited behavior",
        "changed_paths": ["app/example.ts"],
        "technical_topics": ["route adapter"],
        "architecture_stage": "route responsibility",
        "rule_ids": ["ARCH-001"],
        "classification": "foundation",
        "audit_note": "Establishes the boundary used by later route work.",
    }
    value.update(overrides)
    return value


class WemakeIndexBuilderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.builder = load_module()

    def test_merge_preserves_existing_human_annotations(self) -> None:
        draft = record("001", "a" * 40, subject="Fresh Git subject", technical_topics=[], architecture_stage="", rule_ids=[], classification="UNREVIEWED", audit_note="")
        existing = record("099", "a" * 40, technical_topics=["validated action"], architecture_stage="mutation boundary", rule_ids=["RR7-002"], classification="pattern-refinement", audit_note="Moves the mutation protocol into the route adapter.")

        merged = self.builder.merge_records([draft], [existing])

        self.assertEqual("001", merged[0]["number"])
        self.assertEqual("Fresh Git subject", merged[0]["subject"])
        self.assertEqual(["validated action"], merged[0]["technical_topics"])
        self.assertEqual("pattern-refinement", merged[0]["classification"])

    def test_merge_marks_a_new_hash_unreviewed(self) -> None:
        draft = record("001", "b" * 40, technical_topics=["wrong"], architecture_stage="wrong", rule_ids=["ARCH-001"], classification="foundation", audit_note="wrong")

        merged = self.builder.merge_records([draft], [])

        self.assertEqual([], merged[0]["technical_topics"])
        self.assertEqual("", merged[0]["architecture_stage"])
        self.assertEqual([], merged[0]["rule_ids"])
        self.assertEqual("UNREVIEWED", merged[0]["classification"])
        self.assertEqual("", merged[0]["audit_note"])

    def test_annotated_hash_missing_from_requested_revision_is_refused(self) -> None:
        existing = record("001", "c" * 40)
        with self.assertRaisesRegex(ValueError, "annotated hash"):
            self.builder.merge_records([], [existing])

    def test_malformed_and_duplicate_existing_records_are_rejected(self) -> None:
        duplicate = [record("001", "d" * 40), record("002", "d" * 40)]
        with self.assertRaisesRegex(ValueError, "duplicate"):
            self.builder.validate_existing_records(duplicate)
        with self.assertRaisesRegex(ValueError, "missing"):
            self.builder.validate_existing_records([{"hash": "e" * 40}])

    def test_payload_validation_rejects_malformed_types_and_hashes(self) -> None:
        with self.assertRaisesRegex(ValueError, "records"):
            self.builder.validate_payload({"source_url": SOURCE_URL, "pinned_head": PINNED_HEAD, "verified_at": "2026-08-04", "record_count": 0, "records": "not a list"}, {"ARCH-001"}, False)
        malformed = record("001", "A" * 40, author_date="not-a-date", changed_paths=["", "app/example.ts"], technical_topics=[""], rule_ids=[""], classification="bad")
        with self.assertRaisesRegex(ValueError, "hash"):
            self.builder.validate_existing_records([malformed])

    def test_record_count_rejects_bool(self) -> None:
        payload = self.builder.make_payload([record("001", "a" * 40)], SOURCE_URL, "a" * 40, "2026-08-04")
        payload["record_count"] = True
        with self.assertRaisesRegex(ValueError, "record count"):
            self.builder.validate_payload(payload, {"ARCH-001"}, require_audited=True)

    def test_validation_rejects_audited_markers_and_head_mismatch_alongside_pristine_records(self) -> None:
        audited = record("001", "a" * 40, audit_note="TODO: audit this route.")
        pristine = record("002", "b" * 40, technical_topics=[], architecture_stage="", rule_ids=[], classification="UNREVIEWED", audit_note="")
        payload = self.builder.make_payload([audited, pristine], SOURCE_URL, "b" * 40, "2026-08-04")
        with self.assertRaisesRegex(ValueError, "unaudited marker"):
            self.builder.validate_payload(payload, {"ARCH-001"}, require_audited=False)
        audited["audit_note"] = "Audited route boundary."
        payload["pinned_head"] = "c" * 40
        with self.assertRaisesRegex(ValueError, "pinned head"):
            self.builder.validate_payload(payload, {"ARCH-001"}, require_audited=False)

    def test_whitespace_only_human_annotations_are_rejected(self) -> None:
        whitespace = record("001", "d" * 40, technical_topics=[" "], architecture_stage=" ", rule_ids=["ARCH-001"], classification="foundation", audit_note=" ")
        payload = self.builder.make_payload([whitespace], SOURCE_URL, "d" * 40, "2026-08-04")
        with self.assertRaisesRegex(ValueError, "technical_topics"):
            self.builder.validate_payload(payload, {"ARCH-001"}, require_audited=False)

    def test_duplicate_or_padded_human_annotations_are_rejected(self) -> None:
        duplicate_topics = record("001", "d" * 40, technical_topics=["route", "route"])
        with self.assertRaisesRegex(ValueError, "technical_topics"):
            self.builder.validate_existing_records([duplicate_topics])
        duplicate_rules = record("001", "e" * 40, rule_ids=["ARCH-001", "ARCH-001"])
        with self.assertRaisesRegex(ValueError, "rule_ids"):
            self.builder.validate_existing_records([duplicate_rules])
        for field, value in (("technical_topics", [" route"]), ("rule_ids", ["ARCH-001 "]), ("architecture_stage", " route"), ("classification", "foundation "), ("audit_note", "note. ")):
            padded = record("001", "f" * 40, **{field: value})
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, field):
                self.builder.validate_existing_records([padded])

    def test_git_derived_todo_words_do_not_count_as_unaudited_markers(self) -> None:
        source_markers = record("001", "a" * 40, subject="TODO: preserve source history", changed_paths=["app/FIXME route.ts"])
        payload = self.builder.make_payload([source_markers], SOURCE_URL, "a" * 40, "2026-08-04")
        self.builder.validate_payload(payload, {"ARCH-001"}, require_audited=True)

    def test_annotation_marker_tokens_are_rejected(self) -> None:
        for field, value in (("technical_topics", ["TODO"]), ("architecture_stage", "FIXME later"), ("audit_note", "Contains a PLACEHOLDER marker.")):
            marked = record("001", "a" * 40, **{field: value})
            payload = self.builder.make_payload([marked], SOURCE_URL, "a" * 40, "2026-08-04")
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, "unaudited marker"):
                self.builder.validate_payload(payload, {"ARCH-001"}, require_audited=True)

    def test_whitespace_only_subject_and_changed_path_are_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "subject"):
            self.builder.validate_existing_records([record("001", "e" * 40, subject="   ")])
        with self.assertRaisesRegex(ValueError, "changed paths"):
            self.builder.validate_existing_records([record("001", "f" * 40, changed_paths=["  "])])

    def test_markdown_escapes_table_text_and_emits_matching_rows(self) -> None:
        records = [record(f"{number:03d}", f"{number:040x}") for number in range(1, 136)]
        records[0]["subject"] = "Title | with pipe"
        payload = self.builder.make_payload(records, SOURCE_URL, PINNED_HEAD, "2026-08-04")
        markdown = self.builder.render_markdown(payload)

        self.assertIn("Title \\| with pipe", markdown)
        self.assertEqual(135, sum(bool(re.match(r"^\| \d{3} \| [0-9a-f]{40} \|", line)) for line in markdown.splitlines()))

    def test_equivalent_output_paths_are_rejected_without_corruption(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "index"
            target.write_bytes(b"original")
            hardlink = root / "hardlink"
            os.link(target, hardlink)
            symlink = root / "symlink"
            symlink.symlink_to(target)
            for other in (target, hardlink, symlink):
                with self.subTest(other=other), self.assertRaisesRegex(ValueError, "distinct"):
                    self.builder.validate_output_paths(target, other)
                self.assertEqual(b"original", target.read_bytes())

    def test_cli_rejects_same_output_path_before_git_work(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "index"
            output.write_bytes(b"original")
            completed = subprocess.run(
                ["python3", str(SCRIPT), "--repo", "/not/a/repository", "--revision", PINNED_HEAD, "--json", str(output), "--markdown", str(output)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(2, completed.returncode)
            self.assertIn("distinct", completed.stderr)
            self.assertNotIn("Traceback", completed.stderr)
            self.assertEqual(b"original", output.read_bytes())

    def test_pair_write_failure_restores_preexisting_outputs_and_cleans_temps(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            json_path = root / "index.json"
            markdown_path = root / "index.md"
            json_path.write_bytes(b"old-json\x00")
            markdown_path.write_bytes(b"old-markdown\n")
            replacements = 0

            def fail_markdown(source: str, destination: str) -> None:
                nonlocal replacements
                replacements += 1
                if replacements == 2:
                    raise OSError("simulated Markdown commit failure")
                os.replace(source, destination)

            with self.assertRaisesRegex(OSError, "publish output pair"):
                self.builder.write_output_pair(json_path, "new json", markdown_path, "new markdown", replace=fail_markdown)
            self.assertEqual(b"old-json\x00", json_path.read_bytes())
            self.assertEqual(b"old-markdown\n", markdown_path.read_bytes())
            self.assertEqual({"index.json", "index.md"}, {path.name for path in root.iterdir()})

    def test_pair_write_failure_does_not_leave_one_sided_new_output(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            json_path = root / "index.json"
            markdown_path = root / "index.md"
            replacements = 0

            def fail_markdown(source: str, destination: str) -> None:
                nonlocal replacements
                replacements += 1
                if replacements == 2:
                    raise OSError("simulated Markdown commit failure")
                os.replace(source, destination)

            with self.assertRaisesRegex(OSError, "publish output pair"):
                self.builder.write_output_pair(json_path, "new json", markdown_path, "new markdown", replace=fail_markdown)
            self.assertFalse(json_path.exists())
            self.assertFalse(markdown_path.exists())
            self.assertEqual([], list(root.iterdir()))

    def test_successful_pair_write_preserves_existing_modes_and_sets_new_modes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            json_path = root / "index.json"
            markdown_path = root / "index.md"
            json_path.write_text("old json", encoding="utf-8")
            markdown_path.write_text("old markdown", encoding="utf-8")
            json_path.chmod(0o640)
            markdown_path.chmod(0o644)

            self.builder.write_output_pair(json_path, "new json", markdown_path, "new markdown")

            self.assertEqual("new json", json_path.read_text(encoding="utf-8"))
            self.assertEqual("new markdown", markdown_path.read_text(encoding="utf-8"))
            self.assertEqual(0o640, stat.S_IMODE(json_path.stat().st_mode))
            self.assertEqual(0o644, stat.S_IMODE(markdown_path.stat().st_mode))

            new_json = root / "new.json"
            new_markdown = root / "new.md"
            self.builder.write_output_pair(new_json, "json", new_markdown, "markdown")
            self.assertEqual(0o644, stat.S_IMODE(new_json.stat().st_mode))
            self.assertEqual(0o644, stat.S_IMODE(new_markdown.stat().st_mode))
            self.assertEqual({"index.json", "index.md", "new.json", "new.md"}, {path.name for path in root.iterdir()})

    def test_first_replace_failure_leaves_both_existing_files_untouched(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            json_path = root / "index.json"
            markdown_path = root / "index.md"
            json_path.write_bytes(b"old json")
            markdown_path.write_bytes(b"old markdown")
            json_path.chmod(0o640)
            markdown_path.chmod(0o604)
            before = {
                json_path: (json_path.stat().st_ino, stat.S_IMODE(json_path.stat().st_mode), json_path.read_bytes()),
                markdown_path: (markdown_path.stat().st_ino, stat.S_IMODE(markdown_path.stat().st_mode), markdown_path.read_bytes()),
            }

            def fail_first(source: str, destination: str) -> None:
                raise OSError("simulated first replace failure")

            with self.assertRaisesRegex(OSError, "publish output pair"):
                self.builder.write_output_pair(json_path, "new json", markdown_path, "new markdown", replace=fail_first)

            for path, expected in before.items():
                self.assertEqual(expected, (path.stat().st_ino, stat.S_IMODE(path.stat().st_mode), path.read_bytes()))
            self.assertEqual({"index.json", "index.md"}, {path.name for path in root.iterdir()})

    def test_second_replace_failure_restores_only_first_file_with_original_mode(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            json_path = root / "index.json"
            markdown_path = root / "index.md"
            json_path.write_bytes(b"old json")
            markdown_path.write_bytes(b"old markdown")
            json_path.chmod(0o640)
            markdown_path.chmod(0o604)
            original_json_inode = json_path.stat().st_ino
            original_markdown_inode = markdown_path.stat().st_ino
            replacements = 0

            def fail_second(source: str, destination: str) -> None:
                nonlocal replacements
                replacements += 1
                if replacements == 2:
                    raise OSError("simulated second replace failure")
                os.replace(source, destination)

            with self.assertRaisesRegex(OSError, "publish output pair"):
                self.builder.write_output_pair(json_path, "new json", markdown_path, "new markdown", replace=fail_second)

            self.assertEqual(b"old json", json_path.read_bytes())
            self.assertEqual(0o640, stat.S_IMODE(json_path.stat().st_mode))
            self.assertNotEqual(original_json_inode, json_path.stat().st_ino)
            self.assertEqual(b"old markdown", markdown_path.read_bytes())
            self.assertEqual(0o604, stat.S_IMODE(markdown_path.stat().st_mode))
            self.assertEqual(original_markdown_inode, markdown_path.stat().st_ino)
            self.assertEqual({"index.json", "index.md"}, {path.name for path in root.iterdir()})

    def test_prepare_helpers_clean_their_temp_after_fsync_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            def fail_fsync(file_descriptor: int) -> None:
                raise OSError("simulated fsync failure")

            with self.assertRaisesRegex(OSError, "fsync"):
                self.builder._prepare_text(root / "new.json", "new", ".prepared-", fsync=fail_fsync)
            self.assertEqual([], list(root.iterdir()))

            existing = root / "existing.json"
            existing.write_bytes(b"original")
            existing.chmod(0o640)
            before = (existing.stat().st_ino, stat.S_IMODE(existing.stat().st_mode), existing.read_bytes())
            with self.assertRaisesRegex(OSError, "fsync"):
                self.builder._prepare_backup(existing, ".backup-", fsync=fail_fsync)
            self.assertEqual(before, (existing.stat().st_ino, stat.S_IMODE(existing.stat().st_mode), existing.read_bytes()))
            self.assertEqual({"existing.json"}, {path.name for path in root.iterdir()})

    def test_prospective_equivalence_after_json_replace_rolls_back_prior_state(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            json_path = root / "index.json"
            markdown_path = root / "index.md"
            json_path.write_bytes(b"old json")
            markdown_path.write_bytes(b"old markdown")
            json_path.chmod(0o640)
            markdown_path.chmod(0o604)
            original_markdown_inode = markdown_path.stat().st_ino

            with self.assertRaisesRegex(OSError, "equivalent"):
                self.builder.write_output_pair(
                    json_path,
                    "new json",
                    markdown_path,
                    "new markdown",
                    equivalent_after_json=lambda json_destination, markdown_destination: True,
                )

            self.assertEqual(b"old json", json_path.read_bytes())
            self.assertEqual(0o640, stat.S_IMODE(json_path.stat().st_mode))
            self.assertEqual(b"old markdown", markdown_path.read_bytes())
            self.assertEqual(0o604, stat.S_IMODE(markdown_path.stat().st_mode))
            self.assertEqual(original_markdown_inode, markdown_path.stat().st_ino)
            self.assertEqual({"index.json", "index.md"}, {path.name for path in root.iterdir()})

    def test_real_filesystem_equivalent_absent_names_do_not_leave_one_sided_output(self) -> None:
        variants = (("case-probe", "CASE-PROBE", "case-index", "CASE-INDEX"), ("caf\u00e9-probe", "cafe\u0301-probe", "caf\u00e9-index", "cafe\u0301-index"))
        observed = 0
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for probe_name, probe_alias_name, output_name, output_alias_name in variants:
                variant_root = root / str(observed)
                variant_root.mkdir()
                probe = variant_root / probe_name
                probe_alias = variant_root / probe_alias_name
                probe.write_bytes(b"probe")
                equivalent = probe_alias.exists() and os.path.samefile(probe, probe_alias)
                probe.unlink()
                if not equivalent:
                    variant_root.rmdir()
                    continue
                observed += 1
                json_path = variant_root / output_name
                markdown_path = variant_root / output_alias_name
                with self.assertRaisesRegex(OSError, "equivalent"):
                    self.builder.write_output_pair(json_path, "json", markdown_path, "markdown")
                self.assertFalse(json_path.exists())
                self.assertFalse(markdown_path.exists())
                self.assertEqual([], list(variant_root.iterdir()))
                variant_root.rmdir()
        if not observed:
            self.skipTest("filesystem does not equate tested case or Unicode variants")

    @unittest.skipUnless(os.environ.get("WEMAKE_REPO"), "set WEMAKE_REPO for filesystem-alias CLI integration")
    def test_cli_rejects_prospective_case_alias_without_one_sided_output(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            probe = root / "probe"
            probe_alias = root / "PROBE"
            probe.write_bytes(b"probe")
            equivalent = probe_alias.exists() and os.path.samefile(probe, probe_alias)
            probe.unlink()
            if not equivalent:
                self.skipTest("filesystem is case-sensitive")
            json_path = root / "index"
            markdown_path = root / "INDEX"
            completed = subprocess.run(
                ["python3", str(SCRIPT), "--repo", os.environ["WEMAKE_REPO"], "--revision", PINNED_HEAD, "--json", str(json_path), "--markdown", str(markdown_path)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(2, completed.returncode)
            self.assertIn("equivalent", completed.stderr)
            self.assertNotIn("Traceback", completed.stderr)
            self.assertFalse(json_path.exists())
            self.assertFalse(markdown_path.exists())
            self.assertEqual([], list(root.iterdir()))

    def test_expected_cli_error_is_concise(self) -> None:
        completed = subprocess.run(
            ["python3", str(SCRIPT), "--repo", "/not/a/repository", "--revision", PINNED_HEAD, "--json", "/tmp/no.json", "--markdown", "/tmp/no.md"],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertNotEqual(0, completed.returncode)
        self.assertLess(len(completed.stderr.splitlines()), 3)
        self.assertNotIn("Traceback", completed.stderr)

    def test_existing_payload_rejects_bad_metadata_and_mixed_annotations(self) -> None:
        payload = self.builder.make_payload([record("001", "f" * 40)], SOURCE_URL, PINNED_HEAD, "2026-08-04")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "index.json"
            payload["source_url"] = "https://example.invalid/not-wemake"
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "source"):
                self.builder.read_existing(path)
            payload["source_url"] = SOURCE_URL
            payload["pinned_head"] = "f" * 40
            payload["records"][0].update({"technical_topics": [], "architecture_stage": "", "rule_ids": ["NOPE-001"], "classification": "pattern-introduction", "audit_note": ""})
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "annotations"):
                self.builder.read_existing(path)

    def test_source_url_override_cannot_bypass_unrelated_origin(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory) / "repo"
            subprocess.run(["git", "init", str(repo)], check=True, capture_output=True, text=True)
            subprocess.run(["git", "-C", str(repo), "remote", "add", "origin", "https://github.com/example/not-wemake.git"], check=True, capture_output=True, text=True)
            completed = subprocess.run(["python3", str(SCRIPT), "--repo", str(repo), "--revision", "HEAD", "--json", str(repo / "a.json"), "--markdown", str(repo / "a.md"), "--source-url", SOURCE_URL], text=True, capture_output=True, check=False)
            self.assertEqual(2, completed.returncode)
            self.assertIn("origin", completed.stderr)


class WemakeCommittedIndexTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.builder = load_module()
        with JSON_PATH.open(encoding="utf-8") as file:
            cls.payload = json.load(file)

    def test_committed_index_is_complete_and_audited(self) -> None:
        payload = self.payload
        self.assertEqual(SOURCE_URL, payload["source_url"])
        self.assertEqual(PINNED_HEAD, payload["pinned_head"])
        self.assertEqual("2026-08-04", payload["verified_at"])
        self.assertEqual(135, payload["record_count"])
        self.assertEqual(135, len(payload["records"]))
        self.builder.validate_payload(payload, self.builder.load_rule_ids(ROOT / "references" / "rule-catalog.json"), require_audited=True)
        records = payload["records"]
        self.assertEqual([f"{number:03d}" for number in range(1, 136)], [record["number"] for record in records])
        self.assertEqual(PINNED_HEAD, records[-1]["hash"])
        self.assertEqual(135, len({record["hash"] for record in records}))
        self.assertEqual(set(self.builder.CLASSIFICATIONS), {record["classification"] for record in records})
        for record in records:
            self.assertTrue(record["audit_note"].endswith("."))
            self.assertNotEqual(record["subject"].strip().lower(), record["audit_note"].strip(".").lower())
            self.assertNotIn("placeholder", record["audit_note"].lower())
            if record["classification"] in {"teaching-transition", "legacy-risk"}:
                self.assertRegex(record["audit_note"].lower(), "temporary|later|legacy|incomplete|risk|not a current")

    def test_markdown_is_rendered_from_the_committed_json(self) -> None:
        rendered = self.builder.render_markdown(self.payload)
        self.assertEqual(rendered, MARKDOWN_PATH.read_text(encoding="utf-8"))
        self.assertEqual(135, sum(bool(re.match(r"^\| \d{3} \| [0-9a-f]{40} \|", line)) for line in rendered.splitlines()))
        self.assertNotIn("```", rendered)

    def test_known_lesson_and_legacy_records_remain_explicitly_non_recommendations(self) -> None:
        records = {record["number"]: record for record in self.payload["records"]}
        for number in ("017", "018", "021", "027", "032", "045", "066", "068", "070", "071", "072", "073", "074", "077", "078", "079", "080", "082", "084", "085", "086", "089", "110", "111", "112"):
            self.assertEqual("teaching-transition", records[number]["classification"])
        for number in ("063", "067", "069", "075", "076", "081", "083", "087", "091", "093", "095", "101", "103", "104", "109", "113", "116", "117", "119", "120", "122", "126", "127", "128", "129", "133"):
            self.assertEqual("legacy-risk", records[number]["classification"])
        for number in ("088", "090", "135"):
            self.assertEqual("correction", records[number]["classification"])
        self.assertIn("DB-005", records["116"]["rule_ids"])
        self.assertEqual({"DB-001", "DB-003"}, set(records["121"]["rule_ids"]))
        self.assertIn("SEC-001", records["127"]["rule_ids"])
        self.assertIn("ZOD-001", records["128"]["rule_ids"])
        self.assertEqual({"SUPA-005", "UI-005", "TS-002", "RR7-006"}, set(records["120"]["rule_ids"]))
        self.assertEqual({"RR7-002", "SEC-001", "SEC-003"}, set(records["122"]["rule_ids"]))
        self.assertNotIn("RR7-001", records["003"]["rule_ids"])
        self.assertNotIn("RR7-001", records["005"]["rule_ids"])
        self.assertEqual(
            {"007", "010", "017", "018", "021", "027", "028", "030", "031", "032", "037", "045", "065", "066", "068", "070", "071", "072", "073", "074", "077", "078", "079", "080", "082", "084", "085", "086", "089", "099", "110", "111", "112", "124", "125"},
            {number for number, record in records.items() if record["classification"] == "teaching-transition"},
        )
        self.assertEqual(
            {"063", "067", "069", "075", "076", "081", "083", "087", "091", "093", "095", "101", "103", "104", "107", "109", "113", "116", "117", "119", "120", "122", "123", "126", "127", "128", "129", "130", "133", "134"},
            {number for number, record in records.items() if record["classification"] == "legacy-risk"},
        )

    @unittest.skipUnless(os.environ.get("WEMAKE_REPO"), "set WEMAKE_REPO for Git provenance integration")
    def test_committed_index_matches_pinned_git_history(self) -> None:
        repo = Path(os.environ["WEMAKE_REPO"])
        commits = self.builder.collect_git_records(repo, PINNED_HEAD)
        records = self.payload["records"]
        self.assertEqual(135, len(commits))
        self.assertEqual([item["hash"] for item in commits], [item["hash"] for item in records])
        for actual, indexed in zip(commits, records):
            self.assertEqual(actual["author_date"], indexed["author_date"])
            self.assertEqual(actual["subject"], indexed["subject"])
            self.assertEqual(actual["changed_paths"], indexed["changed_paths"])

    @unittest.skipUnless(os.environ.get("WEMAKE_REPO"), "set WEMAKE_REPO for Git provenance integration")
    def test_merge_paths_are_derived_from_the_merge_result(self) -> None:
        repo = Path(os.environ["WEMAKE_REPO"])
        indexed = {record["hash"]: record for record in self.builder.collect_git_records(repo, PINNED_HEAD)}
        for commit_hash in ("4cbba8b6d4b19fb808a9b2f10cc75a0b5d127dcb", "088286184a579c8c8c6df9f0d31cada1e08d6d7b"):
            result_paths = subprocess.run(
                ["git", "-C", str(repo), "diff-tree", "--root", "-m", "--no-commit-id", "--name-only", "-r", commit_hash],
                text=True,
                capture_output=True,
                check=True,
            ).stdout.splitlines()
            self.assertEqual(sorted(set(result_paths)), indexed[commit_hash]["changed_paths"])

    @unittest.skipUnless(os.environ.get("WEMAKE_REPO"), "set WEMAKE_REPO for generator preservation integration")
    def test_generator_preserves_existing_human_annotations(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            json_path = Path(directory) / "index.json"
            markdown_path = Path(directory) / "index.md"
            shutil.copy2(JSON_PATH, json_path)
            before = {record["hash"]: tuple(record[field] if not isinstance(record[field], list) else tuple(record[field]) for field in ("technical_topics", "architecture_stage", "rule_ids", "classification", "audit_note")) for record in self.payload["records"]}
            completed = subprocess.run(
                ["python3", str(SCRIPT), "--repo", os.environ["WEMAKE_REPO"], "--revision", PINNED_HEAD, "--json", str(json_path), "--markdown", str(markdown_path)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(0, completed.returncode, completed.stderr)
            after_payload = json.loads(json_path.read_text(encoding="utf-8"))
            after = {record["hash"]: tuple(record[field] if not isinstance(record[field], list) else tuple(record[field]) for field in ("technical_topics", "architecture_stage", "rule_ids", "classification", "audit_note")) for record in after_payload["records"]}
            self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
