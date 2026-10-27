
import unittest

from src.auto_labeler.reference_object_tool import ReferenceObjectTool


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


if __name__ == "__main__":
    unittest.main()
