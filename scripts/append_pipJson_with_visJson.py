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
    parser.add_argument('-verbose',
                        help="Verbose mode", action='store_true')                    
    return parser     
    
    
def append_images_key(input_json):
    # appends 'images' json object
    output_json = input_json    
    output_json['images'] = {}
    
    return output_json
    
def append_imagesfnames_keys(input_json):
    # appends the filenames keys under 'images'
    output_json = input_json

    # get all filenames
    fnames = input_json['files'] 
        
    images_json = dict()
    for f in fnames:
        images_json[f] = {}        
    output_json['images']= images_json   
    
    return output_json
    
def append_objects_key(input_json):
    # appends 'objects' key under each filename of 'images'
    output_json = input_json 
    images_json = output_json['images']
    
    for fnames_key in images_json.keys():
        images_json[fnames_key]['objects'] = {}
        
    output_json['images']= images_json    
    
    return output_json
    
#def copy_classification(obj_)     
    
def append_objects(input_json, args):    
    # appends the actual detected objects under the 'objects' key for each filename
    output_json = input_json 
    images_json = output_json['images']
    classes_json = input_json['classes']
    
    for fname in images_json.keys():
        for obj in classes_json.keys():
            # find out which objects were detected in which image
            obj_list = classes_json[obj]
            for o in obj_list:
                if o['path'] == fname:
                    if args.verbose:
                        print("In file '{}' top object '{}' has been detected!".format(fname, obj))
                    
                    if o.has_key('classification'):
                        obj_info = { 'probabiliity': o['probability'], 'bbox': o['bbox'], 'classification':o['classification']}
                    else:
                        obj_info = { 'probabiliity': o['probability'], 'bbox': o['bbox'] }
                    images_json[fname]['objects'][obj] = obj_info
                                        
    output_json['images']= images_json    
    
    return output_json
    
    
    
def main():
    # parse the input arguments
    parser= argument_parser()
    args = parser.parse_args()
    
    # load the input (pipeline output) json file
    input_json = json.load(args.input_json_fname)
    
    # appending json object suited better for visualization
    output_json = append_images_key(input_json)
    output_json = append_imagesfnames_keys(output_json)
    output_json = append_objects_key(output_json)  
    output_json = append_objects(output_json, args)
    
    # outputting
    output_json_pp = json.dumps(output_json, indent=4)
    if args.verbose:
        print("Output JSON: {}".format(output_json_pp))
    
    json.dump(output_json, args.output_json_fname, indent=4)
    
        
if __name__ == "__main__"    :
    main()
    