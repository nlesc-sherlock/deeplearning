# -*- coding: utf-8 -*-
# @Author: Patrick Bos
# @Date:   2016-12-14 08:05:09
# @Last Modified by:   Patrick Bos
# @Last Modified time: 2016-12-14 11:05:20

import cnn_classify
import argparse


def get_class_image_filenames_from_json(json_object, class_key,
                                        subclass_key=None):
    filenames = []
    if class_key in json_object['classes'].keys():
        class_objects = json_object['classes'][class_key]
        for class_object in class_objects:
            if subclass_key is not None:
                if subclass_key in class_object.keys():
                    fn = class_object[subclass_key]['cropped_image']
            else:
                fn = class_object['cropped_image']
            filenames.append(fn)
    return filenames


def get_person_face_image_filenames_from_json(json_object):
    return get_class_image_filenames_from_json(json_object, 'person',
                                               subclass_key='face')

def get_person_image_filenames_from_json(json_object):
    return get_class_image_filenames_from_json(json_object, 'person')

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
    for tag in tags:
        new_tags.append({'name': translate[tag['name']],
                         'probability': tag['probability']})
    return new_tags


def generate_output_json(input_json, classification, probability_threshold,
                         classifier_key, class_key, tag_name_translation=None,
                         subclass_key=None):
    class_objects = input_json['classes'][class_key]
    predictions = classification['predictions']
    tags = {}
    for fn, prediction in predictions.iteritems():
        tags[fn] = {}
        for name, probability in prediction['tags'].iteritems():
            if probability > probability_threshold:
                tags[fn][name] = probability
    classification = {'classifier': classifier_key}
    for class_object in class_objects:
        if subclass_key is not None:
            if subclass_key in class_object.keys():
                classified_object = class_object[subclass_key]
        else:
            classified_object = class_object

        fn = classified_object['cropped_image']
        classified_object.setdefault('classification', []).append(classification.copy())
        mangled_tags = inflate_tags(tags[fn])
        if tag_name_translation is not None:
            mangled_tags = translate_tag_names(mangled_tags,
                                               tag_name_translation)
        classified_object['classification'][-1]['tags'] = mangled_tags

    # note that we modified the input_json object!
    return input_json


def generate_output_json_face(input_json, classification, probability_threshold,
                              classifier_key, tag_name_translation=None):
    output_json = generate_output_json(input_json, classification,
                                       probability_threshold, classifier_key,
                                       'person',
                                       tag_name_translation=tag_name_translation,
                                       subclass_key='face')
    return output_json
