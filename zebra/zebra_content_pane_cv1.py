# zebra/zebra_content_pane_cv1.py
from __future__ import annotations

from typing import Optional

from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QSlider, QCheckBox, QPushButton, QFrame
)

from tools.tool_menu_content_pane import ToolMenuContentPane


class ZebraContentPaneCV1(ToolMenuContentPane):
    # Signals you can hook from your app shell / scene.
    threshold_changed = Signal(int)
    knockout_changed = Signal(int)
    bw_changed = Signal(bool)

    previous_image_clicked = Signal()
    next_image_clicked = Signal()
    calibrate_clicked = Signal()
    reset_clicked = Signal()

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setObjectName("ZebraContentPaneCV1")

        root = QVBoxLayout()
        root.setContentsMargins(12, 10, 12, 12)
        root.setSpacing(10)

        # --- threshold slider ---
        self.threshold_label = QLabel("threshold: 128")
        self.threshold_label.setObjectName("ZebraLabel")

        self.threshold_slider = QSlider(Qt.Horizontal)
        self.threshold_slider.setRange(0, 255)
        self.threshold_slider.setValue(128)
        self.threshold_slider.valueChanged.connect(self._on_threshold)

        root.addWidget(self.threshold_label)
        root.addWidget(self.threshold_slider)

        # --- knockout slider ---
        self.knockout_label = QLabel("knockout: 0")
        self.knockout_label.setObjectName("ZebraLabel")

        self.knockout_slider = QSlider(Qt.Horizontal)
        self.knockout_slider.setRange(0, 100)
        self.knockout_slider.setValue(0)
        self.knockout_slider.valueChanged.connect(self._on_knockout)

        root.addWidget(self.knockout_label)
        root.addWidget(self.knockout_slider)

        # --- bw checkbox ---
        row_bw = QHBoxLayout()
        row_bw.setContentsMargins(0, 0, 0, 0)
        row_bw.setSpacing(8)

        self.bw_checkbox = QCheckBox("bw")
        self.bw_checkbox.stateChanged.connect(self._on_bw)

        row_bw.addWidget(self.bw_checkbox, 0)
        row_bw.addStretch(1)
        root.addLayout(row_bw)

        # --- separator ---
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setObjectName("ZebraSeparator")
        root.addWidget(sep)

        # --- buttons row 1: prev / next ---
        row_nav = QHBoxLayout()
        row_nav.setSpacing(8)

        self.prev_btn = QPushButton("previous image")
        self.next_btn = QPushButton("next image")
        self.prev_btn.clicked.connect(self.previous_image_clicked.emit)
        self.next_btn.clicked.connect(self.next_image_clicked.emit)

        row_nav.addWidget(self.prev_btn, 1)
        row_nav.addWidget(self.next_btn, 1)
        root.addLayout(row_nav)

        # --- buttons row 2: calibrate / reset ---
        row_ops = QHBoxLayout()
        row_ops.setSpacing(8)

        self.calibrate_btn = QPushButton("calibrate")
        self.reset_btn = QPushButton("reset")
        self.calibrate_btn.clicked.connect(self.calibrate_clicked.emit)
        self.reset_btn.clicked.connect(self._on_reset_clicked)

        row_ops.addWidget(self.calibrate_btn, 1)
        row_ops.addWidget(self.reset_btn, 1)
        root.addLayout(row_ops)

        self.setLayout(root)

        # Local styling for content area
        self.setStyleSheet("""
        QWidget#ZebraContentPaneCV1 {
            background: transparent;
        }
        QLabel#ZebraLabel {
            color: rgba(255,255,255,210);
        }
        QCheckBox {
            color: rgba(255,255,255,210);
        }
        QFrame#ZebraSeparator {
            color: rgba(255,255,255,40);
            background: rgba(255,255,255,40);
            max-height: 1px;
        }
        QPushButton {
            color: rgba(255,255,255,210);
            background: rgba(255,255,255,18);
            border: 1px solid rgba(255,255,255,28);
            border-radius: 8px;
            padding: 6px 10px;
        }
        QPushButton:hover {
            background: rgba(255,255,255,28);
        }
        """)

    # --- events ---
    def _on_threshold(self, v: int) -> None:
        self.threshold_label.setText(f"threshold: {v}")
        self.threshold_changed.emit(v)

    def _on_knockout(self, v: int) -> None:
        self.knockout_label.setText(f"knockout: {v}")
        self.knockout_changed.emit(v)

    def _on_bw(self, state: int) -> None:
        self.bw_changed.emit(state == Qt.Checked)

    def _on_reset_clicked(self) -> None:
        self.threshold_slider.setValue(128)
        self.knockout_slider.setValue(0)
        self.bw_checkbox.setChecked(False)
        self.reset_clicked.emit()

    # --- convenience getters ---
    def get_threshold(self) -> int:
        return int(self.threshold_slider.value())

    def get_knockout(self) -> int:
        return int(self.knockout_slider.value())

    def get_bw(self) -> bool:
        return bool(self.bw_checkbox.isChecked())
