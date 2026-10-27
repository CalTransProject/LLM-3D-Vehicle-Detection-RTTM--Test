
"""Tkinter UI for applying a reference object across frames."""

import tkinter as tk
from tkinter import messagebox

from .reference_object_workflow import ReferenceObjectWorkflow


class ReferenceObjectUI:
    """Display a reference-object drawing and apply interface."""

    def __init__(self, root=None, workflow=None):
        self.root = root or tk.Tk()
        self.workflow = workflow or ReferenceObjectWorkflow()

        self.root.title("Reference Object Tool")
        self.root.geometry("800x600")

        self.frame_id = tk.StringVar(value="frame_001")
        self.frame_ids = tk.StringVar(
            value="frame_001, frame_002, frame_003"
        )

        self.canvas = None
        self.drag_start = None
        self.rectangle_id = None

        self._build_ui()

    def _build_ui(self):
        """Create the UI controls and drawing canvas."""
        controls = tk.Frame(self.root, padx=10, pady=10)
        controls.pack(fill=tk.X)

        tk.Label(controls, text="Current frame ID:").grid(
            row=0, column=0, sticky="w"
        )
        tk.Entry(
            controls, textvariable=self.frame_id, width=20
        ).grid(row=0, column=1, padx=5)

        tk.Label(controls, text="Frames to apply to:").grid(
            row=1, column=0, sticky="w"
        )
        tk.Entry(
            controls, textvariable=self.frame_ids, width=45
        ).grid(row=1, column=1, padx=5)

        tk.Button(
            controls,
            text="Apply to All Frames",
            command=self._apply_to_frames,
        ).grid(row=2, column=0, columnspan=2, pady=8)

        self.canvas = tk.Canvas(
            self.root,
            bg="#202020",
            width=760,
            height=450,
            cursor="crosshair",
        )
        self.canvas.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.canvas.bind("<ButtonPress-1>", self._start_box)
        self.canvas.bind("<B1-Motion>", self._update_box)
        self.canvas.bind("<ButtonRelease-1>", self._finish_box)

        tk.Label(
            self.root,
            text="Drag on the canvas to draw a reference bounding box.",
        ).pack(pady=(0, 10))

    def _start_box(self, event):
        """Begin drawing a box on the canvas."""
        frame_id = self.frame_id.get().strip()
        if not frame_id:
            messagebox.showerror("Missing frame", "Enter a frame ID.")
            return

        self.drag_start = (event.x, event.y)
        self.workflow.start_drawing(frame_id, event.x, event.y)

        if self.rectangle_id is not None:
            self.canvas.delete(self.rectangle_id)

        self.rectangle_id = self.canvas.create_rectangle(
            event.x,
            event.y,
            event.x + 1,
            event.y + 1,
            outline="#FFD700",
            width=2,
        )

    def _update_box(self, event):
        """Update the visible box while dragging."""
        if self.drag_start is None:
            return

        start_x, start_y = self.drag_start

        self.canvas.coords(
            self.rectangle_id,
            start_x,
            start_y,
            event.x,
            event.y,
        )

        self.workflow.update_drawing(event.x, event.y)

    def _finish_box(self, event):
        """Finish drawing the reference box."""
        if self.drag_start is None:
            return

        self.workflow.finish_drawing(event.x, event.y)
        self.drag_start = None

    def _apply_to_frames(self):
        """Apply the current box to the listed frame IDs."""
        frame_ids = [
            item.strip()
            for item in self.frame_ids.get().split(",")
            if item.strip()
        ]

        if not frame_ids:
            messagebox.showerror(
                "Missing frames",
                "Enter at least one frame ID.",
            )
            return

        try:
            processed = self.workflow.apply_to_frames(frame_ids)
        except (ValueError, OSError, TypeError, AttributeError) as error:
            messagebox.showerror("Apply failed", str(error))
            return

        messagebox.showinfo(
            "Reference object applied",
            f"Applied the reference object to {len(processed)} frames.\n"
            f"Saved annotations to the configured JSON file.",
        )


def main():
    """Launch the reference-object interface."""
    root = tk.Tk()
    ReferenceObjectUI(root=root)
    root.mainloop()


if __name__ == "__main__":
    main()
