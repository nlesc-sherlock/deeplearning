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
                    "id" : "/path/to/image",
                    "probability" : <float>,
                    "bbox" : [x, y, w, h]
                },
                {
                    "id" : "/and/another/image",
                    "probability" : <float>,
                    "bbox" : [x, y, w, h]
                }
            ],
            "person" : [
                {
                    "id" : "/and/another/image",
                    "probability" : <float>,
                    "bbox" : [x, y, w, h]
                }
            ]
        }
    }
}

Usage:std
  run_yolo.py <jsonpath>
"""
from docopt import docopt
import json
import subprocess

if __name__ == '__main__':
    args = docopt(__doc__)
    input = json.loads(args['<jsonpath>'])
    for input_path in input['files']:
        command = ["./darknet", "detect", "cfg/yolo.cfg", "yolo.weights", input_path]
        temp_path = 'output.tmp'
        with open(temp_path, 'w') as output_file:
            result = subprocess.call(command, stdout=output_file)
        with open(temp_path, 'r') as output_file:
            elements = {}
            for line in output_file:
                if line.startswith("'class':"):
                    occurence = {}
                    for key, value in line.split(','):
                        if key in ['class', 'prob']
                        occurence[key], value

