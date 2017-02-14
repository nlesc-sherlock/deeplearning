#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Patrick Bos
# @Date:   2016-12-13 11:48:22
# @Last Modified by:   Patrick Bos
# @Last Modified time: 2016-12-14 15:24:48

import cnn_classify
import crablip
import json
import os

if __name__ == '__main__':
    # determined empirically
    probability_threshold = 0.9
    # parameters
    class_key = 'car'
    classifier_key = 'car/color'

    parser = crablip.get_workflow_argument_parser()

    args = parser.parse_args()
    print args

    # hard code the json output file, since we need to add this back into the
    # giant workflow json object
    outfn = "classification.json"

    input_json = json.load(args.json_input_file)
    output_json = input_json 
    
    
    image_filenames = crablip.get_class_image_filenames_from_json(input_json,
                                                                  class_key)
 
    #image_filenames = [os.path.join(args.data_path, filename) for filename in image_filenames]
    if image_filenames:
        with file(outfn, "w") as outfile:
            cnn_classify.run(args.data_path, image_filenames, args.model_path,
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

        output_json = crablip.generate_output_json(input_json,
                                                   classification,
                                                   probability_threshold,
                                                   classifier_key, class_key)

    json.dump(output_json, args.workflow_out, indent=4)
    
