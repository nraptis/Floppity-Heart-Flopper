# tools/tool_menu.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple

from PySide6.QtCore import Qt, QPoint
from PySide6.QtWidgets import QWidget, QVBoxLayout

from tools.tool_menu_top_bar import ToolMenuTopBar
from tools.tool_menu_content_pane import ToolMenuContentPane

from PySide6.QtGui import QPainter, QPainterPath, QColor, QPen
from PySide6.QtCore import QRectF

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

        self._collapsed: bool = False
        self._expanded_size = self.size()  # remembered once we show

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

        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_StyledBackground, True)

        #self.setAttribute(Qt.WA_TranslucentBackground, False)
        #self.setStyleSheet("background-color: white;")

        root = QVBoxLayout()
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)
        root.addWidget(self.top_bar, 0)
        root.addWidget(self.content_pane, 1)
        self.setLayout(root)

        self.resize(640, 480)
        self.resize(*initial_size)

        self.setStyleSheet("""
        QWidget#ToolMenu {
            background: transparent;
            border: 1px solid rgba(255,255,255,40);
            border-radius: 10px;
        }

        QWidget#ToolMenuTopBar,
        QWidget#ZebraMenuTopBar {
            background-color: #0A0F1B;             /* slightly darker */
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
            border-bottom: 1px solid rgba(255,255,255,30);
        }

        QLabel#ToolMenuTopBarTitle {
            color: rgba(235,245,255,230);
            font-weight: 600;
        }

        QPushButton#ToolMenuTopBarClose {
            color: rgba(235,245,255,220);
            background: rgba(255,255,255,18);
            border: 1px solid rgba(255,255,255,28);
            border-radius: 6px;
        }
        QPushButton#ToolMenuTopBarClose:hover {
            background: rgba(255,255,255,30);
        }
        QSlider::groove:horizontal {
            height: 6px;
            background: rgba(255,255,255,30);
            border-radius: 3px;
        }
        QSlider::sub-page:horizontal {
            background: rgba(40,140,255,180);
            border-radius: 3px;
        }
        QSlider::add-page:horizontal {
            background: rgba(255,255,255,18);
            border-radius: 3px;
        }
        QSlider::handle:horizontal {
            width: 16px;
            height: 16px;
            margin: -6px 0;               /* centers handle over groove */
            border-radius: 8px;
            background-color: #EAF2FF;     /* solid */
            border: 1px solid rgba(0,0,0,70);
        }

        QSlider::handle:horizontal:hover {
            background-color: #FFFFFF;
        }
                           
        QWidget#ZebraSegmented {
            background: rgba(255,255,255,10);
            border: 1px solid rgba(255,255,255,22);
            border-radius: 8px;
        }

        QPushButton#ZebraSegmentButton {
            padding: 4px 10px;
            border: none;
            color: rgba(235,245,255,200);
            background: transparent;
        }

        QPushButton#ZebraSegmentButton:checked {
            background: rgba(40,140,255,180);
            color: rgba(255,255,255,240);
        }

        QWidget#ZebraSegmented QPushButton:first-child {
            border-top-left-radius: 8px;
            border-bottom-left-radius: 8px;
        }

        QWidget#ZebraSegmented QPushButton:last-child {
            border-top-right-radius: 8px;
            border-bottom-right-radius: 8px;
        }
                           
        QPushButton#ToolMenuTopBarMinimize {
            color: rgba(235,245,255,220);
            background: rgba(255,255,255,18);
            border: 1px solid rgba(255,255,255,28);
            border-radius: 6px;
            font-weight: 700;
        }
        
        QPushButton#ToolMenuTopBarMinimize:hover {
            background: rgba(255,255,255,30);
        }
        
        QPushButton#ToolMenuTopBarMinimize {
            font-size: 14px;
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

    def paintEvent(self, event) -> None:
        radius = 12.0

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

        rect = QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5)

        path = QPainterPath()
        path.addRoundedRect(rect, radius, radius)

        # Background
        painter.fillPath(path, QColor("#0B1220"))

        # Border
        pen = QPen(QColor(255, 255, 255, 40))
        pen.setWidthF(1.0)
        painter.setPen(pen)
        painter.drawPath(path)

        painter.end()
        super().paintEvent(event)

    def is_collapsed(self) -> bool:
        return self._collapsed

    def toggle_collapsed(self) -> None:
        self.set_collapsed(not self._collapsed)

    def set_collapsed(self, collapsed: bool) -> None:
        if self._collapsed == collapsed:
            return
        self._collapsed = collapsed

        if collapsed:
            # remember expanded size before shrinking
            self._expanded_size = self.size()

            # hide content, keep top bar
            self.content_pane.setVisible(False)

            # shrink to just top bar (+ a tiny padding)
            h = self.top_bar.height()
            self.setMinimumHeight(h)
            self.setMaximumHeight(h)
            self.resize(self.width(), h)
        else:
            # restore content
            self.content_pane.setVisible(True)

            # restore sizing constraints
            self.setMinimumHeight(0)
            self.setMaximumHeight(16777215)  # Qt's "no limit"

            # restore previous expanded size
            if self._expanded_size is not None:
                self.resize(self._expanded_size)
