# -*- coding: utf-8 -*-
# @Author: Patrick Bos
# @Date:   2016-12-14 08:05:09
# @Last Modified by:   Patrick Bos
# @Last Modified time: 2016-12-14 08:08:55

import cnn_classify
import argparse


def get_person_face_image_filenames_from_json(json_object):
    filenames = []
    if 'person' in json_object['classes'].keys():
        persons = json_object['classes']['person']
        for person in persons:
            if 'face' in person.keys():
                filenames.append(person['face']['cropped_image'])
    return filenames


def get_workflow_argument_parser():
    parser = cnn_classify.get_default_argument_parser()

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

    return parser
