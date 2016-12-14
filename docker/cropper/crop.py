#!/usr/bin/env python

import argparse, json, os, subprocess

def crop(classification, output_folder):
    filepath = classification['path']
    pathsplit = filepath.split('/')
    filesplit = pathsplit[-1].split('.')
    newfile = "{}/{}_{}.{}".format(
            output_folder,
            '.'.join(filesplit[:-1]),
            classification['class'],
            filesplit[-1])
    bboxstr = "{2}x{3}+{0}+{1}".format(*[int(i) for i in classification['bbox']])
    command = "convert {} -crop {} {}".format(filepath, bboxstr, newfile)
    if verbose:
        print command
    os.system(command)
    return newfile


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

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
    parser.add_argument("--cropped_folder",
                        help="Folder (including path, full or relative) "
                             "in which to store the cropped images Sherlock workflow "
                             "specification.", required=True,
                        type=str)
    parser.add_argument("-v", "--verbose", help="Verbose mode.", action="store_true", default=0)

    args = parser.parse_args()
    print args

    verbose = args.verbose

    data = json.load(args.json_input_file)

    # os.mkdir(args.cropped_folder)
    
    for classification in data['classifications']:
        if classification['probability'] > 0.5:
            classification['cropped_file'] = crop(classification, args.cropped_folder)
        
    if verbose:
        print(json.dumps(data, indent=4))

    json.dump(data, args.workflow_out, indent=4, sort_keys=True)
