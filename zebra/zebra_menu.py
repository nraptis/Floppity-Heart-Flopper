# zebra/zebra_menu.py
from __future__ import annotations

from typing import Optional

from tools.tool_menu import ToolMenu, ToolMenuOverlayConfig
from zebra.zebra_menu_top_bar import ZebraMenuTopBar
from zebra.zebra_content_pane_cv1 import ZebraContentPaneCV1


class ZebraMenu(ToolMenu):
    def __init__(
        self,
        is_draggable: bool = True,
        parent=None,
    ) -> None:
        top_bar = ZebraMenuTopBar(title="Zebra CV1")
        content = ZebraContentPaneCV1()

        overlay = ToolMenuOverlayConfig(
            follow_glfw_window=True,
            x_offset=20,
            y_offset=60,
        )

        super().__init__(
            top_bar=top_bar,
            content_pane=content,
            is_draggable=is_draggable,
            initial_size=(380, 260),
            overlay_config=overlay,
            parent=parent,
        )

    @property
    def zebra(self) -> ZebraContentPaneCV1:
        return self.content_pane  # type: ignore
