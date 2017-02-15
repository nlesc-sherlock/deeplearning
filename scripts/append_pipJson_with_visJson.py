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
    
    
def make_images_section(input_json):
    # appends 'images' json object
    output_json = input_json    
    output_json['images'] = []
    
    return output_json
    
def fill_objects_section(input_json, args):
    # appends the filenames keys and 'obkects' under 'images'
    output_json = input_json

    # get all filenames
    fnames = input_json['files'] 
        
    images_json = []
    for f in fnames:
        images_json.append({ f:{'objects': make_objectlist(f, input_json, args)} })       
    output_json['images']= images_json   
        
    return output_json

#def find_ind_dict_list_of_dicts(lst, dict_key):
#    # finding the index of a dictionary with a dict_key key from a list of dictionaries  
#    for i, dic in enumerate(lst):
#        print "dictionary in the list: ", dic
#        if dic.has_key(dict_key):
#                print "dictionary in the list with the desired key: ", dic, dict_key
#                return i, dict
#    return -1, {}        
    

def make_objectlist(filename, input_json, args):
    objects_list = []
    
    classes_json = input_json['classes']
    
    for obj in classes_json.keys():
            # find out which objects were detected in which image
            obj_list = classes_json[obj]
            for o in obj_list:
                if o['path'] == filename:
                    if args.verbose:
                        print("In file '{}' top object '{}' has been detected!".format(filename, obj))
                    
                    if o.has_key('classification'):
                        obj_data = { 'probability': o['probability'], 'bbox': o['bbox'], 'classification':o['classification']}
                    else:
                        if o.has_key('face'):
                            person_face_obj = o['face'];
                            bbox_person = o['bbox']
                            bbox_face = person_face_obj['bbox']
                            abs_bbox_face = []
                            abs_bbox_face.append(bbox_person[0] + bbox_face[0])
                            abs_bbox_face.append(bbox_person[1] + bbox_face[1]) 
                            abs_bbox_face.append(bbox_face[2]) 
                            abs_bbox_face.append(bbox_face[3])
                            detail_obj = {'name': u'face', 'bbox': abs_bbox_face, 'classification':person_face_obj['classification']} 
                            obj_data = { 'probability': o['probability'], 'bbox': o['bbox'], 'detail':detail_obj}
                            #print obj_data
                        else:
                            obj_data = { 'probability': o['probability'], 'bbox': o['bbox'] }

    
    objects_list.append(obj_data)
    
    return objects_list    
    
    
def main():
    # parse the input arguments
    parser= argument_parser()
    args = parser.parse_args()
    
    # load the input (pipeline output) json file
    input_json = json.load(args.input_json_fname)
    
    # appending json object suited better for visualization
    output_json = make_images_section(input_json)
    output_json = fill_objects_section(output_json, args)
    
    # outputting
    output_json_pp = json.dumps(output_json, indent=4)
    if args.verbose:
        print("Output JSON: {}".format(output_json_pp))
    
    json.dump(output_json, args.output_json_fname, indent=4)
    
        
if __name__ == "__main__"    :
    main()
    