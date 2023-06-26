import argparse
import sys
import cv2
import os
import numpy as np
from PIL import Image
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QSlider, QFrame, QGroupBox, QGridLayout, QGraphicsView, QScrollArea
from PyQt5.QtGui import QPixmap, QWheelEvent, QImage
from PyQt5.QtCore import Qt


class ImageProcessor:
    def __init__(self):
        self.image = None

    def read_images_names(self, image_path):
        image_names = []
        for file_name in os.listdir(image_path):
            if file_name.endswith('.jpg') or file_name.endswith('.png'):
                image_names.append(file_name)
        return image_names

    def read_image(self, image_path):
        image = cv2.imread(image_path)
        self.image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


    def read_annotation_files(self, annotations_path):
        annotations_files = []
        for file_name in os.listdir(annotations_path):
            if file_name.endswith('.txt'):
                annotations_files.append(file_name)
        return annotations_files

    def read_and_draw_annotations(self, annotation_path):
        with open(annotation_path, 'r') as file:
            for line in file:
                line = str.split(line, ' ')
                if len(line) == 10:
                    int_values = []
                    for value in line[0:8]:
                        value = float(value)
                        value = int(value)
                        int_values.append(value)

                    x_1, y_1, x_2, y_2, x_3, y_3, x_4, y_4 = int_values
                    points = [(x_1, y_1), (x_2, y_2), (x_3, y_3), (x_4, y_4)]
                    category, difficult = line[8:10]

                    points = np.array(points, dtype=np.int32)

                    cv2.polylines(self.image, [points], isClosed=True, color=(0, 255, 0), thickness=2)

    def save_image(self, output_path):
        self.image.save(output_path)


    def convert_to_qpixmap(self):
        height, width, channels = self.image.shape
        qimage = QImage(self.image.data, width, height, channels * width, QImage.Format_RGB888)

        return qimage


class ImageViewer(QMainWindow):
    def __init__(self, images_path, annotations_path):
        super().__init__()
        self.images_path = images_path
        self.annotations_path = annotations_path
        self.setWindowTitle("Test window")

        self.current_img_index = 0
        self.image_processor = ImageProcessor()

        self.images_names = self.image_processor.read_images_names(self.images_path)
        self.annotations_files_names = self.image_processor.read_annotation_files(self.annotations_path)

        if len(self.images_names) != len(self.annotations_files_names):
            print('Different length of lists with filenames, check the number of files in the given folders')
            exit()

        self.window_width = 800
        self.window_height = 800
        self.setGeometry(100, 100, self.window_width, self.window_height)

        image_widget = QWidget()
        self.setCentralWidget(image_widget)

        self.create_top_buttons_group()
        self.create_image_label(self.window_width, self.window_height)


        main_layout = QGridLayout()
        main_layout.addWidget(self.top_buttons_group)
        main_layout.addWidget(self.image_label)
        image_widget.setLayout(main_layout)
        self.show_image()


    def wheelEvent(self, event: QWheelEvent):
        print('wheelEvent')

    def create_image_label(self, window_width, window_height):
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)

    def show_image(self):

        self.image_processor.read_image(self.images_path + '/' + self.images_names[self.current_img_index])

        annotation_file_name = self.images_names[self.current_img_index].rsplit(".", 1)[0] + '.txt'
        self.image_processor.read_and_draw_annotations(self.annotations_path + '/' + annotation_file_name)

        self.pixmap = QPixmap(self.image_processor.convert_to_qpixmap())
        pixmap_width = self.pixmap.width()
        pixmap_height = self.pixmap.height()

        if self.window_width > pixmap_width or self.window_height > pixmap_height:
            scaled_pixmap = self.pixmap.scaled(pixmap_width, pixmap_height, Qt.KeepAspectRatio)
        else:
            scaled_pixmap = self.pixmap.scaled(self.window_width, self.window_height, Qt.KeepAspectRatio)

        self.image_label.setPixmap(scaled_pixmap)


    def create_top_buttons_group(self):

        self.top_buttons_group = QGroupBox()

        prev_img_button = QPushButton("Prev image")
        next_img_button = QPushButton("Next image")
        button3 = QPushButton("Button 3")

        prev_img_button.clicked.connect(self.prev_img_button_clicked)
        next_img_button.clicked.connect(self.next_img_button_clicked)

        layout = QHBoxLayout()
        layout.addWidget(prev_img_button)
        layout.addWidget(next_img_button)
        layout.addWidget(button3)

        self.top_buttons_group.setLayout(layout)

    def prev_img_button_clicked(self):
        if abs(self.current_img_index - 1) == len(self.images_names):
            self.current_img_index = 0
        else:
            self.current_img_index = self.current_img_index - 1

        self.show_image()

    def next_img_button_clicked(self):
        if self.current_img_index + 1 == len(self.images_names):
            self.current_img_index = 0
        else:
            self.current_img_index = self.current_img_index + 1

        self.show_image()


def main(images_path, annotations_path):
    app = QApplication(sys.argv)
    viewer = ImageViewer(images_path, annotations_path)
    viewer.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--images-path", default="", type=str, metavar="PATH", help="Path to images folder")
    parser.add_argument("--annotations-path", default="", type=str, metavar="PATH", help="Path to annotations json file")
    args = parser.parse_args()

    main(args.images_path, args.annotations_path)
