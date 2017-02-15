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
                             "of the appended json file",
                        type=argparse.FileType('w'))
    return parser     
    
    
def append_images_key(input_json):
    output_json = input_json    
    output_json['images'] = {}
    
    return output_json
    
def append_imagesfnames_keys(input_json):

    # get all filenames
    fnames = input_json['files'] 

    output_json = input_json    
    images_json ={}
    for f in fnames:
        images_json[f] = []        
    output_json['images']= images_json   
    return output_json
    
    
def main():
    # parse the input arguments
    parser= argument_parser()
    args = parser.parse_args()
    
    # load the input (pipeline output) json file
    input_json = json.load(args.input_json_fname)
    
    output_json = append_images_key(input_json)
    output_json = append_imagesfnames_keys(output_json)
       
    # outputting
    output_json_pp = json.dumps(output_json, indent=4)
    print("Output JSON: {}".format(output_json_pp))
    
    json.dump(output_json, args.output_json_fname, indent=4)
    
        
if __name__ == "__main__"    :
    main()
    