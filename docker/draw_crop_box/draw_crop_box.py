#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import skimage
import skimage.io
import argparse
import json
import os


def load_image(filename):
    image = skimage.img_as_float(skimage.io.imread(filename))
    return image


def load_image_boxes(filename, filehandle):
    json_dict = json.load(filehandle)
    return json_dict[filename]['boxes']


def draw_box(ax, left, top, width, height, color=(0, 0, 0)):
    coords = ((left, top), width, height)
    rect = plt.Rectangle(*coords, fill=False, edgecolor=color, linewidth=2)
    ax.add_patch(rect)


def draw_label(ax, left, top, class_name, class_score, color=(0, 0, 0)):
    display_txt = '%s: %.2f' % (class_name, class_score)
    ax.text(left, top, display_txt, bbox={'facecolor': color, 'alpha': 0.5})


def get_argument_parser():
    parser = argparse.ArgumentParser()

    # filenames
    parser.add_argument("image_file",
                        help="The file path of the image file.",
                        type=argparse.FileType('r'))
    parser.add_argument("image_boxes_file",
                        help="The file path of the file containing the "
                        "coordinates of the boxes you want to draw in the "
                        "image.",
                        type=argparse.FileType('r'))
    parser.add_argument("-o", "--output_file", help="Output file path",
                        type=argparse.FileType('w'), default="-")  # "-" means stdout

    return parser


def get_output_format(output_file):
    filename = output_file.name
    # get format from filename, or from backend's default filetype
    format = os.path.splitext(filename)[1][1:]
    if format == '':
        format = 'jpg'
    format = format.lower()
    return format


def main():
    parser = get_argument_parser()
    args = parser.parse_args()

    image = load_image(args.image_file.name)
    boxes = load_image_boxes(args.image_file.name, args.image_boxes_file)

    fig, ax = plt.subplots(1, 1)

    ax.imshow(image)

    colors = plt.cm.Set2(np.linspace(0, 1, 9)).tolist()

    for ix, box in enumerate(boxes):
        color = colors[ix % len(colors)]
        draw_box(ax, box['left'], box['top'], box['width'], box['height'],
                 color=color)
        draw_label(ax, box['left'], box['top'],
                   box['class_name'], box['class_score'],
                   color=color)

    fig.savefig(args.output_file, format=get_output_format(args.output_file))


if __name__ == "__main__":
    main()
