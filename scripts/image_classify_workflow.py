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


def run_ssd_detection(client, input_json, output_json, volumes):
    # Cannot use the docker client unfortunately, have to use nvidia-docker as a command line
    # client.containers.run('nlescsherlockdl/object_detect_ssdnet_wrapper', volumes=volumes, command=["input_json"])
    command = "nvidia-docker run " + create_volume_string(volumes)  + " nlescsherlockdl/object_detect_ssdnet_wrapper " + \
              " --workflow_out " + output_json + " " + input_json
    #print("Command: ", command)
    subprocess.call(command, shell=True)


def run_cropper_after_face_detection(client, input_json, output_json, volumes):
    probability = "0.1"

    command = "docker run " + create_volume_string(volumes)  + " nlescsherlockdl/cropper" + \
              " --workflow_out " + output_json + " --cropped_folder " + volumes['cropped']['bind'] + " -p " + probability + " --specialised " + input_json
    print("Command: ", command)
    subprocess.call(command, shell=True)


def run_cropper_after_ssd(client, input_json, output_json, volumes):
    probability = "0.1"

#    client.containers.run('nlescsherlockdl/cropper', volumes=volumes, command=["--wokflow_out", output_json, "--cropped_folder", cropdir, \
#                                                                               "-p", probability, "input_json"])
    command = "docker run " + create_volume_string(volumes)  + " nlescsherlockdl/cropper" + \
              " --workflow_out " + output_json + " --cropped_folder " + volumes['cropped']['bind'] + " -p " + probability + " " + input_json
#    print("Command: ", command)
    subprocess.call(command, shell=True)


def run_cnn_classify(client, input_json, output_json, volumes, docker_image):
    # Cannot use the docker client unfortunately, have to use nvidia-docker as a command line
    command = "nvidia-docker run " + create_volume_string(volumes) + docker_image + \
              " --workflow_out " + output_json + " " + input_json
    #print("Command: ", command)
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

    args = parser.parse_args()
    
    inputdir = args.input_directory
    outputdir = args.output_directory
    tmpdir = args.temp_directory
    print("done.")
    #print("Arguments found:", args)
    print("\n\n")

    print("Now setting up the docker environment..", end="")
    sys.stdout.flush()
    docker_images = [
        'nlescsherlockdl/object_detect_ssdnet_wrapper',
        'nlescsherlockdl/cropper',
        'nlescsherlockdl/car_color_workflow',
        'nlescsherlockdl/car_model_workflow',
        'nlescsherlockdl/face_detector_workflow_minimal',
        'nlescsherlockdl/person_face_gender_workflow',
        'nlescsherlockdl/person_face_age_workflow',
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
    output_json = os.path.join(volumes['temp']['bind'], "detect.json")
    run_ssd_detection(client, input_json, output_json, volumes)
    print("done.")

    print("Now running cropping...", end="")
    sys.stdout.flush()
    input_json  = os.path.join(volumes['temp']['bind'], "detect.json")
    output_json = os.path.join(volumes['temp']['bind'], "cropped.json")
    run_cropper_after_ssd(client, input_json, output_json, volumes)
    print("done.")

    print("Now running car color classification...", end="")
    sys.stdout.flush()
    input_json  = os.path.join(volumes['temp']['bind'], "cropped.json")
    output_json = os.path.join(volumes['temp']['bind'], "colored.json")

    docker_image = 'nlescsherlockdl/car_color_workflow'
    run_cnn_classify(client, input_json, output_json, volumes, docker_image)
    print("done.")
    
    
    print("Now running car model classification...", end="")
    sys.stdout.flush()
    input_json  = os.path.join(volumes['temp']['bind'], "colored.json")
    output_json = os.path.join(volumes['temp']['bind'], "model.json")

    docker_image = 'nlescsherlockdl/car_model_workflow'
    run_cnn_classify(client, input_json, output_json, volumes, docker_image)
    print("done.")

    print("Now running face detection...", end="")
    sys.stdout.flush()
    input_json  = os.path.join(volumes['temp']['bind'], "model.json")
    output_json = os.path.join(volumes['temp']['bind'], "faces.json")

    run_face_detection(client, input_json, output_json, volumes, docker_image)
    print("done.")

    print("Now running cropping...", end="")
    sys.stdout.flush()
    input_json  = os.path.join(volumes['temp']['bind'], "faces.json")
    output_json = os.path.join(volumes['temp']['bind'], "faces_cropped.json")
    run_cropper_after_face_detection(client, input_json, output_json, volumes)
    print("done.")


    print("Now running gender classification...", end="")
    sys.stdout.flush()
    input_json  = os.path.join(volumes['temp']['bind'], "faces_cropped.json")
    output_json = os.path.join(volumes['temp']['bind'], "gender.json")

    docker_image = 'nlescsherlockdl/person_face_gender_workflow'
    run_cnn_classify(client, input_json, output_json, volumes, docker_image)
    print("done.")

    print("Now running gender classification...", end="")
    sys.stdout.flush()
    input_json  = os.path.join(volumes['temp']['bind'], "gender.json")
    output_json = os.path.join(volumes['temp']['bind'], "age.json")

    docker_image = 'nlescsherlockdl/person_face_age_workflow'
    run_cnn_classify(client, input_json, output_json, volumes, docker_image)
    print("done.")

    print("Copying results to output...", end="")
    sys.stdout.flush()

    output_json = os.path.join(tmpdir, "age.json")
    tmpdest = os.path.join(outputdir, os.path.basename(os.path.normpath(volumes['cropped']['path'])))
    shutil.copy(output_json, outputdir)
    dirutil.copy_tree(volumes['cropped']['path'], tmpdest)
    print("done.")
