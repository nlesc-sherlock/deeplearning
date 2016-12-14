#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Patrick Bos
# @Date:   2016-12-13 11:48:22
# @Last Modified by:   Patrick Bos
# @Last Modified time: 2016-12-14 10:10:24

import cnn_classify
import image_classify_workflow_wrap_lib as flibflob
import json


if __name__ == '__main__':
    # determined empirically
    probability_threshold = 0.6
    # gender parameters
    classifier_key = 'face/gender'
    tag_name_translation = {'m': 'male', 'f': 'female'}

    parser = flibflob.get_workflow_argument_parser()

    args = parser.parse_args()
    print args

    # hard code the json output file, since we need to add this back into the
    # giant workflow json object
    outfn = "/tmp/gender_classification.json"

    input_json = json.load(args.json_input_file)

    image_filenames = flibflob.get_person_face_image_filenames_from_json(input_json)

    if image_filenames:
        with file(outfn, "w") as outfile:
            cnn_classify.run(image_filenames, args.model_path,
                             args.model_snapshot,
                             model_deploy=args.model_deploy,
                             labels_name=args.model_labels,
                             mean_pixel_name=args.mean_pixel_name,
                             gray_range=args.gray_range,
                             channel_swap=args.channel_swap,
                             batch_size=args.batch_size,
                             gpu_id=args.gpu_id, verbose=args.verbose,
                             json=args.json, outfile=outfile)

        with file(outfn, "r") as fp:
            gender_classification = json.load(fp)

        output_json = flibflob.generate_output_json_face(input_json,
                                                         gender_classification,
                                                         probability_threshold,
                                                         classifier_key,
                                                         tag_name_translation)

        json.dump(output_json, args.workflow_out, indent=4)
    else:
        raise Exception("No person faces in input json file.")
