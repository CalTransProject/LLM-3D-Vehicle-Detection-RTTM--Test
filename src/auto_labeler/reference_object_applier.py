
"""Apply the same reference object annotation across multiple frames."""

from copy import deepcopy


class ReferenceObjectApplier:
    """Add or update a reference object in every frame's annotations."""

    def __init__(self, manager):
        self.manager = manager

    def apply_to_frames(self, reference_object, frame_ids):
        """Save the same reference object for each supplied frame.

        Args:
            reference_object: The reference object to copy.
            frame_ids: Iterable of frame identifiers.

        Returns:
            The frame identifiers that were processed.
        """
        processed_frames = []

        for frame_id in frame_ids:
            reference_copy = deepcopy(reference_object)

            # Give each frame its own copy to avoid shared mutable state.
            self.manager.save_reference_object(
                frame_id,
                reference_copy,
            )

            processed_frames.append(frame_id)

        return processed_frames
