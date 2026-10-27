
"""Tests for saving and loading reference-object annotations."""

import json
import tempfile
import unittest
from pathlib import Path

from src.auto_labeler.reference_object import BoundingBox, ReferenceObject
from src.auto_labeler.reference_object_manager import ReferenceObjectManager


class TestReferenceObjectManager(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.file_path = Path(self.temp_dir.name) / "reference_objects.json"
        self.manager = ReferenceObjectManager(str(self.file_path))

        self.objects = [
            ReferenceObject(
                frame_id="frame_001",
                bbox=BoundingBox(10, 20, 40, 50),
            ),
            ReferenceObject(
                frame_id="frame_002",
                bbox=BoundingBox(10, 20, 40, 50),
            ),
        ]

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_save_creates_json_file(self):
        self.manager.save(self.objects)

        self.assertTrue(self.file_path.exists())

        with self.file_path.open(encoding="utf-8") as file:
            data = json.load(file)

        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["frame_id"], "frame_001")
        self.assertEqual(data[1]["frame_id"], "frame_002")

    def test_load_returns_saved_objects(self):
        self.manager.save(self.objects)

        loaded = self.manager.load()

        self.assertEqual(len(loaded), 2)
        self.assertEqual(
            [obj.frame_id for obj in loaded],
            ["frame_001", "frame_002"],
        )

        for obj in loaded:
            self.assertEqual(obj.bbox.x, 10)
            self.assertEqual(obj.bbox.y, 20)
            self.assertEqual(obj.bbox.width, 40)
            self.assertEqual(obj.bbox.height, 50)

    def test_load_returns_empty_list_when_file_missing(self):
        self.assertEqual(self.manager.load(), [])

    def test_save_overwrites_previous_annotations(self):
        self.manager.save(self.objects)
        self.manager.save([self.objects[0]])

        loaded = self.manager.load()

        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0].frame_id, "frame_001")


if __name__ == "__main__":
    unittest.main()

