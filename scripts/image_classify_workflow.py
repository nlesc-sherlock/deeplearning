#!/usr/bin/env python

from __future__ import print_function

import docker
import json
import argparse
import os
import subprocess

from utils.pathtype import PathType

def generate_json_from_directory(directory, outfile, volumes):
    files_json = {
        "files": []
    }
    for _root, dirs, files in os.walk(directory, topdown=False):
        for name in files:
            if name.endswith('.jpg') or name.endswith('.png'):
                filepath = os.path.join(volumes['input']['bind'],os.path.relpath(os.path.join(_root, name), volumes['input']['path']))
                files_json["files"].append(filepath)

    json.dump(files_json, outfile, indent=4, sort_keys=True)


def run_ssd_detection(client, input_json, output_json, volumes):
    # Cannot use the docker client unfortunately, have to use nvidia-docker as a command line
    # client.containers.run('nlescsherlockdl/object_detect_ssdnet_wrapper', volumes=volumes, command=["input_json"])
    indir = volumes['input']['path']+":"+volumes['input']['bind']
    outdir = volumes['output']['path']+":"+volumes['output']['bind']
    tmpdir = volumes['temp']['path']+":"+volumes['temp']['bind']
    command = "nvidia-docker run" + " -v " + indir + " -v " + outdir + " -v " + tmpdir + " nlescsherlockdl/object_detect_ssdnet_wrapper " + \
              " --workflow_out " + output_json + " " + input_json
    print("Command: ", command)
    subprocess.call(command, shell=True)


if __name__ == "__main__":
    print("**************************************************\n"
          "*                                                *\n"
          "*  Welcome to the image classification workflow  *\n"
          "*  this verion isimplemented by a python script. *\n"
          "*                                                *\n"
          "**************************************************\n\n")
    print("Now parsing arguments.....", end="")
    parser = argparse.ArgumentParser()

    pathtype = PathType(exists=True, type='dir', dash_ok=False, abs=True)

    parser.add_argument("input_directory", type=pathtype)
    parser.add_argument("output_directory", type=pathtype)
    parser.add_argument("temp_directory", type=pathtype)

    args = parser.parse_args()
    
    inputdir = args.input_directory
    outputdir = args.output_directory
    tmpdir = args.temp_directory
    print("done.")
    print("Arguments found:", args)
    print("\n\n")

    print("Now setting up the docker environment..", end="")
    docker_images = [
        'nlescsherlockdl/object_detect_ssdnet_wrapper'
    ]
    client = docker.from_env()
    
    for image in docker_images:
        print(".", end="")
        client.images.pull(image)

    volumes = {
        'input': {
            'path': inputdir,
            'bind': '/data'
        },
        'output': {
            'path': outputdir,
            'bind': '/out'
        },
        'temp': {
            'path': tmpdir,
            'bind': '/temp'
        }
    }
    volumes[inputdir] = {'bind': '/data', 'mode': 'rw'}
    volumes[outputdir] = {'bind': '/out', 'mode': 'rw'}
    volumes[tmpdir] = {'bind': '/temp', 'mode': 'rw'}
    print("done.\n\n")


    print("Now searching for files in input directory...", end="")
    input_json = os.path.join(tmpdir, "files.json")
    with file(input_json, 'w') as outfile:
        generate_json_from_directory(inputdir, outfile, volumes)
    print("done.")
    print("Input filepaths written to: ", input_json, "\n\n")

    print("Now running object detection...", end="")
    input_json = os.path.join(volumes['temp']['bind'], "files.json")
    output_json = os.path.join(volumes['temp']['bind'], "detect.json")
    run_ssd_detection(client, input_json, output_json, volumes)
    print("done.")

