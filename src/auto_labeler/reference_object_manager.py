
"""Save and load reference-object annotations as JSON."""

import json
from pathlib import Path
from typing import Dict, List

from .reference_object import ReferenceObject, BoundingBox


class ReferenceObjectManager:
    """Manage reference-object annotations in a JSON file."""

    def __init__(self, file_path: str = "data/reference_objects.json"):
        self.file_path = Path(file_path)

    def save(self, objects: List[ReferenceObject]) -> None:
        """Save reference objects to a JSON file."""
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        data = [obj.to_dict() for obj in objects]

        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)

    def load(self) -> List[ReferenceObject]:
        """Load reference objects from a JSON file."""
        if not self.file_path.exists():
            return []

        with self.file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError("Reference-object data must be a JSON list.")

        objects = []

        for item in data:
            bbox_data = item["bbox"]
            bbox = BoundingBox(
                x=bbox_data["x"],
                y=bbox_data["y"],
                width=bbox_data["width"],
                height=bbox_data["height"],
            )

            objects.append(
                ReferenceObject(
                    frame_id=item["frame_id"],
                    bbox=bbox,
                    class_name=item.get("class_name", "Reference Object"),
                    color=item.get("color", "#FFD700"),
                )
            )

        return objects
