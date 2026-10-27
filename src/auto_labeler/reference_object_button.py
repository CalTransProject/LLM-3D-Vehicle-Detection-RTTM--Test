"""Button handler for applying a reference object across frames."""

from typing import Iterable

from .reference_object_applier import ReferenceObjectApplier
from .reference_object_tool import ReferenceObjectTool


class ReferenceObjectButton:
    """Connect a UI button action to reference-object application."""

    def __init__(
        self,
        tool: ReferenceObjectTool,
        applier: ReferenceObjectApplier,
    ) -> None:
        self.tool = tool
        self.applier = applier

    def on_click(self, frame_ids: Iterable[str]) -> list:
        """Apply the current reference object to the supplied frames."""
        if self.tool.reference_object is None:
            raise ValueError(
                "Create a reference object before applying it."
            )

        return self.tool.apply_to_frames(
            self.applier,
            frame_ids,
        )
