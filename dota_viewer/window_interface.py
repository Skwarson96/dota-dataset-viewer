from PyQt5.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QWidget,
    QGroupBox,
    QGraphicsScene,
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QRectF

from dota_viewer.image_processor import ImageProcessor
from dota_viewer.image_viewer import ImageViewer


class WindowInterface(QWidget):
    def __init__(self, image_path, annotations_path, save_images_path, save_masks_path):
        super().__init__()

        self.images_path = image_path
        self.annotations_path = annotations_path
        self.save_images_path = save_images_path
        self.save_masks_path = save_masks_path
        self.hide_labels = False
        self.hide_frames = False
        self.fit_view = True

        self.setWindowTitle("DOTA dataset viewer")

        self.current_img_index = 0
        self.image_processor = ImageProcessor(self.images_path, self.annotations_path)
        self.images_names = self.image_processor.images_names

        self.view = ImageViewer()
        self.scene = QGraphicsScene()

        self.create_top_buttons_group()
        self.create_information_label_group()

        self.show_image()
        self.scale_factor = 1

        self.view.setScene(self.scene)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.top_buttons_group)
        main_layout.addWidget(self.information_labels_group)
        main_layout.addWidget(self.view)

        self.setLayout(main_layout)

    def show_image(self):
        self.image_processor.read_image(
            self.images_path + "/" + self.images_names[self.current_img_index]
        )

        annotation_file_name = (
            self.images_names[self.current_img_index].rsplit(".", 1)[0] + ".txt"
        )

        self.image_processor.read_file_data(
            self.annotations_path + "/" + annotation_file_name
        )

        if not self.hide_frames:
            self.image_processor.draw_frames()

        if not self.hide_labels:
            self.image_processor.draw_labels()

        self.image_info_label.setText(
            f"Image name: {self.images_names[self.current_img_index]}, image number: {self.current_img_index+1}/{len(self.images_names)}"
        )

        self.pixmap = QPixmap(self.image_processor.convert_to_qpixmap())

        self.scene.clear()
        if self.fit_view:
            self.scene.setSceneRect(QRectF(self.pixmap.rect()))
            self.view.fitInView(
                self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio
            )

            scale_factor = self._adjust_scale(self.view.transform().m11())
            self.view.scale(1.0 * scale_factor, 1.0 * scale_factor)

        self.scene.addPixmap(self.pixmap)
        self.view.show()

    def create_top_buttons_group(self):
        self.top_buttons_group = QGroupBox()

        prev_img_button = QPushButton("Prev image")
        next_img_button = QPushButton("Next image")
        save_img_button = QPushButton("Save image")
        save_mask_button = QPushButton("Save mask")
        toggle_labels_button = QPushButton("Toggle labels")
        toggle_frames_button = QPushButton("Toggle frames")

        prev_img_button.clicked.connect(self.prev_img_button_clicked)
        next_img_button.clicked.connect(self.next_img_button_clicked)
        save_img_button.clicked.connect(self.save_img_button_clicked)
        save_mask_button.clicked.connect(self.save_mask_button_clicked)
        toggle_labels_button.clicked.connect(self.toggle_labels_button_clicked)
        toggle_frames_button.clicked.connect(self.toggle_frames_button_clicked)

        layout = QGridLayout()
        layout.addWidget(prev_img_button, 0, 0)
        layout.addWidget(next_img_button, 0, 1)
        layout.addWidget(save_img_button, 0, 2)
        layout.addWidget(save_mask_button, 0, 3)
        layout.addWidget(toggle_labels_button, 1, 0)
        layout.addWidget(toggle_frames_button, 1, 1)

        self.top_buttons_group.setLayout(layout)

    def create_information_label_group(self):
        self.information_labels_group = QGroupBox()

        self.image_info_label = QLabel()

        layout = QHBoxLayout()
        layout.addWidget(self.image_info_label)

        self.information_labels_group.setLayout(layout)

    def _adjust_scale(self, current_scale):
        scale_factor = 1 / current_scale
        return scale_factor

    def prev_img_button_clicked(self):
        if abs(self.current_img_index - 1) == len(self.images_names):
            self.current_img_index = 0
        else:
            self.current_img_index = self.current_img_index - 1

        self.fit_view = True
        self.show_image()

    def next_img_button_clicked(self):
        if self.current_img_index + 1 == len(self.images_names):
            self.current_img_index = 0
        else:
            self.current_img_index = self.current_img_index + 1

        self.fit_view = True
        self.show_image()

    def save_img_button_clicked(self):
        self.image_processor.save_image(
            self.images_path,
            self.save_images_path,
            self.images_names[self.current_img_index],
        )

    def save_mask_button_clicked(self):
        self.image_processor.save_mask(
            self.images_path,
            self.save_masks_path,
            self.images_names[self.current_img_index],
        )

    def toggle_labels_button_clicked(self):
        self.hide_labels = not self.hide_labels
        self.fit_view = False
        self.show_image()

    def toggle_frames_button_clicked(self):
        self.hide_frames = not self.hide_frames
        self.fit_view = False
        self.show_image()
