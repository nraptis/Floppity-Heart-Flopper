# zebra/zebra_menu_top_bar.py
from __future__ import annotations

from typing import Optional
from PySide6.QtWidgets import QWidget

from tools.tool_menu_top_bar import ToolMenuTopBar


class ZebraMenuTopBar(ToolMenuTopBar):
    def __init__(self, title: str = "Zebra CV1", parent: Optional[QWidget] = None) -> None:
        super().__init__(title=title, parent=parent)
        self.setObjectName("ZebraMenuTopBar")
