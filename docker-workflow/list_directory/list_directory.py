#!/usr/bin/env python

import json
import argparse
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("input_directory",
                        help="The directory (including path, full or relative) "
                             "of the json files for the input")
    parser.add_argument("--workflow_out",
                        help="Filename (including path, full or relative) "
                             "of the output json file in the Sherlock workflow "
                             "specification.", required=True,
                        type=argparse.FileType('w'))
    parser.add_argument("-v", "--verbose", help="Verbose mode.", action="store_true", default=0)

    args = parser.parse_args()
    
    if args.verbose:
        print args

    files_json = {
        "files": []
    }

    for _root, dirs, files in os.walk(args.input_directory, topdown=False):
        for name in files:
            if name.endswith('.jpg') or name.endswith('.png'):
                filepath = os.path.relpath(os.path.join(_root, name))
                files_json["files"].append(filepath)

    json.dump(files_json, args.workflow_out, indent=4, sort_keys=True)