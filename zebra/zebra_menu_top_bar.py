# zebra/zebra_menu_top_bar.py
from __future__ import annotations

from typing import Optional
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal
from PySide6.QtCore import Qt, QPoint
from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QButtonGroup

from tools.tool_menu_top_bar import ToolMenuTopBar


class ZebraMenuTopBar(ToolMenuTopBar):

    mode_changed = Signal(str)  # "Off" | "Mid1" | "Mid2" | "Full"

    def __init__(self, title: str = "Zebra CV1", parent: Optional[QWidget] = None) -> None:
        super().__init__(title=title, parent=parent)
        self.setObjectName("ZebraMenuTopBar")

        seg = QWidget(self)
        seg.setObjectName("ZebraSegmented")

        seg_layout = QHBoxLayout(seg)
        seg_layout.setContentsMargins(0, 0, 0, 0)
        seg_layout.setSpacing(0)

        self._seg_group = QButtonGroup(self)
        self._seg_group.setExclusive(True)

        labels = ["Off", "Mid1", "Mid2", "Full"]
        self._seg_buttons: list[QPushButton] = []

        for i, text in enumerate(labels):
            b = QPushButton(text)
            b.setCheckable(True)
            b.setObjectName("ZebraSegmentButton")
            seg_layout.addWidget(b)

            self._seg_group.addButton(b, i)
            self._seg_buttons.append(b)

        self._seg_buttons[0].setChecked(True)  # default Off

        self._seg_group.idClicked.connect(self._on_seg_clicked)

        # Insert segmented control into the existing top-bar layout:
        # layout = [title_label, close_btn]
        lay = self.layout()
        lay.insertWidget(2, seg, 0)  # now: [min, title, seg, close]
        lay.setStretch(0, 0)         # min fixed
        lay.setStretch(1, 1)         # title expands
        lay.setStretch(2, 0)         # segmented fixed
        lay.setStretch(3, 0)         # close fixed

    def _on_seg_clicked(self, idx: int) -> None:
        text = ["Off", "Mid1", "Mid2", "Full"][idx]
        self.mode_changed.emit(text)
