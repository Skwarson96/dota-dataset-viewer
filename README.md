# dota-dataset-viewer

A simple application to view data saved in [DOTA](https://captain-whu.github.io/DOTA/dataset.html) format

![GIF](https://github.com/Skwarson96/dota-dataset-viewer/blob/readme_and_refactor/assets/dota_viewer.gif)

## Installation
``` 
pip3 install -r requirements.txt
pip3 install opencv-python-headless==4.7.0.72 
```

## Usage
```
python3 dota_viewer.py

optional arguments:
- --images-path         Path to images folder
- --annotations-path    Path to annotations json file
- --save-images-path    Path to the folder for saving photos with annotations
- --save-masks-path     Path to the folder for saving binary masks
```
<kbd>Ctrl</kbd> + <kbd>WheelKey</kbd> Zooming in and out

## Example
```
python3 dota_viewer.py --images-path ./dota/images/ --annotations-path ./dota/annotations/ --save-images-path ./dota/saved_images --save-masks-path ./dota/saved_masks
```
