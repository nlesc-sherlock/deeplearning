#!/usr/bin/env python
"""
Analyze a set of images using ResNet50 and print classifications of the image along with their probabilities.

Usage:std
  imagenet.py IMAGE_PATH ...
"""

from docopt import docopt
from keras.applications.resnet50 import ResNet50
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np

height = 224
width = 224
channels = 3
top = 5


def load_image(path):
    img = image.load_img(path, target_size=(224, 224))
    x = image.img_to_array(img)
    return x


if __name__ == '__main__':
    args = docopt(__doc__)
    paths = args['IMAGE_PATH']
    model = ResNet50(weights='imagenet')

    x = np.zeros((len(paths), height, width, channels))
    for i, path in enumerate(paths):
        x[i] = load_image(path)
    x = preprocess_input(x)

    predictions = decode_predictions(model.predict(x), top=top)
    for i, path in enumerate(paths):
        print(paths[i], predictions[i])
