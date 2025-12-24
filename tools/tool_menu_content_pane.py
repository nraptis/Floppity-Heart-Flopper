# tools/tool_menu_content_pane.py
from __future__ import annotations

from typing import Optional

from PySide6.QtWidgets import QWidget


class ToolMenuContentPane(QWidget):
    """
    Base class for content panes. Override to add controls.

    The menu will call `on_attach(menu)` after construction.
    """

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._menu = None

    def on_attach(self, menu) -> None:
        self._menu = menu

    @property
    def menu(self):
        return self._menu
