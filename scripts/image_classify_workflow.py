#!/usr/bin/env python

from __future__ import print_function

import docker
import json
import argparse
import os
import sys
import subprocess
import distutils.dir_util as dirutil
import shutil

from utils.pathtype import PathType

def check_input(inputfile):
    stats = os.stat(inputfile)
    if stats.st_size > 0:
        return True
    else:
        return False

def create_volume_string(volumes):
    new_string = ""
    for key, volume in volumes.iteritems():
        new_string += "-v " + volume['path'] + ":" + volume['bind'] + " "
    return new_string


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


def run_ssd_detection(client, input_json, output_json, volumes, verbose):
    # Cannot use the docker client unfortunately, have to use nvidia-docker as a command line
    # client.containers.run('nlescsherlockdl/object_detect_ssdnet_wrapper', volumes=volumes, command=["input_json"])
    extra_params = " "
    if verbose:
        extra_params += "-v "

    command = "nvidia-docker run " + create_volume_string(volumes)  + " nlescsherlockdl/object_detect_ssdnet_wrapper_coco " + \
              " --workflow_out " + output_json + extra_params + input_json
    #print("Command: ", command)
    subprocess.call(command, shell=True)


def run_cropper_after_face_detection(client, input_json, output_json, volumes):
    probability = "0.1"

    command = "docker run " + create_volume_string(volumes)  + " nlescsherlockdl/cropper:old" + \
              " --workflow_out " + output_json + " --cropped_folder " + volumes['cropped']['bind'] + " -p " + probability + " --specialised " + input_json
    print("Command: ", command)
    subprocess.call(command, shell=True)


def run_cropper_after_ssd(client, input_json, output_json, volumes, verbose=False):
    probability = "0.1"

#    client.containers.run('nlescsherlockdl/cropper', volumes=volumes, command=["--wokflow_out", output_json, "--cropped_folder", cropdir, \
#                                                                               "-p", probability, "input_json"])
    command = "docker run " + create_volume_string(volumes)  + " nlescsherlockdl/cropper:old " \
              " --workflow_out " + output_json + " --cropped_folder " + volumes['cropped']['bind'] + " -p " + probability + " " + input_json
    if verbose:
        print("Command: ", command)
    subprocess.call(command, shell=True)


def run_cnn_classify(client, input_json, output_json, volumes, docker_image):
    # Cannot use the docker client unfortunately, have to use nvidia-docker as a command line
    command = "nvidia-docker run " + create_volume_string(volumes) + docker_image + \
              " --workflow_out " + output_json + " " + input_json
    print("Command: ", command)
    subprocess.call(command, shell=True)


def run_face_detection(client, input_json, output_json, volumes, docker_image):
    command = "nvidia-docker run " + create_volume_string(volumes)  + " nlescsherlockdl/face_detector_workflow_minimal " + \
          " --workflow_out " + output_json + " " + input_json
    print("Command: ", command)
    subprocess.call(command, shell=True)


if __name__ == "__main__":
    print("***************************************************\n"
          "*                                                 *\n"
          "*  Welcome to the image classification workflow.  *\n"
          "*        This version is a python script.         *\n"
          "*                                                 *\n"
          "***************************************************\n\n")
    print("Now parsing arguments.....", end="")
    sys.stdout.flush()
    parser = argparse.ArgumentParser()

    pathtype = PathType(exists=True, type='dir', dash_ok=False, abs=True)

    parser.add_argument("input_directory", type=pathtype)
    parser.add_argument("output_directory", type=pathtype)
    parser.add_argument("temp_directory", type=pathtype)

    parser.add_argument("-v", "--verbose", help="Verbose mode.", action="store_true", default=0) 

    args = parser.parse_args()
    
    inputdir = args.input_directory
    outputdir = args.output_directory
    tmpdir = args.temp_directory

    verbose = args.verbose

    print("done.")
    #print("Arguments found:", args)
    print("\n\n")

    print("Now setting up the docker environment..", end="")
    sys.stdout.flush()
    docker_images = [
        'nlescsherlockdl/object_detect_ssdnet_wrapper_coco',
        'nlescsherlockdl/cropper',
        'nlescsherlockdl/car_color_workflow',
        'nlescsherlockdl/car_model_workflow',
        'nlescsherlockdl/face_detector_workflow_minimal',
        'nlescsherlockdl/person_face_gender_workflow',
        'nlescsherlockdl/person_face_age_workflow',
    ]
    client = docker.from_env()
    
