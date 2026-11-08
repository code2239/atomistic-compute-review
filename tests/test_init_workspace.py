"""Filesystem behavior tests; no engines, inference, or external services."""

import importlib.util
from pathlib import Path
import tempfile
import unittest


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "skills/atomistic-compute-review/scripts/init_workspace.py"
)
SPEC = importlib.util.spec_from_file_location("workspace_initializer", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class InitializeWorkspaceTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def test_creates_only_core_layout_and_index(self):
        MODULE.initialize_workspace(self.root)
        self.assertEqual(
            {p.name for p in self.root.iterdir()}, set(MODULE.CORE_DIRECTORIES)
        )
        self.assertEqual(
            {str(p.relative_to(self.root)) for p in self.root.rglob("*") if p.is_file()},
            {"docs/index.md"},
        )

    def test_repeat_preserves_index_and_existing_artifacts(self):
        MODULE.initialize_workspace(self.root)
        index = self.root / "docs/index.md"
        index.write_text("用户维护的索引\n", encoding="utf-8")
        source = self.root / "input/POSCAR"
        source.write_bytes(b"existing input\n")
        result = MODULE.initialize_workspace(self.root)
        self.assertEqual(index.read_text(encoding="utf-8"), "用户维护的索引\n")
        self.assertEqual(source.read_bytes(), b"existing input\n")
        self.assertEqual(result["directories_created"], [])
        self.assertEqual(result["index"]["action"], "kept")

    def test_check_makes_no_changes(self):
        result = MODULE.initialize_workspace(self.root, check_only=True)
        self.assertEqual(list(self.root.iterdir()), [])
        self.assertEqual(result["directories_to_create"], list(MODULE.CORE_DIRECTORIES))

    def test_directory_conflict_fails_before_any_creation(self):
        conflict = self.root / "output"
        conflict.write_bytes(b"keep this file")
        with self.assertRaises(ValueError):
            MODULE.initialize_workspace(self.root)
        self.assertEqual(list(self.root.iterdir()), [conflict])
        self.assertEqual(conflict.read_bytes(), b"keep this file")

    def test_index_directory_conflict_fails_before_creation(self):
        (self.root / "docs/index.md").mkdir(parents=True)
        with self.assertRaises(ValueError):
            MODULE.initialize_workspace(self.root)
        self.assertEqual({p.name for p in self.root.iterdir()}, {"docs"})

    def test_symlink_is_not_followed_or_replaced(self):
        with tempfile.TemporaryDirectory() as outside:
            link = self.root / "docs"
            link.symlink_to(outside, target_is_directory=True)
            with self.assertRaises(ValueError):
                MODULE.initialize_workspace(self.root)
            self.assertTrue(link.is_symlink())
            self.assertEqual(list(Path(outside).iterdir()), [])
            self.assertEqual(list(self.root.iterdir()), [link])

    def test_index_symlink_does_not_change_target(self):
        (self.root / "docs").mkdir()
        target = self.root / "original.md"
        target.write_bytes(b"keep original")
        (self.root / "docs/index.md").symlink_to(target)
        with self.assertRaises(ValueError):
            MODULE.initialize_workspace(self.root)
        self.assertEqual(target.read_bytes(), b"keep original")
        self.assertFalse((self.root / "input").exists())

    def test_missing_project_is_not_created(self):
        missing = self.root / "missing-project"
        with self.assertRaises(ValueError):
            MODULE.initialize_workspace(missing)
        self.assertFalse(missing.exists())


if __name__ == "__main__":
    unittest.main()
