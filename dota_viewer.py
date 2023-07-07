import argparse
import sys

from PyQt5.QtWidgets import QApplication

from dota_viewer.window_interface import WindowInterface


def main(images_path, annotations_path, save_images_path, save_masks_path):
    app = QApplication(sys.argv)
    viewer = WindowInterface(
        images_path, annotations_path, save_images_path, save_masks_path
    )
    viewer.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--images-path",
        default="./images/",
        type=str,
        metavar="PATH",
        help="Path to images folder",
    )
    parser.add_argument(
        "--annotations-path",
        default="./annotations/",
        type=str,
        metavar="PATH",
        help="Path to annotations json file",
    )
    parser.add_argument(
        "--save-images-path",
        default="",
        type=str,
        metavar="PATH",
        help="Path to the folder for saving photos with annotations",
    )
    parser.add_argument(
        "--save-masks-path",
        default="",
        type=str,
        metavar="PATH",
        help="Path to the folder for saving binary masks",
    )
    args = parser.parse_args()

    main(
        args.images_path,
        args.annotations_path,
        args.save_images_path,
        args.save_masks_path,
    )
