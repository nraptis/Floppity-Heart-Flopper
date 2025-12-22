# labeling_scene.py
from __future__ import annotations
from typing import Optional

from OpenGL import GL as gl
from graphics.graphics_scene import GraphicsScene
from asset_bundle import AssetBundle
from graphics.graphics_library import GraphicsLibrary
from graphics.graphics_pipeline import GraphicsPipeline
from graphics.graphics_matrix import GraphicsMatrix
from graphics.graphics_color import GraphicsColor
from graphics.graphics_shape_2d_instance import GraphicsShape2DInstance
from label_scene_constants import LabelSceneConstants
from label_scene_mouse_mode import LabelSceneMouseMode
from paint_widget import PaintWidget

class LabelingScene(GraphicsScene):
    def __init__(self, graphics: GraphicsLibrary, pipeline: GraphicsPipeline, assets: AssetBundle) -> None:
        super().__init__(graphics, pipeline)
        self.assets = assets

        # Shape instances for the split bars (fill)
        self.top_bar_shape_instance: Optional[GraphicsShape2DInstance] = None
        self.center_bar_shape_instance: Optional[GraphicsShape2DInstance] = None

        # Stroke shapes (behind the fill)
        self.top_bar_stroke_shape_instance: Optional[GraphicsShape2DInstance] = None
        self.center_bar_stroke_shape_instance: Optional[GraphicsShape2DInstance] = None

        # Midpoints (in framebuffer coordinates)
        self.center_bar_x: int = 0
        self.top_bar_y: int = 0

        # Drag state
        self.mouse_mode: LabelSceneMouseMode = LabelSceneMouseMode.NONE
        self.bar_drag_start_bar_x: float = 0.0
        self.bar_drag_start_mouse_x: float = 0.0
        self.bar_drag_start_bar_y: float = 0.0
        self.bar_drag_start_mouse_y: float = 0.0

        # Previous framebuffer size (for proportional resize)
        self.previous_frame_buffer_width: float = float(self.graphics.frame_buffer_width)
        self.previous_frame_buffer_height: float = float(self.graphics.frame_buffer_height)

        self.paint_widget = PaintWidget(graphics, pipeline)

    # --------------------------------------------------------------
    # Lifecycle
    # --------------------------------------------------------------

    def wake(self) -> None:
        pass

    def load_prepare(self) -> None:
        pass

    def load(self) -> None:
        """
        Load textures / buffers / assets as needed.
        (Currently empty – bars are pure shapes, built in load_complete.)
        """
        self.paint_widget.load(self.assets)

    def load_complete(self) -> None:
        """
        Build the bar instances and position them using
        the current framebuffer size and LabelSceneConstants.
        """
        width = float(self.graphics.frame_buffer_width)
        height = float(self.graphics.frame_buffer_height)

        # Midpoints – tweak top_bar_y fraction later as desired.
        self.center_bar_x = int(width / 2.0)
        self.top_bar_y = int(height * 0.25)  # placeholder: 25% down from top

        # ---- Top bar stroke (horizontal) --------------------------
        self.top_bar_stroke_shape_instance = GraphicsShape2DInstance()
        self.top_bar_stroke_shape_instance.load(self.graphics)

        # ---- Top bar fill (horizontal) ----------------------------
        self.top_bar_shape_instance = GraphicsShape2DInstance()
        self.top_bar_shape_instance.load(self.graphics)

        # ---- Center bar stroke (vertical) -------------------------
        self.center_bar_stroke_shape_instance = GraphicsShape2DInstance()
        self.center_bar_stroke_shape_instance.load(self.graphics)

        # ---- Center bar fill (vertical) ---------------------------
        self.center_bar_shape_instance = GraphicsShape2DInstance()
        self.center_bar_shape_instance.load(self.graphics)

        # Initial geometry + colors
        self._update_top_bar_shape()
        self._update_center_bar_shape()
        self._update_top_bar_color()
        self._update_center_bar_color()

        # Record framebuffer size
        self.previous_frame_buffer_width = width
        self.previous_frame_buffer_height = height

        self.paint_widget.set_frame(100, 100, 100, 100)

    def resize(self) -> None:
        """
        Adjust bar positions when the framebuffer size changes.
        The center bar keeps the same relative X fraction.
        """
        width = float(self.graphics.frame_buffer_width)
        height = float(self.graphics.frame_buffer_height)

        # Preserve center_bar_x as a fraction of old width
        if self.previous_frame_buffer_width > 0.0:
            fraction_x = float(self.center_bar_x) / self.previous_frame_buffer_width
            self.center_bar_x = int(fraction_x * width)

        # Optionally you could also preserve top_bar_y as a fraction of height.
        # For now, leave it as-is unless you decide otherwise.

        # Rebuild geometry
        self._update_top_bar_shape()
        self._update_center_bar_shape()

        # Update previous size
        self.previous_frame_buffer_width = width
        self.previous_frame_buffer_height = height

    def update(self, dt: float) -> None:
        """
        Main per-frame update.
        """
        pass

    # --------------------------------------------------------------
    # Helpers to update bar geometry from midpoints
    # --------------------------------------------------------------

    def _update_top_bar_shape(self) -> None:
        if self.top_bar_shape_instance is None and self.top_bar_stroke_shape_instance is None:
            return

        width = float(self.graphics.frame_buffer_width)

        # Stroke rect
        stroke_height = float(LabelSceneConstants.top_bar_height_stroke)
        stroke_y = float(self.top_bar_y) - stroke_height * 0.5

        if self.top_bar_stroke_shape_instance is not None:
            self.top_bar_stroke_shape_instance.set_position_frame(
                x=0.0,
                y=stroke_y,
                width=width,
                height=stroke_height,
            )

        # Fill rect
        fill_height = float(LabelSceneConstants.top_bar_height_fill)
        fill_y = float(self.top_bar_y) - fill_height * 0.5

        if self.top_bar_shape_instance is not None:
            self.top_bar_shape_instance.set_position_frame(
                x=0.0,
                y=fill_y,
                width=width,
                height=fill_height,
            )

    def _update_center_bar_shape(self) -> None:
        if self.center_bar_shape_instance is None and self.center_bar_stroke_shape_instance is None:
            return

        width = float(self.graphics.frame_buffer_width)
        height = float(self.graphics.frame_buffer_height)

        # Stroke rect
        stroke_width = float(LabelSceneConstants.center_bar_width_stroke)
        stroke_x = float(self.center_bar_x) - stroke_width * 0.5
        stroke_height = height - float(self.top_bar_y)

        if self.center_bar_stroke_shape_instance is not None:
            self.center_bar_stroke_shape_instance.set_position_frame(
                x=stroke_x,
                y=float(self.top_bar_y),
                width=stroke_width,
                height=stroke_height,
            )

        # Fill rect
        fill_width = float(LabelSceneConstants.center_bar_width_fill)
        fill_x = float(self.center_bar_x) - fill_width * 0.5
        fill_height = stroke_height

        if self.center_bar_shape_instance is not None:
            self.center_bar_shape_instance.set_position_frame(
                x=fill_x,
                y=float(self.top_bar_y),
                width=fill_width,
                height=fill_height,
            )

    # --------------------------------------------------------------
    # Color helpers
    # --------------------------------------------------------------

    def _update_top_bar_color(self) -> None:
        """
        Stroke never changes. Fill changes when selected.
        """
        stroke_color = LabelSceneConstants.bar_stroke_color

        if self.mouse_mode == LabelSceneMouseMode.DRAGGING_TOP_BAR:
            fill_color = LabelSceneConstants.bar_fill_color_selected
        else:
            fill_color = LabelSceneConstants.bar_fill_color_unselected

        if self.top_bar_stroke_shape_instance is not None:
            self.top_bar_stroke_shape_instance.color = stroke_color
        if self.top_bar_shape_instance is not None:
            self.top_bar_shape_instance.color = fill_color


    def _update_center_bar_color(self) -> None:
        """
        Stroke never changes. Fill changes when selected.
        """
        stroke_color = LabelSceneConstants.bar_stroke_color

        if self.mouse_mode == LabelSceneMouseMode.DRAGGING_CENTER_BAR:
            fill_color = LabelSceneConstants.bar_fill_color_selected
        else:
            fill_color = LabelSceneConstants.bar_fill_color_unselected

        if self.center_bar_stroke_shape_instance is not None:
            self.center_bar_stroke_shape_instance.color = stroke_color
        if self.center_bar_shape_instance is not None:
            self.center_bar_shape_instance.color = fill_color

    # --------------------------------------------------------------
    # Draw
    # --------------------------------------------------------------

    def draw(self) -> None:
        """
        Draw the divider bars using a simple 2D ortho projection.
        Stroke shapes are rendered first, then fills.
        """
        graphics = self.graphics
        pipeline = self.pipeline
        shape_program = pipeline.program_shape_2d

        width = float(graphics.frame_buffer_width)
        height = float(graphics.frame_buffer_height)

        # Ortho projection matching the framebuffer
        projection_matrix = GraphicsMatrix()
        projection_matrix.ortho_size(width=width, height=height)

        # Clear background
        graphics.clear_rgb(0.14, 0.14, 0.18)

        # Basic alpha blending
        graphics.blend_set_alpha()

        # Render helper
        def draw_instance(instance: Optional[GraphicsShape2DInstance]) -> None:
            if instance is None:
                return
            instance.projection_matrix = projection_matrix.copy()
            # Identity model-view (no extra transform)
            instance.model_view_matrix = GraphicsMatrix()
            instance.render(shape_program)

        # Stroke first
        draw_instance(self.top_bar_stroke_shape_instance)
        draw_instance(self.center_bar_stroke_shape_instance)

        # Then fill
        draw_instance(self.top_bar_shape_instance)
        draw_instance(self.center_bar_shape_instance)

        self.paint_widget.draw()

    # --------------------------------------------------------------
    # Cleanup
    # --------------------------------------------------------------

    def dispose(self) -> None:
        """
        Clean up GPU resources for the bar instances.
        Safe to call multiple times.
        """
        if self.top_bar_shape_instance is not None:
            self.top_bar_shape_instance.dispose()
            self.top_bar_shape_instance = None

        if self.center_bar_shape_instance is not None:
            self.center_bar_shape_instance.dispose()
            self.center_bar_shape_instance = None

        if self.top_bar_stroke_shape_instance is not None:
            self.top_bar_stroke_shape_instance.dispose()
            self.top_bar_stroke_shape_instance = None

        if self.center_bar_stroke_shape_instance is not None:
            self.center_bar_stroke_shape_instance.dispose()
            self.center_bar_stroke_shape_instance = None

    # --------------------------------------------------------------
    # Drag helpers
    # --------------------------------------------------------------

    def mouse_capture_drag_start_top_bar(self, xpos: float, ypos: float) -> None:
        self.bar_drag_start_bar_y = float(self.top_bar_y)
        self.bar_drag_start_mouse_y = float(ypos)
        self.mouse_mode = LabelSceneMouseMode.DRAGGING_TOP_BAR
        self._update_top_bar_color()
        self._update_center_bar_color()

    def mouse_capture_drag_start_center_bar(self, xpos: float, ypos: float) -> None:
        self.bar_drag_start_bar_x = float(self.center_bar_x)
        self.bar_drag_start_mouse_x = float(xpos)
        self.mouse_mode = LabelSceneMouseMode.DRAGGING_CENTER_BAR
        self._update_top_bar_color()
        self._update_center_bar_color()

    # --------------------------------------------------------------
    # Input
    # --------------------------------------------------------------

    def mouse_down(self, button: int, xpos: float, ypos: float) -> None:
        # Default state
        self.mouse_mode = LabelSceneMouseMode.NONE

        distance_to_top_bar = abs(float(self.top_bar_y) - ypos)
        distance_to_center_bar = abs(float(self.center_bar_x) - xpos)

        top_grab_half = float(LabelSceneConstants.top_bar_height_grab) * 0.5
        center_grab_half = float(LabelSceneConstants.center_bar_width_grab) * 0.5

        if distance_to_top_bar < top_grab_half:
            if distance_to_center_bar < center_grab_half:
                # Near both – grab whichever is closer
                if distance_to_center_bar < distance_to_top_bar:
                    self.mouse_capture_drag_start_center_bar(xpos, ypos)
                    return
                else:
                    self.mouse_capture_drag_start_top_bar(xpos, ypos)
                    return
            else:
                self.mouse_capture_drag_start_top_bar(xpos, ypos)
                return
        elif distance_to_center_bar < center_grab_half:
            self.mouse_capture_drag_start_center_bar(xpos, ypos)
            return

        # If we didn't grab anything, make sure colors are idle
        self.mouse_mode = LabelSceneMouseMode.NONE
        self._update_top_bar_color()
        self._update_center_bar_color()

    def mouse_up(self, button: int, xpos: float, ypos: float) -> None:
        # Drop back to NONE on any mouse up and reset colors.
        self.mouse_mode = LabelSceneMouseMode.NONE
        self._update_top_bar_color()
        self._update_center_bar_color()

    def mouse_move(self, xpos: float, ypos: float) -> None:
        width = float(self.graphics.frame_buffer_width)
        height = float(self.graphics.frame_buffer_height)

        if self.mouse_mode == LabelSceneMouseMode.DRAGGING_CENTER_BAR:
            dx = xpos - self.bar_drag_start_mouse_x
            new_x = self.bar_drag_start_bar_x + dx

            # Clamp within the window, leaving some margin based on grab width
            margin = float(LabelSceneConstants.center_bar_width_grab) * 0.5
            min_x = margin
            max_x = width - margin
            if new_x < min_x:
                new_x = min_x
            if new_x > max_x:
                new_x = max_x

            self.center_bar_x = int(new_x)
            self._update_center_bar_shape()

        elif self.mouse_mode == LabelSceneMouseMode.DRAGGING_TOP_BAR:
            dy = ypos - self.bar_drag_start_mouse_y
            new_y = self.bar_drag_start_bar_y + dy

            # Clamp within the window, leaving some margin based on grab height
            margin = float(LabelSceneConstants.top_bar_height_grab) * 0.5
            min_y = margin
            max_y = height - margin
            if new_y < min_y:
                new_y = min_y
            if new_y > max_y:
                new_y = max_y

            self.top_bar_y = int(new_y)
            self._update_top_bar_shape()
            self._update_center_bar_shape()

    def mouse_wheel(self, direction: int) -> None:
        pass

    def key_down(
        self,
        key: int,
        mod_control: bool,
        mod_alt: bool,
        mod_shift: bool,
    ) -> None:
        pass

    def key_up(
        self,
        key: int,
        mod_control: bool,
        mod_alt: bool,
        mod_shift: bool,
    ) -> None:
        pass
