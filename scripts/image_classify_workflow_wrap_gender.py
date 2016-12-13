# -*- coding: utf-8 -*-
# @Author: Patrick Bos
# @Date:   2016-12-13 11:48:22
# @Last Modified by:   Patrick Bos
# @Last Modified time: 2016-12-13 12:53:45

import cnn_classify
import json

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("json_file", help="The filename (including path, full or relative) of the json file that specifies the input to the classifier.")

    json.
    cnn_classify.run(image_filenames, args.model_path, args.model_snapshot,
                     model_deploy=args.model_deploy, labels_name=args.model_labels,
                     mean_pixel_name=args.mean_pixel_name, gray_range=args.gray_range,
                     channel_swap=args.channel_swap, batch_size=args.batch_size,
                     gpu_id=args.gpu_id, verbose=args.verbose, json=args.json,
                     outfile=args.outfile)

