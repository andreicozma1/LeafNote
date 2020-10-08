from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QWidget, QToolButton, QVBoxLayout, QFrame


class CollapsibleWidget(QWidget):
    def __init__(self, title: str = ""):
        super(CollapsibleWidget, self).__init__()

        layout_vertical = QVBoxLayout(self)
        layout_vertical.setContentsMargins(0, 0, 0, 0)
        layout_vertical.setSpacing(0)

        btn_toggle = QToolButton(self)
        btn_toggle.setText(title)
        btn_toggle.setCheckable(True)
        btn_toggle.setChecked(False)
        # btn_toggle.setLayoutDirection(Qt.RightToLeft)
        btn_toggle.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        btn_toggle.setArrowType(Qt.RightArrow)
        btn_toggle.setIconSize(QSize(8, 8))
        btn_toggle.setStyleSheet("QToolButton {border: none; font-size: 12px;}"
                                 "QToolButton:hover{color:rgba(255,255,255,0.5)}")

        area_content = QFrame()

        layout_vertical.addWidget(btn_toggle)
        layout_vertical.addWidget(area_content)
