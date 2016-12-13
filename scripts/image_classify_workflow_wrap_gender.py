# -*- coding: utf-8 -*-
# @Author: Patrick Bos
# @Date:   2016-12-13 11:48:22
# @Last Modified by:   Patrick Bos
# @Last Modified time: 2016-12-13 14:16:53

import cnn_classify
import argparse
import json


def get_person_face_image_filenames_from_json(json_object):
    filenames = []
    if 'person' in json_object.keys():
        persons = json_object['classes']['person']
        for person in persons:
            if 'face' in person.keys():
                filenames.append(person['face']['cropped_image'])
    return filenames


def inflate_tags(tags):
    """
    The json output in cnn_classify uses a compact json notation of
    <class>: <probability>. We want out tags to be in
    "name": <class>, "probability": <probability> format.
    In addition, we want "female" instead of "f" and "male" instead of "m".
    """
    translate = {'m': 'male', 'f': 'female'}
    new_tags = []
    for name, probability in tags.iteritems():
        new_tags.append({'name': translate[name], 'probability': probability})
    return new_tags


def generate_output_json(input_json, gender_classification):
    persons = input_json['classes']['person']
    predictions = gender_classification['predictions']
    classification = {'classifier': 'face/gender'}
    for person in persons:
        if 'face' in person.keys():
            person['face'].setdefault('classification', []).append(classification)
            filename = person['face']['cropped_image']
            person['face']['classification'][-1]['tags'] = inflate_tags(predictions[filename]['tags'])

    # note that we modified the input_json object!
    return input_json


if __name__ == '__main__':
    parser = cnn_classify.get_default_argument_parser()

    parser.add_argument("json_input_file",
                        help="The filename (including path, full or relative) "
                             "of the json file that specifies the input to the "
                             "classifier.",
                        type=argparse.FileType('r'), required=True)
    parser.add_argument("--workflow_out",
                        help="Filename (including path, full or relative) "
                             "of the output json file in the Sherlock workflow "
                             "specification.", required=True)

    args = parser.parse_args()
    print args

    # hard code the json output file, since we need to add this back into the
    # giant workflow json object
    outfile = "/tmp/gender_classification.json"

    input_json = json.load(args.json_input_file)

    image_filenames = get_person_face_image_filenames_from_json(input_json)

    if image_filenames:
        cnn_classify.run(image_filenames, args.model_path, args.model_snapshot,
                         model_deploy=args.model_deploy,
                         labels_name=args.model_labels,
                         mean_pixel_name=args.mean_pixel_name,
                         gray_range=args.gray_range,
                         channel_swap=args.channel_swap,
                         batch_size=args.batch_size,
                         gpu_id=args.gpu_id, verbose=args.verbose,
                         json=args.json, outfile=outfile)

        with file("/tmp/gender_classification.json", "r") as fp:
            gender_classification = json.load(fp)

        output_json = generate_output_json(input_json, gender_classification)

        with file("/output/" + args.workflow_out, "w") as fp:
            json.dump(output_json, fp)
    else:
        raise Exception("No person faces in input json file.")
