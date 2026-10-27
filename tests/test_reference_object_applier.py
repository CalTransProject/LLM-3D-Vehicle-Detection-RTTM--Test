"""Tests for applying a reference object across multiple frames."""

import unittest
from copy import deepcopy

from auto_labeler.reference_object_applier import ReferenceObjectApplier


class FakeManager:
    """Store reference object annotations for each frame."""

    def __init__(self):
        self.objects_by_frame = {}

    def save_reference_object(self, frame_id, reference_object):
        """Save a reference object for a specific frame."""
        self.objects_by_frame[frame_id] = reference_object


class TestReferenceObjectApplier(unittest.TestCase):
    """Test reference object application across frames."""

    def setUp(self):
        self.manager = FakeManager()
        self.applier = ReferenceObjectApplier(self.manager)

        self.reference_object = {
            "label": "reference_object",
            "bbox": [10, 20, 100, 80],
        }

        self.frame_ids = [0, 1, 2]

    def test_applies_reference_object_to_all_frames(self):
        """The same reference object should be saved for every frame."""
        processed_frames = self.applier.apply_to_frames(
            self.reference_object,
            self.frame_ids,
        )

        self.assertEqual(processed_frames, self.frame_ids)
        self.assertEqual(
            list(self.manager.objects_by_frame.keys()),
            self.frame_ids,
        )

        for frame_id in self.frame_ids:
            self.assertEqual(
                self.manager.objects_by_frame[frame_id],
                self.reference_object,
            )

    def test_each_frame_receives_a_separate_copy(self):
        """Changing one frame's object should not change another's."""
        self.applier.apply_to_frames(
            self.reference_object,
            self.frame_ids,
        )

        first = self.manager.objects_by_frame[0]
        second = self.manager.objects_by_frame[1]

        self.assertIsNot(first, second)
        self.assertIsNot(first, self.reference_object)

        first["bbox"][0] = 999

        self.assertEqual(
            self.manager.objects_by_frame[1]["bbox"],
            [10, 20, 100, 80],
        )
        self.assertEqual(
            self.reference_object["bbox"],
            [10, 20, 100, 80],
        )

    def test_empty_frame_list(self):
        """No frames should be processed when the list is empty."""
        processed_frames = self.applier.apply_to_frames(
            self.reference_object,
            [],
        )

        self.assertEqual(processed_frames, [])
        self.assertEqual(self.manager.objects_by_frame, {})


if __name__ == "__main__":
    unittest.main()
