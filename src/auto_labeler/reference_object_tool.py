
"""Interactive reference-object bounding box tool."""

from dataclasses import asdict, dataclass
from typing import Dict, Optional, Tuple

REFERENCE_OBJECT_CLASS = "Reference Object"
REFERENCE_OBJECT_COLOR = "#FFD700"


@dataclass
class BoundingBox:
    x: float
    y: float
    width: float
    height: float

    def __post_init__(self) -> None:
        if self.width <= 0 or self.height <= 0:
            raise ValueError("Bounding-box dimensions must be positive.")

    def move(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def resize(self, width: float, height: float) -> None:
        if width <= 0 or height <= 0:
            raise ValueError("Bounding-box dimensions must be positive.")
        self.width = width
        self.height = height

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class ReferenceObject:
    frame_id: str
    bbox: BoundingBox
    class_name: str = REFERENCE_OBJECT_CLASS
    color: str = REFERENCE_OBJECT_COLOR

    def to_dict(self) -> Dict:
        return {
            "frame_id": self.frame_id,
            "class_name": self.class_name,
            "color": self.color,
            "bbox": self.bbox.to_dict(),
        }


class ReferenceObjectTool:
    """Manage one reference-object box using frame coordinates.

    Call start_drag(), update_drag(), and finish_drag() from
    your interface's mouse event handlers.
    """

    def __init__(self) -> None:
        self.reference_object: Optional[ReferenceObject] = None
        self._drag_start: Optional[Tuple[float, float]] = None

    def start_drag(
        self, frame_id: str, x: float, y: float
    ) -> None:
        """Begin drawing a new box at the mouse position."""
        self._drag_start = (x, y)
        self.reference_object = ReferenceObject(
            frame_id=frame_id,
            bbox=BoundingBox(x, y, 1, 1),
        )

    def update_drag(self, x: float, y: float) -> None:
        """Update the box while the mouse is moving."""
        if self._drag_start is None or self.reference_object is None:
            return

        start_x, start_y = self._drag_start
        left, top = min(start_x, x), min(start_y, y)
        width, height = abs(x - start_x), abs(y - start_y)

        # Keep dimensions positive while the user is dragging.
        self.reference_object.bbox = BoundingBox(
            left, top, max(width, 1), max(height, 1)
        )

    def finish_drag(self, x: float, y: float) -> None:
        """Finish drawing the box and validate its final dimensions."""
        if self._drag_start is None:
            return

        self.update_drag(x, y)
        self._drag_start = None

    def resize(self, width: float, height: float) -> None:
        """Set the box size while keeping its top-left position."""
        if self.reference_object is None:
            raise ValueError("Create a reference box first.")

        self.reference_object.bbox.resize(width, height)

    def remove(self, x: float, y: float) -> bool:
        """Remove the box when the user clicks inside it."""
        obj = self.reference_object
        if obj is None:
            return False

        box = obj.bbox
        if (
            box.x <= x <= box.x + box.width
            and box.y <= y <= box.y + box.height
        ):
            self.reference_object = None
            self._drag_start = None
            return True

        return False

    def to_dict(self) -> Optional[Dict]:
        """Return the current box data, or None if no box exists."""
        if self.reference_object is None:
            return None
        return self.reference_object.to_dict()
