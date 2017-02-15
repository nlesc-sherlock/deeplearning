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
import os
import subprocess
import argparse
import json


def line_to_occurrence(path, line):
    occurrence = {'path':path}
#    print "Image: ", path, "This is the line: ", line
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
    bbox = [left, top, right - left, bottom - top]
    occurrence['bbox'] = bbox
    return clas, occurrence


def get_image_filenames_from_json(json_object):
    if 'files' in json_object.keys():                                                                                                                                 
        return json_object['files']


if __name__ == '__main__':
    parser = argparse.ArgumentParser() 

    parser.add_argument("json_input_file", 
                        help="The filename (including path, full or relative) " 
                             "of the json file that specifies the input to the " 
                             "classifier.", 
                             type=argparse.FileType('r')) 
    parser.add_argument("--workflow_out", 
                        help="Filename (including path, full or relative) " 
                        "of the output json file in the Sherlock workflow " 
                        "specification.", required=True, 
                        type=argparse.FileType('w')) 
    parser.add_argument("--input_directory", required=True) 
    parser.add_argument("-v", "--verbose", help="Verbose mode.", action="store_true", default=0) 
 
    args = parser.parse_args() 
     
    if args.verbose: 
        print args 

    verbose = args.verbose 
    input_json = json.load(args.json_input_file) 

    image_filenames = get_image_filenames_from_json(input_json)
    if image_filenames:
        classes = {}
        for input_path in input_json['files']:
            input_file = os.path.join(args.input_directory, input_path)
            command = ["./darknet", "detect", "cfg/yolo.cfg", "yolo.weights", input_file]
            temp_path = 'output.tmp'
            result = subprocess.check_output(command, cwd='/darknet')
            for line in result.split('\n'):
                if line.startswith("'class':"):
                    clas, occurrence = line_to_occurrence(input_path, line)
                    if clas in classes:
                        classes[clas].append(occurrence)
                    else:
                        classes[clas] = [occurrence]
        json_output = input_json
        json_output['classes'] = classes

    json.dump(json_output, args.workflow_out, indent=4, sort_keys=True, ensure_ascii=False)