#    for image in docker_images:
#        print(".", end="")
#        client.images.pull(image)

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
        },
        'cropped': {
            'path': os.path.join(tmpdir, 'cropped'),
            'bind': '/cropped'
        }
    }
    print("done.\n\n")

    print("Now searching for files in input directory...", end="")
    sys.stdout.flush()
    input_json = os.path.join(tmpdir, "files.json")
    with file(input_json, 'w') as outfile:
        generate_json_from_directory(inputdir, outfile, volumes)
    print("done.")
    print("Input filepaths written to: ", input_json, "\n\n")


    print("Now running object detection...", end="")
    sys.stdout.flush()
    input_json = os.path.join(volumes['temp']['bind'], "files.json")
    input_file = os.path.join(volumes['temp']['path'], "files.json")
    output_json = os.path.join(volumes['temp']['bind'], "detect.json")
    if check_input(input_file):
        run_ssd_detection(client, input_json, output_json, volumes, verbose)
    else:
        raise Exception("Input file " + input_file + " was empty")
    print("done.")

    print("Now running cropping...", end="")
    sys.stdout.flush()
    input_json  = os.path.join(volumes['temp']['bind'], "detect.json")
    input_file = os.path.join(volumes['temp']['path'], "detect.json")
    output_json = os.path.join(volumes['temp']['bind'], "cropped.json")
    if check_input(input_file):
        run_cropper_after_ssd(client, input_json, output_json, volumes, verbose=verbose)
    else:
        raise Exception("Input file " + input_file + " was empty")
    print("done.")

    print("Now running car color classification...", end="")
    sys.stdout.flush()
    input_json  = os.path.join(volumes['temp']['bind'], "cropped.json")
    input_file = os.path.join(volumes['temp']['path'], "cropped.json")
    output_json = os.path.join(volumes['temp']['bind'], "colored.json")

    docker_image = 'nlescsherlockdl/car_color_workflow'
    if check_input(input_file):
        run_cnn_classify(client, input_json, output_json, volumes, docker_image)
    else:
        raise Exception("Input file " + input_file + " was empty")
    print("done.")
    
    
    print("Now running car model classification...", end="")
    sys.stdout.flush()
    input_json  = os.path.join(volumes['temp']['bind'], "colored.json")
    input_file = os.path.join(volumes['temp']['path'], "colored.json")
    output_json = os.path.join(volumes['temp']['bind'], "model.json")

    docker_image = 'nlescsherlockdl/car_model_workflow'
    if check_input(input_file):
        run_cnn_classify(client, input_json, output_json, volumes, docker_image)
    else:
        raise Exception("Input file " + input_file + " was empty")
    print("done.")

    print("Now running face detection...", end="")
    sys.stdout.flush()
    input_json  = os.path.join(volumes['temp']['bind'], "model.json")
    input_file = os.path.join(volumes['temp']['path'], "model.json")
    output_json = os.path.join(volumes['temp']['bind'], "faces.json")

    if check_input(input_file):
        run_face_detection(client, input_json, output_json, volumes, docker_image)
    else:
        raise Exception("Input file " + input_file + " was empty")
    print("done.")

    print("Now running cropping...", end="")
    sys.stdout.flush()
    input_json  = os.path.join(volumes['temp']['bind'], "faces.json")
    input_file = os.path.join(volumes['temp']['path'], "faces.json")
    output_json = os.path.join(volumes['temp']['bind'], "faces_cropped.json")
    if check_input(input_file):
        run_cropper_after_face_detection(client, input_json, output_json, volumes)
    else:
        raise Exception("Input file " + input_file + " was empty")
    print("done.")


    print("Now running gender classification...", end="")
    sys.stdout.flush()
    input_json  = os.path.join(volumes['temp']['bind'], "faces_cropped.json")
    input_file = os.path.join(volumes['temp']['path'], "faces_cropped.json")
    output_json = os.path.join(volumes['temp']['bind'], "gender.json")

    docker_image = 'nlescsherlockdl/person_face_gender_workflow'
    if check_input(input_file):
        run_cnn_classify(client, input_json, output_json, volumes, docker_image)
    else:
        raise Exception("Input file " + input_file + " was empty")
    print("done.")

    print("Now running gender classification...", end="")
    sys.stdout.flush()
    input_json  = os.path.join(volumes['temp']['bind'], "gender.json")
    input_file = os.path.join(volumes['temp']['path'], "gender.json")
    output_json = os.path.join(volumes['temp']['bind'], "age.json")

    docker_image = 'nlescsherlockdl/person_face_age_workflow'
    if check_input(input_file):
        run_cnn_classify(client, input_json, output_json, volumes, docker_image)
    else:
        raise Exception("Input file " + input_file + " was empty")
    print("done.")

    print("Copying results to output...", end="")
    sys.stdout.flush()

    output_json = os.path.join(tmpdir, "age.json")
    tmpdest = os.path.join(outputdir, os.path.basename(os.path.normpath(volumes['cropped']['path'])))
    shutil.copy(output_json, outputdir)
    dirutil.copy_tree(volumes['cropped']['path'], tmpdest)
    print("done.")
