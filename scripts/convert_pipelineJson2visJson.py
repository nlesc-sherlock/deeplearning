# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 15:35:55 2017

@author: elena
"""
import argparse
import json

def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_json_fname')
    
    return parser 
    

def load_json_file(filename):
    
    with open(filename) as fp:
        json_data = json.load(fp)

    return json_data
    
def main():
    # parse the input arguments
    parser= argument_parser()
    args = parser.parse_args()
    
    # load the input (pipeline output) json file
    input_json = load_json_file(args.input_json_fname)
    
    # pretty print the json data
    print json.dumps(input_json, indent=4, sort_keys = True)
    
if __name__ == "__main__"    :
    main()
    