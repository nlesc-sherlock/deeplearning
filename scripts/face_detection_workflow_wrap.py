#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Elena Ranguelova
# @Date:   2016-12-14 11:23

#import sys
#sys.path.insert(0,'/home/elena/Sherlock/deeplearning/FaceDetector/facedetect-master/')
import facedetect as fd
import wrap_lib as wl
import json


if __name__ == '__main__':
    parser = wl.get_workflow_argument_parser()

    args = parser.parse_args()
   # print args

    fd.load_cascades(fd.DATA_DIR)
    
    input_json = json.load(args.json_input_file)

    # N.B.: input_json will be altered!

    if 'person' in input_json['classes'].keys():
        persons = input_json['classes']['person']
        for person in persons:
            image_fn = person['cropped_image']
            _, features = fd.face_detect_file(image_fn)
            person['face'] = {}
            person['face']['path'] = image_fn
            person['face']['bbox'] = list(features[0])

        json.dump(input_json, args.workflow_out, indent=4)
    else:
        raise Exception("No persons in input json file.")
