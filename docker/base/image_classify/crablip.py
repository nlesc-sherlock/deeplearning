# -*- coding: utf-8 -*-
# @Author: Patrick Bos
# @Date:   2016-12-14 08:05:09
# @Last Modified by:   Patrick Bos
# @Last Modified time: 2016-12-14 13:30:31

import argparse


def get_default_argument_parser():
    parser = argparse.ArgumentParser()

    # model file parameters
    parser.add_argument("-M", "--model_path", help="Model files directory. Should contain the files: snapshot.caffemodel, deploy.prototxt and labels.txt. Any files with other filenames can be given with other parameters (see below).", required=True)
    parser.add_argument("-D", "--data_path", help="Directory path of where the data is mounted. If this script is running whithin a docker it should be the docker local path", default="/data")
    model_group = parser.add_argument_group(title="Model file names.", description="Override the default filenames of the model.")
    model_group.add_argument("--model_snapshot", help="The filename of the caffemodel snapshot in the model directory.", default='snapshot.caffemodel')
    model_group.add_argument("--model_deploy", help="The filename of the deploy file in the model directory.", default='deploy.prototxt')
    model_group.add_argument("--model_labels", help="The filename of the labels file in the model directory.", default='labels.txt')
    model_group.add_argument("--mean_pixel_name", help="Mean pixel file name of the trained model (default: mean.binaryproto).", default='mean.binaryproto')

    output_group = parser.add_argument_group(title="Output format.", description="Define the output format.")
    output_group.add_argument("--json", help="Output json format",
                              action="store_true", default=0)
    output_group.add_argument("-o", "--outfile", help="Output file path",
                              type=argparse.FileType('w'), default="-")

    parser.add_argument("--gray_range", help="Gray range of the images (default: 255).", type=int, default=255)
    parser.add_argument("--channel_swap", help="Use numbers 0, 1 and 2 to give the order of the color-channels that the model used, for instance 0 1 2 for RGB. Some models swap the channels from RGB to BGR (this is the default: 2 1 0).", nargs=3, default=[2, 1, 0])
    parser.add_argument("--batch_size", help="Number of images processed simultaneously. Default: taken from model configuration.", type=int, default=0)
    parser.add_argument("--gpu_id", help="To use GPU mode, specify the gpu_id that you want to use. Default: CPU mode (-1).", type=int, default=-1)

    parser.add_argument("-v", "--verbose", help="Verbose mode.", action="store_true", default=0)

    return parser


def get_class_image_filenames_from_json(json_object, class_key,
                                        subclass_key=None):
    filenames = []
    if class_key in json_object['classes'].keys():
        class_objects = json_object['classes'][class_key]
        for class_object in class_objects:
            fn = None
            if subclass_key is not None:
                if subclass_key in class_object.keys():
                    fn = class_object[subclass_key]['cropped_image']
            else:
                fn = class_object['cropped_image']
            if fn is not None:
                filenames.append(fn)
    return filenames


def get_person_face_image_filenames_from_json(json_object):
    return get_class_image_filenames_from_json(json_object, 'person',
                                               subclass_key='face')


def get_person_image_filenames_from_json(json_object):
    return get_class_image_filenames_from_json(json_object, 'person')


def get_workflow_argument_parser():
    parser = get_default_argument_parser()

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
