"""Coordinate reference-object creation, application, and persistence."""

from typing import Iterable

from .reference_object_applier import ReferenceObjectApplier
from .reference_object_button import ReferenceObjectButton
from .reference_object_manager import ReferenceObjectManager
from .reference_object_tool import ReferenceObjectTool


class ReferenceObjectWorkflow:
    """Coordinate the reference-object workflow across frames."""

    def __init__(self, file_path: str = "data/reference_objects.json"):
        self.manager = ReferenceObjectManager(file_path)
        self.tool = ReferenceObjectTool()
        self.applier = ReferenceObjectApplier(self.manager)
        self.button = ReferenceObjectButton(self.tool, self.applier)

    def start_drawing(self, frame_id: str, x: float, y: float) -> None:
        """Start drawing a reference-object bounding box."""
        self.tool.start_drag(frame_id, x, y)

    def update_drawing(self, x: float, y: float) -> None:
        """Update the bounding box during dragging."""
        self.tool.update_drag(x, y)

    def finish_drawing(self, x: float, y: float) -> None:
        """Finish drawing the bounding box."""
        self.tool.finish_drag(x, y)

    def apply_to_frames(self, frame_ids: Iterable[str]) -> list:
        """Apply the reference object to all supplied frames and save it."""
        return self.button.on_click(frame_ids)

    def get_reference_object(self):
        """Return the current reference-object data."""
        return self.tool.to_dict()

    def load_saved_objects(self):
        """Return reference objects saved in the JSON file."""
        return self.manager.load()
