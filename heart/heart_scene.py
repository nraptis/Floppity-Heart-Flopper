# pong_scene.py
from __future__ import annotations
from OpenGL import GL as gl
from filesystem.file_utils import FileUtils
from graphics.graphics_scene import GraphicsScene
from graphics.graphics_primitives import Sprite2DVertex
from graphics.graphics_array_buffer import GraphicsArrayBuffer
from graphics.graphics_library import GraphicsLibrary
from graphics.graphics_pipeline import GraphicsPipeline
from graphics.graphics_matrix import GraphicsMatrix
from graphics.graphics_color import GraphicsColor
from graphics.graphics_shape_2d_instance import GraphicsShape2DInstance
from graphics.graphics_sprite_2d_instance import GraphicsSprite2DInstance

from graphics.graphics_texture import GraphicsTexture
from heart.heart_asset_bundle import HeartAssetBundle
import random

rng = random.Random()

class HeartScene(GraphicsScene):

    def __init__(self,
                 graphics: GraphicsLibrary,
                 pipeline: GraphicsPipeline,
                 assets: HeartAssetBundle) -> None:
        
        super().__init__(graphics, pipeline)

        
        self.assets = assets

        self.mouse_x = float(graphics.frame_buffer_width) / 2.0
        self.mouse_y = float(graphics.frame_buffer_height) / 2.0

        self.cario_image = GraphicsSprite2DInstance()
        
        
    
    def wake(self) -> None:
        ...

    def load_prepare(self) -> None:
        pass

    def load(self) -> None:
        self.cario_image.load(self.graphics, self.assets.ekg_sprite_original)


    def load_complete(self) -> None:
        self.resize()

    def resize(self) -> None:
        graphics = self.graphics
    
    def update(self, dt: float) -> None:
        ...

        
    def draw(self) -> None:
        shape_program = self.pipeline.program_shape_2d
        sprite_program = self.pipeline.program_sprite_2d
        width = float(self.graphics.frame_buffer_width)
        height = float(self.graphics.frame_buffer_height)
        projection_matrix = GraphicsMatrix()
        projection_matrix.ortho_size(width=width, height=height)

        model_view_matrix = GraphicsMatrix()
        model_view_matrix.rotate_z(0.01)

        self.graphics.clear_rgb(0.04, 0.04, 0.08)
        self.graphics.blend_set_disabled()

        self.cario_image.projection_matrix = projection_matrix
        self.cario_image.model_view_matrix = model_view_matrix

        self.cario_image.render(sprite_program)


    # --------------------------------------------------------------
    # Input
    # --------------------------------------------------------------

    def mouse_down(self, button: int, xpos: float, ypos: float) -> None:
        ...
        value = random.randint(0, 4)
        if value == 0:
            self.assets.ekg_texture_original.write_pillow(self.assets.ekg_image_a)
        elif value == 1:
            self.assets.ekg_texture_original.write_pillow(self.assets.ekg_image_b)
        elif value == 2:
            self.assets.ekg_texture_original.write_pillow(self.assets.ekg_image_c)
        elif value == 3:
            self.assets.ekg_texture_original.write_pillow(self.assets.ekg_image_d)
        else:
            self.assets.ekg_texture_original.write_pillow(self.assets.ekg_image_e)
    
    def mouse_up(self, button: int, xpos: float, ypos: float) -> None:
        ...
        
    def mouse_move(self, xpos: float, ypos: float) -> None:
        ...
    
    def mouse_wheel(self, direction: int) -> None:
        print(f"HeartScene.mouse_wheel(direction={direction})")

    def key_down(
        self,
        key: int,
        mod_control: bool,
        mod_alt: bool,
        mod_shift: bool,
    ) -> None:
        print(
            f"HeartScene.key_down("
            f"key={key}, "
            f"mod_control={mod_control}, "
            f"mod_alt={mod_alt}, "
            f"mod_shift={mod_shift}"
            f")"
        )

    def key_up(
        self,
        key: int,
        mod_control: bool,
        mod_alt: bool,
        mod_shift: bool,
    ) -> None:
        ...

    # --------------------------------------------------------------
    # Cleanup
    # --------------------------------------------------------------

    def dispose(self) -> None:
        ...
    