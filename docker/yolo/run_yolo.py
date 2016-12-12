#!/usr/bin/env python
"""
Analyze a set of images using YOLO and print tags of found concepts in the image with their probabilities and bounding
boxes. Image paths are defined in a json file.

{
    "files" : [
        "/path/to/image",
        "/and/another/image"
    ]
}

The output will be another json file.

{
    "files" : [
        "/path/to/image",
        "/and/another/image"
    ],
    {
        "classes":{
            "car" : [
                {
                    "path" : "/path/to/image",
                    "probability" : <float>,
                    "bbox" : [x, y, w, h]
                },
                {
                    "path" : "/and/another/image",
                    "probability" : <float>,
                    "bbox" : [x, y, w, h]
                }
            ],
            "person" : [
                {
                    "path" : "/and/another/image",
                    "probability" : <float>,
                    "bbox" : [x, y, w, h]
                }
            ]
        }
    }
}

Usage:std
  run_yolo.py <input_path> <output_path>
"""
from docopt import docopt
import json
import subprocess


def line_to_occurrence(path, line):
    occurrence = {'path':path}
    for pair in line.split(','):
        key, value = pair.split(':')
        key = key.strip(" '")
        value = value.strip(" '")
        if key == 'class':
            clas = value
        if key == 'prob':
            occurrence['probability'] = float(value)
        if key == 'left':
            left = int(value)
        if key == 'top':
            top = int(value)
        if key == 'right':
            right = int(value)
        if key == 'bottom':
            bottom = int(value)
    bbox = [left, top, right - left, top - bottom]
    occurrence['bbox'] = bbox
    return clas, occurrence


if __name__ == '__main__':
    args = docopt(__doc__)
    with open(args['<input_path>'], 'r') as json_file:
        json_input = json.load(json_file)
        classes = {}
        for input_path in json_input['files']:
            command = ["./darknet", "detect", "cfg/yolo.cfg", "yolo.weights", input_path]
            temp_path = 'output.tmp'
            result = subprocess.check_output(command)
            for line in result.split('\n'):
                if line.startswith("'class':"):
                    clas, occurrence = line_to_occurrence(input_path, line)
                    if clas in classes:
                        classes[clas].append(occurrence)
                    else:
                        classes[clas] = [occurrence]
        json_output = json_input
        json_output['classes'] = classes

    with open(args['<output_path>'], 'w') as output_file:
        json.dump(json_output, output_file, indent=4, sort_keys=True, ensure_ascii=False)
