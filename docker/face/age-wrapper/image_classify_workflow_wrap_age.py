#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Patrick Bos
# @Date:   2016-12-13 11:48:22
# @Last Modified by:   Patrick Bos
# @Last Modified time: 2016-12-14 13:33:54

import cnn_classify
import crablip
import json


if __name__ == '__main__':
    # determined empirically
    probability_threshold = 0.15
    # age parameters
    classifier_key = 'face/age'

    parser = crablip.get_workflow_argument_parser()

    args = parser.parse_args()
    print args

    # hard code the json output file, since we need to add this back into the
    # giant workflow json object
    outfn = "/tmp/age_classification.json"

    input_json = json.load(args.json_input_file)
    output_json = input_json
    data_path = args.data_path

    image_filenames = crablip.get_person_face_image_filenames_from_json(input_json)

    if image_filenames:
        with file(outfn, "w") as outfile:
            cnn_classify.run(data_path, image_filenames, args.model_path,
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
            classification = json.load(fp)

        output_json = crablip.generate_output_json_face(input_json,
                                                        classification,
                                                        probability_threshold,
                                                        classifier_key)

    json.dump(output_json, args.workflow_out, indent=4)
    
