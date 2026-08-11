import unittest

from game.modules.persist_schema import *


class SchemaManifestTests(unittest.TestCase):
    def test_fresh_root_has_exact_twelve_leaves(self):
        root = build_fresh_persist_root()
        self.assertEqual(count_normative_leaves(root), 12)
        self.assertEqual(root["collection_epoch_id"], 0)
        self.assertEqual(root["settings"]["font_scale"], 1.0)

    def test_invalid_container_and_protocol_value_fail_closed(self):
        root = build_fresh_persist_root()
        with self.assertRaises(PersistSchemaError):
            validate_persist_root({"settings": root["settings"]})
        class Bomb:
            def __iter__(self):
                raise AssertionError("bomb invoked")
        with self.assertRaises(PersistSchemaError):
            validate_persist_root(Bomb())

    def test_ids_and_settings_are_canonical(self):
        root = build_fresh_persist_root()
        root["achievement_ids"] = ["B", "A"]
        with self.assertRaises(PersistSchemaError):
            validate_persist_root(root)
        root = build_fresh_persist_root()
        root["settings"]["high_contrast"] = 1
        with self.assertRaises(PersistSchemaError):
            validate_persist_root(root)

    def test_snapshot_is_detached_and_manifest_is_exact(self):
        root = build_fresh_persist_root()
        snapshot = snapshot_persist_root(root)
        snapshot["settings"]["high_contrast"] = True
        self.assertFalse(root["settings"]["high_contrast"])
        manifest = build_ownership_manifest()
        validate_ownership_manifest(manifest)
        self.assertEqual(len(manifest["leaf_paths"]), 12)


if __name__ == "__main__":
    unittest.main()
