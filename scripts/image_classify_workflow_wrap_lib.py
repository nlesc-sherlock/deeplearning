# -*- coding: utf-8 -*-
# @Author: Patrick Bos
# @Date:   2016-12-14 08:05:09
# @Last Modified by:   Patrick Bos
# @Last Modified time: 2016-12-14 08:29:00

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


def inflate_tags(tags):
    """
    The json output in cnn_classify uses a compact json notation of
    <class>: <probability>. We want out tags to be in
    "name": <class>, "probability": <probability> format.
    """
    new_tags = [{'name': n, 'probability': p} for n, p in tags.iteritems()]
    return new_tags


def translate_tag_names(tags, translate):
    """
    E.g. for gender, we want "female" instead of "f" and "male" instead of "m".
    """
    new_tags = []
    for tag in tags.iteritems():
        new_tags.append({'name': translate[tag['name']],
                         'probability': tag['probability']})
    return new_tags


def generate_output_json_face(input_json, classification, probability_threshold,
                              classifier_key, tag_name_translation):
    persons = input_json['classes']['person']
    predictions = classification['predictions']
    tags = {}
    for fn, prediction in predictions.iteritems():
        tags[fn] = {}
        for name, probability in prediction['tags'].iteritems():
            if probability > probability_threshold:
                tags[fn][name] = probability
    classification = {'classifier': classifier_key}
    for person in persons:
        if 'face' in person.keys():
            fn = person['face']['cropped_image']
            person['face'].setdefault('classification', []).append(classification.copy())
            mangled_tags = translate_tag_names(inflate_tags(tags[fn]),
                                               tag_name_translation)
            person['face']['classification'][-1]['tags'] = mangled_tags

    # note that we modified the input_json object!
    return input_json
