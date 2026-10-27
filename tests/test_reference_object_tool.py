
import unittest

from src.auto_labeler.reference_object_tool import ReferenceObjectTool
from src.auto_labeler.reference_object_applier import ReferenceObjectApplier


class FakeManager:
    """Store reference objects by frame."""

    def __init__(self):
        self.objects = []

    def load(self):
        return list(self.objects)

    def save(self, objects):
        self.objects = list(objects)


class TestReferenceObjectTool(unittest.TestCase):
    def setUp(self):
        self.tool = ReferenceObjectTool()

    def test_drag_creates_reference_box(self):
        self.tool.start_drag("frame_001", 10, 20)
        self.tool.update_drag(50, 70)
        self.tool.finish_drag(50, 70)

        data = self.tool.to_dict()

        self.assertEqual(data["class_name"], "Reference Object")
        self.assertEqual(data["color"], "#FFD700")
        self.assertEqual(data["bbox"]["x"], 10)
        self.assertEqual(data["bbox"]["y"], 20)
        self.assertEqual(data["bbox"]["width"], 40)
        self.assertEqual(data["bbox"]["height"], 50)

    def test_resize_reference_box(self):
        self.tool.start_drag("frame_001", 10, 20)
        self.tool.finish_drag(50, 70)
        self.tool.resize(60, 80)

        data = self.tool.to_dict()

        self.assertEqual(data["bbox"]["width"], 60)
        self.assertEqual(data["bbox"]["height"], 80)

    def test_click_inside_removes_box(self):
        self.tool.start_drag("frame_001", 10, 20)
        self.tool.finish_drag(50, 70)

        removed = self.tool.remove(30, 40)

        self.assertTrue(removed)
        self.assertIsNone(self.tool.to_dict())

    def test_click_outside_keeps_box(self):
        self.tool.start_drag("frame_001", 10, 20)
        self.tool.finish_drag(50, 70)

        removed = self.tool.remove(100, 100)

        self.assertFalse(removed)
        self.assertIsNotNone(self.tool.to_dict())

    def test_apply_reference_object_to_multiple_frames(self):
        self.tool.start_drag("frame_001", 10, 20)
        self.tool.finish_drag(50, 70)

        manager = FakeManager()
        applier = ReferenceObjectApplier(manager)

        processed = self.tool.apply_to_frames(
            applier,
            ["frame_001", "frame_002", "frame_003"],
        )

        self.assertEqual(
            processed,
            ["frame_001", "frame_002", "frame_003"],
        )
        self.assertEqual(len(manager.objects), 3)
        self.assertEqual(
            [obj.frame_id for obj in manager.objects],
            ["frame_001", "frame_002", "frame_003"],
        )

        for obj in manager.objects:
            self.assertEqual(obj.bbox.x, 10)
            self.assertEqual(obj.bbox.y, 20)
            self.assertEqual(obj.bbox.width, 40)
            self.assertEqual(obj.bbox.height, 50)

    def test_apply_without_reference_box_raises_error(self):
        manager = FakeManager()
        applier = ReferenceObjectApplier(manager)

        with self.assertRaises(ValueError):
            self.tool.apply_to_frames(applier, ["frame_001"])


if __name__ == "__main__":
    unittest.main()

