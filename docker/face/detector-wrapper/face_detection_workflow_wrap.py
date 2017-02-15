#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Elena Ranguelova
# @Date:   2016-12-14 11:23

import os
import facedetect as fd
import crablip
import json

if __name__ == '__main__':
    parser = crablip.get_workflow_argument_parser()

    args = parser.parse_args()
    # print args

    data_path = args.data_path

    fd.load_cascades(fd.DATA_DIR)

    input_json = json.load(args.json_input_file)
    output_json = input_json

    if 'person' in output_json['classes'].keys():
        persons = output_json['classes']['person']
        for person in persons:
            image_fn = person['cropped_image']
            image_path = os.path.join(data_path, image_fn)
            _, features = fd.face_detect_file(image_path)
            if len(features) > 0:
                person[u'face'] = {}
                person[u'face'][u'path'] = image_fn
                person[u'face'][u'bbox'] = [int(x) for x in list(features[0])]

    json.dump(output_json, args.workflow_out, indent=4)
