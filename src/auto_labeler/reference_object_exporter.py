
"""Export reference-object annotations to JSON."""

import json
from pathlib import Path
from typing import List

from .reference_object import ReferenceObject


class ReferenceObjectExporter:
    """Export reference-object annotations in JSON format."""

    def export(
        self,
        objects: List[ReferenceObject],
        output_path: str = "data/reference_objects.json",
    ) -> Path:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        data = [obj.to_dict() for obj in objects]

        with path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)

        return path
