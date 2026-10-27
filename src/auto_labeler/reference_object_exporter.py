
"""Export reference-object annotations to JSON."""

import json
from pathlib import Path
from typing import Iterable, Optional

from .reference_object import ReferenceObject


class ReferenceObjectExporter:
    """Export reference-object annotations to a JSON file."""

    def export(
        self,
        objects: Iterable[ReferenceObject],
        file_path: str = "data/reference_objects_export.json",
    ) -> str:
        """Write reference-object annotations to JSON.

        Args:
            objects: Reference objects to export.
            file_path: Destination JSON file path.

        Returns:
            The destination path as a string.
        """
        destination = Path(file_path)
        destination.parent.mkdir(parents=True, exist_ok=True)

        data = [obj.to_dict() for obj in objects]

        with destination.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)

        return str(destination)

    def export_from_manager(
        self,
        manager,
        file_path: str = "data/reference_objects_export.json",
    ) -> str:
        """Export all annotations currently saved by the manager."""
        objects = manager.load()
        return self.export(objects, file_path)
