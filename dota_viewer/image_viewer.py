from PyQt5.QtWidgets import (
    QApplication,
    QGraphicsView,
)
from PyQt5.QtGui import QWheelEvent
from PyQt5.QtCore import Qt


class ImageViewer(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.setDragMode(QGraphicsView.ScrollHandDrag)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setInteractive(True)

        self.current_scale = 1.0

    def wheelEvent(self, event: QWheelEvent):
        modifiers = QApplication.keyboardModifiers()

        if modifiers == Qt.ControlModifier:
            zoom_in = event.angleDelta().y() > 0
            if zoom_in:
                self.scale(1.1, 1.1)
                self.current_scale = self.transform().m11()
            else:
                self.scale(0.9, 0.9)
                self.current_scale = self.transform().m11()
        else:
            super().wheelEvent(event)
