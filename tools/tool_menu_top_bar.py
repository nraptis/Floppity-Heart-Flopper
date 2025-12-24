# tools/tool_menu_top_bar.py
from __future__ import annotations

from typing import Optional

from PySide6.QtCore import Qt, QPoint, Signal
from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QPushButton


class ToolMenuTopBar(QWidget):
    """
    Simple top bar that can initiate a drag on its parent ToolMenu.

    When the parent menu is_draggable=True:
      - dragging is ONLY allowed when you click+drag on this top bar.
    """

    DEFAULT_HEIGHT = 54

    collapsed_changed = Signal(bool)  # emitted when user toggles collapse

    def __init__(self, title: str = "Tool", parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setFixedHeight(self.DEFAULT_HEIGHT)
        self.setObjectName("ToolMenuTopBar")

        self._pressing = False
        self._press_pos_global: Optional[QPoint] = None

        self.title_label = QLabel(title)
        self.title_label.setObjectName("ToolMenuTopBarTitle")
        self.title_label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        self.close_btn = QPushButton("✕")
        self.close_btn.setFixedSize(28, 24)
        self.close_btn.setObjectName("ToolMenuTopBarClose")
        self.close_btn.clicked.connect(self._on_close_clicked)


        self.min_btn = QPushButton("−")  # starts expanded
        self.min_btn.setFixedSize(28, 24)
        self.min_btn.setObjectName("ToolMenuTopBarMinimize")
        self.min_btn.clicked.connect(self._on_min_clicked)

        layout = QHBoxLayout()
        layout.setContentsMargins(10, 0, 6, 0)
        layout.setSpacing(6)
        layout.addWidget(self.min_btn, 0, Qt.AlignLeft)
        layout.addWidget(self.title_label, 1)
        layout.addWidget(self.close_btn, 0, Qt.AlignRight)
        self.setLayout(layout)

        # Style is mostly on the ToolMenu (parent) via QSS, but safe defaults here.
        self.setMouseTracking(True)

        self.setStyleSheet("""
        QWidget#ToolMenu {
            background: #0B1220;                 /* deep blue onyx */
            border: 1px solid rgba(255,255,255,40);
            border-radius: 10px;
        }
        QWidget#ToolMenuTopBar,
        QWidget#ZebraMenuTopBar {
            background: #0A0F1B;                 /* slightly darker */
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
        """)

    def set_title(self, title: str) -> None:
        self.title_label.setText(title)

    def _on_close_clicked(self) -> None:
        # Hide by default. You can override in subclasses.
        # w = self.window()
        # w.hide()
        print("close was clicked... lol")

    # Drag handling
    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.LeftButton:
            self._pressing = True
            self._press_pos_global = event.globalPosition().toPoint()

            menu = self._find_menu()
            if menu is not None and getattr(menu, "is_draggable", False):
                menu._drag_begin(self._press_pos_global)

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:
        if self._pressing:
            menu = self._find_menu()
            if menu is not None and getattr(menu, "is_draggable", False):
                menu._drag_move(event.globalPosition().toPoint())
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        if event.button() == Qt.LeftButton:
            self._pressing = False
            menu = self._find_menu()
            if menu is not None and getattr(menu, "is_draggable", False):
                menu._drag_end()
        super().mouseReleaseEvent(event)

    def _find_menu(self):
        # The ToolMenu is typically the window() of this widget.
        w = self.window()
        return w
    
    def _on_min_clicked(self) -> None:
        menu = self._find_menu()
        if menu is None:
            return

        # ToolMenu API
        if hasattr(menu, "toggle_collapsed"):
            menu.toggle_collapsed()
            collapsed = bool(getattr(menu, "is_collapsed", lambda: False)())
            self.set_collapsed_visual(collapsed)
            self.collapsed_changed.emit(collapsed)

    def set_collapsed_visual(self, collapsed: bool) -> None:
        # square when minimized, minus when expanded
        self.min_btn.setText("▢" if collapsed else "−")

