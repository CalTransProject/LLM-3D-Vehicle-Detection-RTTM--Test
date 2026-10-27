
"""Apply the same reference object annotation across multiple frames."""

from copy import deepcopy

from .reference_object import ReferenceObject
from .reference_object_manager import ReferenceObjectManager


class ReferenceObjectApplier:
    """Add or update a reference object in multiple frames."""

    def __init__(self, manager: ReferenceObjectManager):
        self.manager = manager

    def apply_to_frames(self, reference_object, frame_ids):
        """Save a separate copy of the reference object for each frame."""
        frame_ids = list(frame_ids)
        if not frame_ids:
            return []

        # Support the older manager API used by existing tests.
        if hasattr(self.manager, "save_reference_object"):
            for frame_id in frame_ids:
                reference_copy = deepcopy(reference_object)
                self.manager.save_reference_object(frame_id, reference_copy)
            return frame_ids

        # Load existing annotations so they are preserved.
        objects = self.manager.load()

        for frame_id in frame_ids:
            reference_copy = deepcopy(reference_object)

            if isinstance(reference_copy, dict):
                reference_copy["frame_id"] = frame_id
            else:
                reference_copy.frame_id = frame_id

            objects = [
                obj for obj in objects
                if getattr(obj, "frame_id", None) != frame_id
            ]
            objects.append(reference_copy)

        self.manager.save(objects)
        return frame_ids

