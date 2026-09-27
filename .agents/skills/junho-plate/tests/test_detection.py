import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "detect_plate.py"
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def load_detector():
    spec = importlib.util.spec_from_file_location("junho_plate_detect_plate", SCRIPT)
    if spec is None or spec.loader is None or not SCRIPT.is_file():
        raise AssertionError("detect_plate.py must provide inspect_project")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def write_complete_project(
    root,
    *,
    package_name="generic-project",
    description="A generic application.",
    readme="# Generic project\n",
    router_name="react-router",
    router_version="7.5.1",
):
    package = {
        "name": package_name,
        "description": description,
        "dependencies": {
            router_name: router_version,
            "@supabase/supabase-js": "2.45.0",
            "drizzle-orm": "0.40.0",
        },
    }
    (root / "package.json").write_text(json.dumps(package), encoding="utf-8")
    (root / "README.md").write_text(readme, encoding="utf-8")
    (root / "app" / "features").mkdir(parents=True)
    (root / "app" / "routes.ts").write_text("export const routes = [];\n", encoding="utf-8")
    supabase = root / "app" / "core" / "supabase"
    supabase.mkdir(parents=True)
    (supabase / "server.ts").write_text("export const server = true;\n", encoding="utf-8")


def update_package(root, **fields):
    package_path = root / "package.json"
    package = json.loads(package_path.read_text(encoding="utf-8"))
    package.update(fields)
    package_path.write_text(json.dumps(package), encoding="utf-8")


class InspectProjectTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.detect_plate = load_detector()

    def inspect(self, fixture_name, **kwargs):
        return self.detect_plate.inspect_project(FIXTURES / fixture_name, **kwargs)

    def test_confirmed_fixture_is_confirmed(self):
        self.assertEqual(self.inspect("confirmed-plate")["status"], "CONFIRMED")

    def test_generic_rr7_fixture_is_compatible(self):
        self.assertEqual(self.inspect("compatible-stack")["status"], "COMPATIBLE")

    def test_unsupported_fixture_is_unsupported(self):
        result = self.inspect("unsupported-project")
        self.assertEqual(result["status"], "UNSUPPORTED")
        self.assertTrue(result["missing"])

    def test_user_confirmation_records_native_lineage_for_compatible_fixture(self):
        result = self.inspect("compatible-stack", user_confirmed=True)
        self.assertEqual(result["status"], "CONFIRMED")
        self.assertIn("user-confirmed-provenance", result["evidence"])

    def test_user_confirmation_does_not_override_missing_rr7(self):
        result = self.inspect("unsupported-project", user_confirmed=True)
        self.assertEqual(result["status"], "UNSUPPORTED")
        self.assertTrue(result["missing"])
        self.assertIn("user-confirmed-provenance", result["evidence"])

    def test_results_have_json_safe_contract(self):
        result = self.inspect("confirmed-plate")
        self.assertEqual(set(result), {"status", "evidence", "missing", "versions"})
        self.assertIsInstance(result["evidence"], list)
        self.assertTrue(result["evidence"])
        json.dumps(result)

    def test_dependency_versions_come_from_package_json(self):
        versions = self.inspect("confirmed-plate")["versions"]
        self.assertEqual(versions["react-router"], "7.1.0")
        self.assertEqual(versions["@supabase/supabase-js"], "2.45.0")
        self.assertEqual(versions["drizzle-orm"], "0.40.0")

    def test_dev_dependencies_supply_stack_signals_and_versions(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_complete_project(root)
            update_package(
                root,
                dependencies={},
                devDependencies={
                    "@react-router/dev": "^7.5.1",
                    "@supabase/ssr": "0.6.0",
                    "drizzle-orm": "0.40.0",
                },
            )
            result = self.detect_plate.inspect_project(root)
        self.assertEqual(result["status"], "COMPATIBLE")
        self.assertEqual(
            result["versions"],
            {
                "@react-router/dev": "^7.5.1",
                "@supabase/ssr": "0.6.0",
                "drizzle-orm": "0.40.0",
            },
        )

    def test_stack_alone_is_compatible_without_creating_provenance(self):
        result = self.inspect("compatible-stack")
        self.assertEqual(result["status"], "COMPATIBLE")
        self.assertNotIn("supaplate-provenance", result["evidence"])
        self.assertIn("generic-or-unverified-origin", result["evidence"])
        self.assertNotIn("missing-supaplate-provenance", result["missing"])

    def test_rr7_alone_is_eligible_and_optional_capabilities_remain_gaps(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "package.json").write_text(
                json.dumps({"dependencies": {"react-router": "7.5.1"}}),
                encoding="utf-8",
            )
            result = self.detect_plate.inspect_project(root)

        self.assertEqual(result["status"], "COMPATIBLE")
        for gap in (
            "missing-supabase",
            "missing-drizzle",
            "missing-app-routes",
            "missing-app-features-directory",
            "missing-server-side-supabase-marker",
        ):
            self.assertIn(gap, result["missing"])

    def test_negated_supaplate_description_is_not_positive_provenance(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_complete_project(root, description="This is not a Supaplate project.")
            result = self.detect_plate.inspect_project(root)
        self.assertEqual(result["status"], "COMPATIBLE")
        self.assertNotIn("supaplate-provenance", result["evidence"])

    def test_incidental_supaplate_readme_mention_is_not_positive_provenance(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_complete_project(
                root,
                readme="# Generic project\n\nA migration guide mentions Supaplate among other options.\n",
            )
            result = self.detect_plate.inspect_project(root)
        self.assertEqual(result["status"], "COMPATIBLE")
        self.assertNotIn("supaplate-provenance", result["evidence"])

    def test_negated_supaplate_package_name_is_not_provenance(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_complete_project(root, package_name="not-supaplate")
            result = self.detect_plate.inspect_project(root)
        self.assertEqual(result["status"], "COMPATIBLE")
        self.assertNotIn("supaplate-provenance", result["evidence"])

    def test_negated_description_with_supaplate_url_is_not_provenance(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_complete_project(
                root,
                description="This is not Supaplate; see https://supaplate.com/docs",
            )
            result = self.detect_plate.inspect_project(root)
        self.assertEqual(result["status"], "COMPATIBLE")
        self.assertNotIn("supaplate-provenance", result["evidence"])

    def test_incidental_supaplate_url_is_not_provenance(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_complete_project(
                root,
                readme="# Generic project\n\nCompare alternatives at https://supaplate.com/docs.\n",
            )
            result = self.detect_plate.inspect_project(root)
        self.assertEqual(result["status"], "COMPATIBLE")
        self.assertNotIn("supaplate-provenance", result["evidence"])

    def test_structured_supaplate_provenance_signals_are_positive(self):
        cases = (
            {"package_name": "supaplate"},
            {"package_name": "@example/supaplate"},
            {"package_metadata": {"supaplateProvenance": True}},
            {"readme": "# Supaplate\n"},
            {"readme": "# Generic project\n\nSupaplate-Provenance: true\n"},
        )
        for case in cases:
            with self.subTest(case=case), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                package_metadata = case.get("package_metadata", {})
                write_complete_project(
                    root,
                    package_name=case.get("package_name", "generic-project"),
                    readme=case.get("readme", "# Generic project\n"),
                )
                if package_metadata:
                    update_package(root, **package_metadata)
                result = self.detect_plate.inspect_project(root)
                self.assertEqual(result["status"], "CONFIRMED")
                self.assertIn("supaplate-provenance", result["evidence"])

    def test_provenance_marker_within_bound_does_not_scan_invalid_tail(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_complete_project(root)
            prefix = b"# Generic project\nSupaplate-Provenance: true\n"
            bounded_prefix = prefix + (b"x" * ((64 * 1024) - len(prefix)))
            (root / "README.md").write_bytes(bounded_prefix + b"\xff")
            result = self.detect_plate.inspect_project(root)
        self.assertEqual(result["status"], "CONFIRMED")
        self.assertIn("supaplate-provenance", result["evidence"])

    def test_provenance_marker_beyond_bound_is_not_detected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_complete_project(root)
            bounded_prefix = b"# Generic project\n" + b"x" * (64 * 1024)
            (root / "README.md").write_bytes(
                bounded_prefix + b"\nSupaplate-Provenance: true\n"
            )
            result = self.detect_plate.inspect_project(root)
        self.assertEqual(result["status"], "COMPATIBLE")
        self.assertNotIn("supaplate-provenance", result["evidence"])

    def test_unrecognized_react_router_package_is_not_framework_mode(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_complete_project(root, router_name="@react-router/unrelated-plugin")
            result = self.detect_plate.inspect_project(root)
        self.assertEqual(result["status"], "UNSUPPORTED")
        self.assertIn("missing-react-router-framework-mode", result["missing"])

    def test_react_router_six_is_not_framework_mode(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_complete_project(root, router_version="6.0.0")
            result = self.detect_plate.inspect_project(root)
        self.assertEqual(result["status"], "UNSUPPORTED")
        self.assertIn("missing-react-router-framework-mode", result["missing"])
        self.assertEqual(result["versions"]["react-router"], "6.0.0")

    def test_react_router_seven_supported_ranges_are_framework_mode(self):
        versions = (
            "7",
            "7.5",
            "7.5.1",
            "^7.5.1",
            "~7.0.0",
            "^v7.5.1",
            "workspace:^7.5.1",
            "7.x",
            "7.x.x",
            "7.5.x",
            "v7.5.1-beta.1+build.2",
        )
        for version in versions:
            with self.subTest(version=version), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                write_complete_project(root, router_version=version)
                result = self.detect_plate.inspect_project(root)
                self.assertEqual(result["status"], "COMPATIBLE")
                self.assertIn("react-router-framework-mode", result["evidence"])
                self.assertEqual(result["versions"]["react-router"], version)

    def test_unknown_react_router_ranges_are_not_framework_mode(self):
        versions = (
            "*",
            "latest",
            "workspace:*",
            "7.x.2",
            "7.*.2",
            "7.5.x.1",
            "7.x-beta",
            "8",
            ">=7.0.0",
            "7 || 8",
            "7.05.01",
            "7.01",
            "7.00.0",
            "7.0.01",
            "7-beta",
            "7.5-beta",
            "7.1.0-01",
            "7.1.0-beta.01",
        )
        for version in versions:
            with self.subTest(version=version), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                write_complete_project(root, router_version=version)
                result = self.detect_plate.inspect_project(root)
                self.assertEqual(result["status"], "UNSUPPORTED")
                self.assertIn("missing-react-router-framework-mode", result["missing"])

    def test_binary_routes_file_is_not_a_readable_structure_marker(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_complete_project(root)
            (root / "app" / "routes.ts").write_bytes(b"\xff\xfe\x00")
            result = self.detect_plate.inspect_project(root)
        self.assertEqual(result["status"], "COMPATIBLE")
        self.assertIn("missing-app-routes", result["missing"])

    def test_utf8_control_bytes_are_not_readable_structure_text(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_complete_project(root)
            (root / "app" / "routes.ts").write_bytes(b"\x01\x02\x03")
            result = self.detect_plate.inspect_project(root)
        self.assertEqual(result["status"], "COMPATIBLE")
        self.assertIn("missing-app-routes", result["missing"])

    def test_large_utf8_routes_file_remains_readable_structure(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_complete_project(root)
            (root / "app" / "routes.ts").write_text("x" * (65 * 1024), encoding="utf-8")
            result = self.detect_plate.inspect_project(root)
        self.assertEqual(result["status"], "COMPATIBLE")
        self.assertIn("app-routes", result["evidence"])

    def test_binary_server_file_with_unsupported_suffix_is_not_a_marker(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_complete_project(root)
            server = root / "app" / "core" / "supabase" / "server.ts"
            unsupported = server.with_suffix(".bin")
            server.rename(unsupported)
            unsupported.write_bytes(b"\xff\xfe\x00")
            result = self.detect_plate.inspect_project(root)
        self.assertEqual(result["status"], "COMPATIBLE")
        self.assertIn("missing-server-side-supabase-marker", result["missing"])

    def test_large_utf8_server_file_remains_readable_structure(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_complete_project(root)
            server = root / "app" / "core" / "supabase" / "server.ts"
            server.write_text("x" * (65 * 1024), encoding="utf-8")
            result = self.detect_plate.inspect_project(root)
        self.assertEqual(result["status"], "COMPATIBLE")
        self.assertIn("server-side-supabase-marker", result["evidence"])

    def test_observer_file_is_not_a_server_marker(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_complete_project(root)
            server = root / "app" / "core" / "supabase" / "server.ts"
            server.rename(server.with_name("observer.ts"))
            result = self.detect_plate.inspect_project(root)
        self.assertEqual(result["status"], "COMPATIBLE")
        self.assertIn("missing-server-side-supabase-marker", result["missing"])

    def test_server_test_file_is_not_a_server_marker(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_complete_project(root)
            server = root / "app" / "core" / "supabase" / "server.ts"
            server.rename(server.with_name("server.test.ts"))
            result = self.detect_plate.inspect_project(root)
        self.assertEqual(result["status"], "COMPATIBLE")
        self.assertIn("missing-server-side-supabase-marker", result["missing"])

    def test_exact_server_file_under_supabase_directory_is_a_marker(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_complete_project(root)
            result = self.detect_plate.inspect_project(root)
        self.assertEqual(result["status"], "COMPATIBLE")
        self.assertIn("server-side-supabase-marker", result["evidence"])

    def test_plate_conventional_server_client_file_is_a_marker(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_complete_project(root)
            server = root / "app" / "core" / "supabase" / "server.ts"
            target = root / "app" / "core" / "lib" / "supa-client.server.ts"
            target.parent.mkdir(parents=True)
            server.rename(target)
            target.write_text(
                "import { createClient } from '@supabase/supabase-js';\n",
                encoding="utf-8",
            )
            result = self.detect_plate.inspect_project(root)
        self.assertEqual(result["status"], "COMPATIBLE")
        self.assertIn("server-side-supabase-marker", result["evidence"])

    def test_conventional_server_client_with_incomplete_utf8_at_eof_is_not_a_marker(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_complete_project(root)
            server = root / "app" / "core" / "supabase" / "server.ts"
            target = root / "app" / "core" / "lib" / "supa-client.server.ts"
            target.parent.mkdir(parents=True)
            server.rename(target)
            target.write_bytes(b"import '@supabase/supabase-js';\n\xe2")
            result = self.detect_plate.inspect_project(root)
        self.assertEqual(result["status"], "COMPATIBLE")
        self.assertIn("missing-server-side-supabase-marker", result["missing"])

    def test_conventional_server_client_rejects_invalid_tail_after_search_bound(self):
        for invalid_tail in (b"\xff", b"\x01"):
            with self.subTest(invalid_tail=invalid_tail), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                write_complete_project(root)
                server = root / "app" / "core" / "supabase" / "server.ts"
                target = root / "app" / "core" / "lib" / "supa-client.server.ts"
                target.parent.mkdir(parents=True)
                server.rename(target)
                prefix = b"supabase\n"
                target.write_bytes(
                    prefix + (b"x" * ((64 * 1024) - len(prefix))) + invalid_tail
                )
                result = self.detect_plate.inspect_project(root)
            self.assertEqual(result["status"], "COMPATIBLE")
            self.assertIn("missing-server-side-supabase-marker", result["missing"])

    def test_conventional_server_client_without_supabase_reference_is_not_a_marker(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_complete_project(root)
            server = root / "app" / "core" / "supabase" / "server.ts"
            target = root / "app" / "core" / "lib" / "supa-client.server.ts"
            target.parent.mkdir(parents=True)
            server.rename(target)
            target.write_text("export const client = true;\n", encoding="utf-8")
            result = self.detect_plate.inspect_project(root)
        self.assertEqual(result["status"], "COMPATIBLE")
        self.assertIn("missing-server-side-supabase-marker", result["missing"])

    def test_conventional_server_client_under_random_core_path_is_not_a_marker(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_complete_project(root)
            server = root / "app" / "core" / "supabase" / "server.ts"
            target = root / "app" / "core" / "random" / "supa-client.server.ts"
            target.parent.mkdir(parents=True)
            server.rename(target)
            target.write_text("import '@supabase/supabase-js';\n", encoding="utf-8")
            result = self.detect_plate.inspect_project(root)
        self.assertEqual(result["status"], "COMPATIBLE")
        self.assertIn("missing-server-side-supabase-marker", result["missing"])

    def test_conventional_server_client_at_core_root_is_not_a_marker(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_complete_project(root)
            server = root / "app" / "core" / "supabase" / "server.ts"
            target = root / "app" / "core" / "supa-client.server.ts"
            server.rename(target)
            target.write_text("import '@supabase/supabase-js';\n", encoding="utf-8")
            result = self.detect_plate.inspect_project(root)
        self.assertEqual(result["status"], "COMPATIBLE")
        self.assertIn("missing-server-side-supabase-marker", result["missing"])

    def test_invalid_or_missing_roots_are_errors(self):
        with self.assertRaises((FileNotFoundError, NotADirectoryError)):
            self.detect_plate.inspect_project(FIXTURES / "does-not-exist")
        with tempfile.NamedTemporaryFile() as file:
            with self.assertRaises(NotADirectoryError):
                self.detect_plate.inspect_project(file.name)

    def test_invalid_package_json_is_an_error(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "package.json").write_text("{ invalid", encoding="utf-8")
            with self.assertRaises(ValueError):
                self.detect_plate.inspect_project(root)

    def test_non_object_dependency_maps_are_errors(self):
        for map_name, value in (("dependencies", []), ("devDependencies", "invalid")):
            with self.subTest(map_name=map_name), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                (root / "package.json").write_text(
                    json.dumps({"name": "generic-project", map_name: value}),
                    encoding="utf-8",
                )
                with self.assertRaisesRegex(ValueError, rf"{map_name}.*object"):
                    self.detect_plate.inspect_project(root)

    def test_non_string_dependency_versions_are_errors(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "package.json").write_text(
                json.dumps({"dependencies": {"react-router": 7}}),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, r"dependencies.*react-router.*string"):
                self.detect_plate.inspect_project(root)

    def test_cli_success_prints_json_without_stderr(self):
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), str(FIXTURES / "confirmed-plate")],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0)
        self.assertEqual(json.loads(completed.stdout)["status"], "CONFIRMED")
        self.assertEqual(completed.stderr, "")

    def test_cli_invalid_input_is_concise_and_has_no_traceback(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "package.json").write_text("{ invalid", encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, str(SCRIPT), str(root)],
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertNotEqual(completed.returncode, 0)
        self.assertEqual(completed.stdout, "")
        self.assertRegex(completed.stderr, r"^error: invalid package\.json[^\n]*\n$")
        self.assertNotIn("Traceback", completed.stderr)


if __name__ == "__main__":
    unittest.main()
