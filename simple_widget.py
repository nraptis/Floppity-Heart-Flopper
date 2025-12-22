# simple_widget.py
from __future__ import annotations
from typing import Optional
from graphics.graphics_library import GraphicsLibrary
from graphics.graphics_pipeline import GraphicsPipeline
from asset_bundle import AssetBundle


class SimpleWidget:

    def __init__(self, graphics: GraphicsLibrary, pipeline: GraphicsPipeline) -> None:
        self.graphics = graphics
        self.pipeline = pipeline

        # Frame-related properties
        self.frame_x: float = 0.0
        self.frame_y: float = 0.0
        self.frame_width: float = 0.0
        self.frame_height: float = 0.0

    # -------- Frame -----------------------------------------------------

    def set_frame(self, x: float, y: float, width: float, height: float) -> None:
        self.frame_x = x
        self.frame_y = y
        self.frame_width = width
        self.frame_height = height

    # -------- Loading ---------------------------------------------------

    def load(self, assets: Optional[AssetBundle]) -> None:
        pass

    # -------- Lifecycle -------------------------------------------------

    def update(self, dt: float) -> None:
        pass

    def draw(self) -> None:
        pass

    def dispose(self) -> None:
        pass

    # -------- Input -----------------------------------------------------

    def mouse_down(self, button: int, xpos: float, ypos: float) -> None:
        pass

    def mouse_up(self, button: int, xpos: float, ypos: float) -> None:
        pass

    def mouse_move(self, xpos: float, ypos: float) -> None:
        pass

    def mouse_wheel(self, direction: int) -> None:
        pass
