import json
import tempfile
import unittest
from pathlib import Path


FIXTURES = Path(__file__).resolve().parent / "fixtures"
SENTINEL = "// Synthetic fixture; not derived from Supaplate source."
SOURCE_SUFFIXES = {".ts", ".tsx", ".sql", ".mjs"}
ALLOWED_SUFFIXES = {".md", ".json", ".ts", ".tsx", ".sql", ".mjs"}
FORBIDDEN_DIRECTORIES = {".git", "node_modules", "vendor", "build", "dist", "generated"}
IMAGE_ARCHIVE_SUFFIXES = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".bmp", ".tif", ".tiff", ".ico", ".avif",
    ".heic", ".heif", ".zip", ".tar", ".gz", ".rar", ".7z", ".tgz", ".bz2", ".xz", ".zst",
}


def assert_safe_fixture_path(path, fixture_root):
    relative = path.relative_to(fixture_root)
    if path.is_symlink():
        raise AssertionError(f"fixture symlink is forbidden: {relative}")


def fixture_roots():
    roots = []
    for path in sorted(FIXTURES.iterdir()):
        assert_safe_fixture_path(path, FIXTURES)
        if path.is_dir():
            roots.append(path)
    return roots


class FixtureProvenanceTests(unittest.TestCase):
    def test_fixture_policy_rejects_symlinks_before_processing(self):
        validator = globals().get("assert_safe_fixture_path")
        self.assertIsNotNone(validator, "fixture policy must expose its path safety guard")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "target.md"
            target.write_text("# Synthetic fixture\n", encoding="utf-8")
            link = root / "linked.md"
            link.symlink_to(target)
            with self.assertRaisesRegex(AssertionError, "symlink"):
                validator(link, root)

    def test_fixture_file_policy_declares_exact_allowlist(self):
        self.assertEqual(
            globals().get("ALLOWED_SUFFIXES"),
            {".md", ".json", ".ts", ".tsx", ".sql", ".mjs"},
        )

    def test_readmes_begin_with_synthetic_fixture_heading(self):
        for root in fixture_roots():
            readme = root / "README.md"
            self.assertTrue(readme.is_file(), f"missing fixture README: {root}")
            self.assertTrue(
                readme.read_text(encoding="utf-8").startswith("# Synthetic fixture"),
                f"invalid synthetic fixture heading: {readme}",
            )

    def test_forbidden_suffix_policy_covers_all_image_and_archive_formats(self):
        required_suffixes = {
            ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".bmp", ".tif", ".tiff",
            ".ico", ".avif", ".heic", ".heif", ".zip", ".tar", ".gz", ".rar", ".7z", ".tgz",
            ".bz2", ".xz", ".zst",
        }
        self.assertEqual(required_suffixes, IMAGE_ARCHIVE_SUFFIXES)
        self.assertTrue(required_suffixes.isdisjoint(ALLOWED_SUFFIXES))

    def test_fixture_roots_declare_synthetic_origin(self):
        roots = fixture_roots()
        self.assertTrue(roots)
        for root in roots:
            manifest = root / "fixture.json"
            self.assertTrue(manifest.is_file(), f"missing fixture manifest: {root}")
            self.assertEqual(
                json.loads(manifest.read_text(encoding="utf-8")),
                {"origin": "synthetic", "derived_from_supaplate": False},
            )

    def test_fixture_json_files_are_valid_objects(self):
        for path in FIXTURES.rglob("*.json"):
            assert_safe_fixture_path(path, FIXTURES)
            self.assertIsInstance(json.loads(path.read_text(encoding="utf-8")), dict)

    def test_fixture_tree_contains_only_safe_synthetic_files(self):
        for path in FIXTURES.rglob("*"):
            assert_safe_fixture_path(path, FIXTURES)
            relative = path.relative_to(FIXTURES)
            self.assertFalse(
                path.is_dir() and path.name in FORBIDDEN_DIRECTORIES,
                f"forbidden fixture directory: {relative}",
            )
            if not path.is_file():
                continue
            if path.name != ".gitkeep":
                self.assertIn(
                    path.suffix.lower(),
                    ALLOWED_SUFFIXES,
                    f"fixture file type is not allowlisted: {relative}",
                )
            self.assertLessEqual(path.stat().st_size, 12 * 1024, f"oversized fixture file: {relative}")
            if path.suffix.lower() in SOURCE_SUFFIXES:
                first_line = path.read_text(encoding="utf-8").splitlines()[0]
                self.assertEqual(first_line, SENTINEL, f"missing synthetic sentinel: {relative}")


if __name__ == "__main__":
    unittest.main()
