from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QWidget, QToolButton, QVBoxLayout


class CollapsibleWidget(QWidget):
    def __init__(self, title: str = ""):
        super(CollapsibleWidget, self).__init__()

        layout_main = QVBoxLayout(self)
        layout_main.setContentsMargins(0, 0, 0, 0)
        layout_main.setSpacing(0)

        self.btn_toggle = QToolButton(self)
        self.btn_toggle.setText(title)
        self.btn_toggle.setCheckable(True)
        self.btn_toggle.setChecked(False)
        # btn_toggle.setLayoutDirection(Qt.RightToLeft)
        self.btn_toggle.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.btn_toggle.setArrowType(Qt.RightArrow)
        self.btn_toggle.setIconSize(QSize(8, 8))
        self.btn_toggle.setStyleSheet("QToolButton {border: none; font-weight: bold;}"
                                      "QToolButton:hover{color:rgba(0,0,0,0.7)}")
        self.btn_toggle.pressed.connect(self.on_pressed)

        self.content = QWidget()
        self.content.setStyleSheet("color: rgba(0,0,0,0.7)")
        self.content.hide()
        self.layout_content = QVBoxLayout(self.content)
        self.layout_content.setContentsMargins(13, 0, 13, 0)
        self.layout_content.setSpacing(0)

        layout_main.addWidget(self.btn_toggle)
        layout_main.addWidget(self.content)

    def on_pressed(self):
        checked = self.btn_toggle.isChecked()
        self.btn_toggle.setArrowType(Qt.RightArrow if checked else Qt.DownArrow)
        self.content.setVisible(False if checked else True)

    def collapse(self):
        self.btn_toggle.setChecked(True)
        self.on_pressed()

    def expand(self):
        self.btn_toggle.setChecked(False)
        self.on_pressed()

    def addElement(self, widget: QWidget):
        self.layout_content.addWidget(widget)
