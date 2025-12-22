# label_scene_constants.py

from graphics.graphics_color import GraphicsColor

class LabelSceneConstants:
    # Vertical center divider (Paint ↔ Overview)
    center_bar_width_fill: float = 4.0
    center_bar_width_stroke: float = 6.0
    center_bar_width_grab: float = 18.0

    # Horizontal divider (UI ↔ bottom widgets)
    top_bar_height_fill: float = 4.0
    top_bar_height_stroke: float = 6.0
    top_bar_height_grab: float = 18.0

    # Fill colors
    bar_fill_color_unselected = GraphicsColor(0.94, 0.94, 0.98)

    # Yellow highlight you liked:
    bar_fill_color_selected = GraphicsColor(1.00, 0.95, 0.60)

    # Stroke color (never changes)
    bar_stroke_color = GraphicsColor(0.68, 0.68, 0.72)
