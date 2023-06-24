import argparse
import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QSlider, QFrame, QGroupBox, QGridLayout, QGraphicsView
from PyQt5.QtGui import QPixmap, QWheelEvent
from PyQt5.QtCore import Qt



class ImageViewer(QMainWindow):
    def __init__(self, images_path):
        super().__init__()
        self.images_path = images_path
        self.setWindowTitle("Test window")

        window_width = 800
        window_height = 800
        self.setGeometry(100, 100, window_width, window_height)

        image_widget = QWidget()
        self.setCentralWidget(image_widget)

        self.create_top_buttons_group()
        self.create_image_label(window_width, window_height)


        main_layout = QGridLayout()
        main_layout.addWidget(self.top_buttons_group)
        main_layout.addWidget(self.image_label)
        image_widget.setLayout(main_layout)


    def wheelEvent(self, event: QWheelEvent):
        print('wheelEvent')

    def create_image_label(self, window_width, window_height):
        self.image_label = QLabel()

        self.image_label.setAlignment(Qt.AlignCenter)

        self.pixmap = QPixmap(self.images_path)
        pixmap_width = self.pixmap.width()
        pixmap_height = self.pixmap.height()

        if window_width>pixmap_width or window_height>pixmap_height:
            scaled_pixmap = self.pixmap.scaled(pixmap_width, pixmap_height, Qt.KeepAspectRatio)
        else:
            scaled_pixmap = self.pixmap.scaled(window_width, window_height, Qt.KeepAspectRatio)

        self.image_label.setPixmap(scaled_pixmap)

    def create_top_buttons_group(self):

        self.top_buttons_group = QGroupBox()

        button1 = QPushButton("Button 1")
        button2 = QPushButton("Button 2")
        button3 = QPushButton("Button 3")

        layout = QHBoxLayout()
        layout.addWidget(button1)
        layout.addWidget(button2)
        layout.addWidget(button3)

        self.top_buttons_group.setLayout(layout)

def main(images_path, annotations_path):
    app = QApplication(sys.argv)
    viewer = ImageViewer(images_path)
    viewer.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--images-path", default="", type=str, metavar="PATH", help="Path to images folder")
    parser.add_argument("--annotations-path", default="", type=str, metavar="PATH", help="Path to annotations json file")
    args = parser.parse_args()

    main(args.images_path, args.annotations_path)
