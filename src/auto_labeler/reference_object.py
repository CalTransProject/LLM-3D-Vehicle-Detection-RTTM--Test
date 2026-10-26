
# Import dataclass to automatically generate initialization methods.
# Import asdict to convert objects into dictionaries.
from dataclasses import dataclass, asdict

# Dict is used to describe the dictionary returned by our methods.
from typing import Dict


# Name used to identify the reference object in the annotation tool.
REFERENCE_OBJECT_CLASS = "Reference Object"

# Gold color makes the reference object visually different
# from the existing vehicle classes.
REFERENCE_OBJECT_COLOR = "#FFD700"


@dataclass
class BoundingBox:
    # Coordinates of the top-left corner of the bounding box.
    x: float
    y: float

    # Width and height determine the size of the bounding box.
    width: float
    height: float

    def __post_init__(self):
        # Make sure the bounding box has a valid, positive size.
        if self.width <= 0 or self.height <= 0:
            raise ValueError(
                "Bounding-box width and height must be positive."
            )

    def move(self, x: float, y: float) -> None:
        # Update the top-left corner to move the bounding box.
        self.x = x
        self.y = y

    def resize(self, width: float, height: float) -> None:
        # Check that the new dimensions are positive.
        if width <= 0 or height <= 0:
            raise ValueError("Width and height must be positive.")

        # Apply the new width and height to the bounding box.
        self.width = width
        self.height = height

    def to_dict(self) -> Dict:
        # Convert the bounding-box coordinates and dimensions
        # into a dictionary for storage or JSON serialization.
        return asdict(self)


@dataclass
class ReferenceObject:
    # Identifier of the video or LiDAR frame containing the object.
    frame_id: str

    # Bounding box that identifies the reference object in the frame.
    bbox: BoundingBox

    # Assign the default reference-object label and gold color.
    class_name: str = REFERENCE_OBJECT_CLASS
    color: str = REFERENCE_OBJECT_COLOR

    def to_dict(self) -> Dict:
        # Convert the reference annotation into a dictionary.
        # The bounding box is stored alongside its frame and label.
        return {
            "frame_id": self.frame_id,
            "class_name": self.class_name,
            "color": self.color,
            "bbox": self.bbox.to_dict(),
        }

