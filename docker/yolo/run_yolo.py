#!/usr/bin/env python
"""
Analyze an image using YOLO and print tags found of found concepts in the image with their probabilities and bounding
boxes
Usage:
  run_yolo.py <imagepath>
"""
from docopt import docopt
import subprocess

if __name__ == '__main__':
    args = docopt(__doc__)
    image_path = args['<imagepath>']
    command = ['./darknet', 'yolo', 'test', 'cfg/yolo.cfg', 'yolo.weights', image_path]
    subprocess.call(command)