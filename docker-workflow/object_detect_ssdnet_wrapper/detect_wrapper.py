#!/usr/bin/env python

import detect
import argparse
import json

def get_image_filenames_from_json(json_object):
    if 'files' in json_object.keys():
        return json_object['files']


def generate_output_json(input_json, object_detection):
    ''' Example object_detection:
        "classifications": [
        {   
            "bbox": [
                170.0,
                16.0,
                178.0,
                342.0
            ],
            "class": "domestic_cat",
            "path": "/opt/caffe/examples/images/cat.jpg",
            "probability": 0.9747376441955566
        },
        {   
            "bbox": [
                96.0,
                134.0,
                383.0,
                184.0
            ],
            "class": "unicycle",
            "path": "/opt/caffe/examples/images/fish-bike.jpg",
            "probability": 0.2054128497838974
        }
    ]
    '''
    if 'classes' not in input_json.keys():
        input_json['classes'] = {} 


    classes = input_json['classes']
    for item in object_detection['classifications']:
        if not item['class'] in classes.keys():
            classes[item['class']] = []
        
        classes[item['class']].append({
            'path': item['path'],
            'probability': item['probability'],
            'bbox': item['bbox']
        })
    
    return input_json


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
    parser.add_argument("-v", "--verbose", help="Verbose mode.", action="store_true", default=0)

    args = parser.parse_args()
    print args

    # hard code the json output file, since we need to add this back into the
    # giant workflow json object
    outfn = "/tmp/detection.json"

    verbose = args.verbose

    input_json = json.load(args.json_input_file)

    image_filenames = get_image_filenames_from_json(input_json)

    if image_filenames:
        with file(outfn, "w") as outfile:    
            threshold = 0.2
            detect.detect_objects(image_filenames, threshold, outfile) 


        with file(outfn, "r") as fp:
            object_detection = json.load(fp)

        output_json = generate_output_json(input_json, object_detection)
        
        if verbose:
            print(json.dumps(output_json, indent=4))

    json.dump(output_json, args.workflow_out, indent=4, sort_keys=True)
