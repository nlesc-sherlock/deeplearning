# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 15:35:55 2017

@author: elena
"""
import argparse
import json

def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_json_fname', 
                        help="The filename (including path, full or relative) "
                             "of the json file comes out of the processing pipeline",
                        type=argparse.FileType('r'))
    parser.add_argument('output_json_fname', 
                        help="The filename (including path, full or relative) "
                             "of the json file to be generated by this converter",
                        type=argparse.FileType('w'))
    return parser     
    
def main():
    # parse the input arguments
    parser= argument_parser()
    args = parser.parse_args()
    
    # load the input (pipeline output) json file
    input_json = json.load(args.input_json_fname)
    
    # get all filenames
    fnames = input_json['files']  
    
    # output json
    output_json =dict()
    for f in fnames:
        output_json[f] = []
        output_json_pp = json.dumps(output_json, indent=4)
    print("Output JSON: {}".format(output_json_pp))
    
    json.dump(output_json, args.output_json_fname, indent=4)
    
    
    
if __name__ == "__main__"    :
    main()
    