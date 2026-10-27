"""Apply the same reference object annotation across multiple frames."""

from copy import deepcopy

from .reference_object import ReferenceObject
from .reference_object_manager import ReferenceObjectManager


class ReferenceObjectApplier:
    """Add or update a reference object in multiple frames."""

    def __init__(self, manager: ReferenceObjectManager):
        self.manager = manager

    def apply_to_frames(self, reference_object, frame_ids):
        """Save a copy of the reference object for each frame.

        Args:
            reference_object: ReferenceObject to apply to each frame.
            frame_ids: Iterable of frame identifiers.

        Returns:
            List of frame identifiers that were processed.
        """
        processed_frames = []

        # Load existing annotations so they are preserved.
        objects = self.manager.load()

        for frame_id in frame_ids:
            reference_copy = deepcopy(reference_object)
            reference_copy.frame_id = frame_id

            # Replace an existing annotation for this frame,
            # or add the reference object if none exists.
            objects = [
                obj for obj in objects
                if obj.frame_id != frame_id
            ]
            objects.append(reference_copy)
            processed_frames.append(frame_id)

        # Save all annotations using the manager's actual API.
        self.manager.save(objects)

        return processed_frames

