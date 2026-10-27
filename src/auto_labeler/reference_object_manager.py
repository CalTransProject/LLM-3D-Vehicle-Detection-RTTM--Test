"""Save and load reference-object annotations as JSON."""

import json
from pathlib import Path
from typing import Iterable

from .reference_object import BoundingBox, ReferenceObject


class ReferenceObjectManager:
    """Manage reference objects saved across dataset frames."""

    def __init__(self, file_path: str = "data/reference_objects.json"):
        self.file_path = Path(file_path)

    def save(self, objects: Iterable[ReferenceObject]) -> None:
        """Save reference objects to JSON."""
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump([obj.to_dict() for obj in objects], file, indent=2)

    def load(self) -> list[ReferenceObject]:
        """Load saved reference objects."""
        if not self.file_path.exists():
            return []

        with self.file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        return [
            ReferenceObject(
                frame_id=item["frame_id"],
                bbox=BoundingBox(**item["bbox"]),
                class_name=item.get("class_name", "Reference Object"),
                color=item.get("color", "#FFD700"),
            )
            for item in data
        ]

    def remove_all(self) -> int:
        """Remove all saved reference objects."""
        objects = self.load()
        count = len(objects)
        self.save([])
        return count

