import cv2
import os
import random
import numpy as np

from PyQt5.QtGui import QImage


class ImageProcessor:
    def __init__(self, images_path, annotations_path):
        self.image = None
        self.mask = None
        self.file_data = None

        self.images_path = images_path
        self.annotations_path = annotations_path

        self.image_names = []
        self.annotations_files = []
        self.unique_categories_with_colors = {}

        self.images_names = self.read_images_names(self.images_path)
        self.annotations_files_names = self.read_annotation_files(self.annotations_path)

        self._check_amount_of_files()
        self._set_categories_colors(self.annotations_path)

    def _check_amount_of_files(self):
        if len(self.images_names) != len(self.annotations_files_names):
            print(
                "Different length of lists with filenames, check the number of files in the given folders"
            )
            exit()
        else:
            pass

    def read_images_names(self, image_path):
        for file_name in os.listdir(image_path):
            if file_name.endswith(".jpg") or file_name.endswith(".png"):
                self.image_names.append(file_name)
        return self.image_names

    def read_image(self, image_path):
        image = cv2.imread(image_path)
        self.image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # create mask
        height, width, _ = self.image.shape
        self.mask = np.zeros((height, width), dtype=np.uint8)

    def read_annotation_files(self, annotations_path):
        for file_name in os.listdir(annotations_path):
            if file_name.endswith(".txt"):
                self.annotations_files.append(file_name)
        return self.annotations_files

    def _set_categories_colors(self, annotation_path):
        for img_name in self.annotations_files:
            with open(annotation_path + img_name, "r") as file:
                for index, line in enumerate(file):
                    line = str.split(line, " ")
                    if len(line) == 10:
                        category = line[8]
                        if category not in self.unique_categories_with_colors.keys():
                            self.unique_categories_with_colors[category] = (
                                random.randint(0, 255),
                                random.randint(0, 255),
                                random.randint(0, 255),
                            )

    def read_file_data(self, annotation_path):
        self.file_data = {}
        with open(annotation_path, "r") as file:
            for index, line in enumerate(file):
                line = str.split(line, " ")
                if len(line) == 10:
                    int_values = []
                    for value in line[0:8]:
                        value = float(value)
                        value = int(value)
                        int_values.append(value)

                    x_1, y_1, x_2, y_2, x_3, y_3, x_4, y_4 = int_values
                    points = [(x_1, y_1), (x_2, y_2), (x_3, y_3), (x_4, y_4)]
                    category, difficult = line[8:10]

                    color = self.unique_categories_with_colors[category]

                    self.file_data[index] = {
                        "points": points,
                        "category": category,
                        "color": color,
                    }

        # return file_data

    def draw_frames(self):
        for index in self.file_data.keys():
            points = self.file_data[index]["points"]
            color = self.file_data[index]["color"]
            points = np.array(points, dtype=np.int32)

            cv2.polylines(
                self.image,
                [points],
                isClosed=True,
                color=color,
                thickness=2,
            )

            # make binary mask
            cv2.fillPoly(self.mask, pts=[points], color=255)

    def draw_labels(self):
        for index in self.file_data.keys():
            category = self.file_data[index]["category"]
            x_1, y_1 = self.file_data[index]["points"][0]
            color = self.file_data[index]["color"]

            # add starting point
            red_color = (255, 0, 0)
            cv2.circle(self.image, (x_1, y_1), 5, red_color, -1)

            # add annotation text
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.5
            thickness = 2
            text_size, baseline = cv2.getTextSize(category, font, font_scale, thickness)
            background_position = (x_1 + text_size[0], y_1 - text_size[1])

            cv2.rectangle(
                self.image, (x_1, y_1 + baseline), background_position, color, -1
            )
            cv2.putText(
                self.image, category, (x_1, y_1), font, font_scale, (0, 0, 0), thickness
            )

    def save_image(self, image_folder_path, output_folder_path, image_name):
        if output_folder_path == "":
            output_folder_path = image_folder_path + "../saved_images"

        if not os.path.exists(output_folder_path):
            os.makedirs(output_folder_path)

        cv2.imwrite(
            output_folder_path + "/" + image_name,
            cv2.cvtColor(self.image, cv2.COLOR_RGB2BGR),
        )
        print(f"Image {image_name} saved!")

    def save_mask(self, image_folder_path, output_folder_path, image_name):
        if output_folder_path == "":
            output_folder_path = image_folder_path + "../saved_masks"

        if not os.path.exists(output_folder_path):
            os.makedirs(output_folder_path)

        cv2.imwrite(output_folder_path + "/mask_" + image_name, self.mask)
        print(f"Mask from {image_name} saved!")

    def convert_to_qpixmap(self):
        height, width, channels = self.image.shape
        qimage = QImage(
            self.image.data, width, height, channels * width, QImage.Format_RGB888
        )

        return qimage
