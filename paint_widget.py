# paint_widget.py
from __future__ import annotations
from typing import Optional
from simple_widget import SimpleWidget
from graphics.graphics_library import GraphicsLibrary
from graphics.graphics_pipeline import GraphicsPipeline
from asset_bundle import AssetBundle
from graphics.graphics_sprite_2d_instance import GraphicsSprite2DInstance
from graphics.graphics_shape_2d_instance import GraphicsShape2DInstance
from graphics.graphics_matrix import GraphicsMatrix

class PaintWidget(SimpleWidget):
    def __init__(self, graphics: GraphicsLibrary, pipeline: GraphicsPipeline) -> None:
        super().__init__(graphics, pipeline)

        self.image_instance = GraphicsSprite2DInstance()


        self.marker_instance_1 = GraphicsShape2DInstance()
        self.marker_instance_2 = GraphicsShape2DInstance()
        self.marker_instance_3 = GraphicsShape2DInstance()

    # -------- Frame -----------------------------------------------------

    def set_frame(self, x: float, y: float, width: float, height: float) -> None:

        left = x
        right = (x + width)
        top = y
        bottom = y + height

        inset_1 = 0.0
        inset_2 = 2.0
        inset_3 = 4.0
        
        self.marker_instance_1.set_position_frame(x + inset_1, y + inset_1, width - inset_1 * 2.0, height - inset_1 * 2.0)
        self.marker_instance_2.set_position_frame(x + inset_2, y + inset_2, width - inset_2 * 2.0, height - inset_2 * 2.0)
        self.marker_instance_3.set_position_frame(x + inset_3, y + inset_3, width - inset_3 * 2.0, height - inset_3 * 2.0)


    # -------- Loading ---------------------------------------------------

    def load(self, assets: Optional[AssetBundle]) -> None:
        self.image_instance.load(self.graphics, assets.ball_sprite)

    # -------- Lifecycle -------------------------------------------------

    def update(self, dt: float) -> None:
        pass

    def draw(self) -> None:
        graphics = self.graphics
        pipeline = self.pipeline
        sprite_program = pipeline.program_sprite_2d

        width = float(graphics.frame_buffer_width)
        height = float(graphics.frame_buffer_height)

        # Ortho projection matching the framebuffer
        projection_matrix = GraphicsMatrix()
        projection_matrix.ortho_size(width=width, height=height)

        # Basic alpha blending
        graphics.blend_set_alpha()

        self.image_instance.projection_matrix = projection_matrix.copy()
        self.image_instance.model_view_matrix = GraphicsMatrix()

        self.image_instance.render(sprite_program)


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
