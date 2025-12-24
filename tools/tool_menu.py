# tools/tool_menu.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple

from PySide6.QtCore import Qt, QPoint
from PySide6.QtWidgets import QWidget, QVBoxLayout

from tools.tool_menu_top_bar import ToolMenuTopBar
from tools.tool_menu_content_pane import ToolMenuContentPane


@dataclass
class ToolMenuOverlayConfig:
    """
    Config for positioning this tool menu over a GLFW window.
    All coordinates are in screen pixels (same space as glfw.get_window_pos).
    """
    follow_glfw_window: bool = True
    x_offset: int = 20
    y_offset: int = 60


class ToolMenu(QWidget):
    
    def __init__(
        self,
        top_bar: ToolMenuTopBar,
        content_pane: ToolMenuContentPane,
        is_draggable: bool = True,
        initial_size: Tuple[int, int] = (360, 220),
        overlay_config: Optional[ToolMenuOverlayConfig] = None,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)

        self.is_draggable = is_draggable
        self.overlay_config = overlay_config or ToolMenuOverlayConfig()

        # Drag state
        self._dragging = False
        self._drag_anchor_global: Optional[QPoint] = None
        self._drag_anchor_window_pos: Optional[QPoint] = None

        self.top_bar = top_bar
        self.content_pane = content_pane
        self.content_pane.on_attach(self)

        self.setObjectName("ToolMenu")

        # Window flags: frameless, tool-like, always on top
        self.setWindowFlags(
            Qt.Tool |
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        self.setStyleSheet("background-color: white;")

        root = QVBoxLayout()
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)
        root.addWidget(self.top_bar, 0)
        root.addWidget(self.content_pane, 1)
        self.setLayout(root)

        self.resize(640, 480)

        # Basic styling (feel free to replace with your own QSS file)
        self.setStyleSheet("""
        QWidget#ToolMenu {
            background: rgba(20, 20, 24, 210);
            border: 1px solid rgba(255,255,255,40);
            border-radius: 10px;
        }
        QWidget#ToolMenuTopBar {
            background: rgba(35, 35, 40, 220);
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
        }
        QLabel#ToolMenuTopBarTitle {
            color: rgba(255,255,255,220);
            font-weight: 600;
        }
        QPushButton#ToolMenuTopBarClose {
            color: rgba(255,255,255,200);
            background: rgba(255,255,255,20);
            border: 1px solid rgba(255,255,255,30);
            border-radius: 6px;
        }
        QPushButton#ToolMenuTopBarClose:hover {
            background: rgba(255,255,255,35);
        }
        """)

    # ---- Drag API (called by ToolMenuTopBar) ----

    def _drag_begin(self, press_pos_global: QPoint) -> None:
        self._dragging = True
        self._drag_anchor_global = press_pos_global
        self._drag_anchor_window_pos = self.pos()

    def _drag_move(self, pos_global: QPoint) -> None:
        if not self._dragging or self._drag_anchor_global is None or self._drag_anchor_window_pos is None:
            return
        delta = pos_global - self._drag_anchor_global
        self.move(self._drag_anchor_window_pos + delta)

    def _drag_end(self) -> None:
        self._dragging = False
        self._drag_anchor_global = None
        self._drag_anchor_window_pos = None
