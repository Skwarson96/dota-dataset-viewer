import argparse
import sys
import cv2
import os
import numpy as np
from PIL import Image
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QSlider, QFrame, QGroupBox, QGridLayout, QGraphicsView, QScrollArea, QGraphicsScene
from PyQt5.QtGui import QPixmap, QWheelEvent, QImage, QTransform
from PyQt5.QtCore import Qt, QRectF


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


class ImageViewer(QWidget):
    def __init__(self, image_path, annotations_path):
        super().__init__()

        self.images_path = image_path
        self.annotations_path = annotations_path
        self.setWindowTitle("DOTA dataset viewer")

        self.current_img_index = 0
        self.image_processor = ImageProcessor()

        self.images_names = self.image_processor.read_images_names(self.images_path)
        self.annotations_files_names = self.image_processor.read_annotation_files(self.annotations_path)

        self.view = QGraphicsView()
        self.scene = QGraphicsScene()

        if len(self.images_names) != len(self.annotations_files_names):
            print('Different length of lists with filenames, check the number of files in the given folders')
            exit()


        self.show_image()
        self.scale_factor = 1

        self.view.setScene(self.scene)

        self.create_top_buttons_group()

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.top_buttons_group)
        main_layout.addWidget(self.view)

        self.setLayout(main_layout)

    def button_clicked(self, button_name):
        print(button_name)


    def show_image(self):
        self.image_processor.read_image(self.images_path + '/' + self.images_names[self.current_img_index])

        annotation_file_name = self.images_names[self.current_img_index].rsplit(".", 1)[0] + '.txt'
        self.image_processor.read_and_draw_annotations(self.annotations_path + '/' + annotation_file_name)

        self.pixmap = QPixmap(self.image_processor.convert_to_qpixmap())
        self.scene.addPixmap(self.pixmap)


    def wheelEvent(self, event: QWheelEvent):
        self.current_scale = 1
        if event.modifiers() & Qt.ControlModifier:
            angle = event.angleDelta().y()

            self.scale_factor = self.scale_factor + (angle / 120) * 0.1

            if self.scale_factor > 5:
                self.scale_factor = 5
            if self.scale_factor < 0.5:
                self.scale_factor = 0.5

            if self.scale_factor < 5 and self.scale_factor > 0.5:
                self.current_scale *= self.scale_factor
                self.view.setTransform(QTransform().scale(self.current_scale, self.current_scale))
        else:
            event.ignore()


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
