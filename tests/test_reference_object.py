
import unittest

from src.auto_labeler.reference_object import (
    BoundingBox,
    ReferenceObject,
    REFERENCE_OBJECT_COLOR,
    REFERENCE_OBJECT_CLASS,
)


class TestBoundingBox(unittest.TestCase):
    def test_valid_dimensions(self):
        box = BoundingBox(10, 20, 30, 40)
        self.assertEqual(box.width, 30)
        self.assertEqual(box.height, 40)

    def test_invalid_dimensions(self):
        with self.assertRaises(ValueError):
            BoundingBox(10, 20, 0, 40)

    def test_move(self):
        box = BoundingBox(10, 20, 30, 40)
        box.move(15, 25)
        self.assertEqual((box.x, box.y), (15, 25))

    def test_resize(self):
        box = BoundingBox(10, 20, 30, 40)
        box.resize(50, 60)
        self.assertEqual((box.width, box.height), (50, 60))

    def test_invalid_resize(self):
        box = BoundingBox(10, 20, 30, 40)
        with self.assertRaises(ValueError):
            box.resize(0, 60)


class TestReferenceObject(unittest.TestCase):
    def test_default_class_and_color(self):
        obj = ReferenceObject("frame_001", BoundingBox(10, 20, 30, 40))
        self.assertEqual(obj.class_name, REFERENCE_OBJECT_CLASS)
        self.assertEqual(obj.color, REFERENCE_OBJECT_COLOR)

    def test_to_dict(self):
        obj = ReferenceObject("frame_001", BoundingBox(10, 20, 30, 40))
        result = obj.to_dict()

        self.assertEqual(result["frame_id"], "frame_001")
        self.assertEqual(result["class_name"], "Reference Object")
        self.assertEqual(result["color"], "#FFD700")
        self.assertEqual(result["bbox"]["width"], 30)


if __name__ == "__main__":
    unittest.main()
