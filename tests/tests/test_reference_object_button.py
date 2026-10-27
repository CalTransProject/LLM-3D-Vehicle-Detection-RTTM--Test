"""Tests for the reference-object apply button handler."""

import unittest

from src.auto_labeler.reference_object_tool import ReferenceObjectTool
from src.auto_labeler.reference_object_applier import ReferenceObjectApplier
from src.auto_labeler.reference_object_button import ReferenceObjectButton


class FakeManager:
    """In-memory manager for testing."""

    def __init__(self):
        self.objects = []

    def load(self):
        return list(self.objects)

    def save(self, objects):
        self.objects = list(objects)


class TestReferenceObjectButton(unittest.TestCase):
    def setUp(self):
        self.tool = ReferenceObjectTool()
        self.manager = FakeManager()
        self.applier = ReferenceObjectApplier(self.manager)
        self.button = ReferenceObjectButton(self.tool, self.applier)

    def test_button_applies_object_to_all_frames(self):
        self.tool.start_drag("frame_001", 10, 20)
        self.tool.finish_drag(50, 70)

        frame_ids = ["frame_001", "frame_002", "frame_003"]
        result = self.button.on_click(frame_ids)

        self.assertEqual(result, frame_ids)
        self.assertEqual(
            [obj.frame_id for obj in self.manager.objects],
            frame_ids,
        )

    def test_button_without_reference_object_raises_error(self):
        with self.assertRaises(ValueError):
            self.button.on_click(["frame_001"])


if __name__ == "__main__":
    unittest.main()
