#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import sys
import caffe
import os
from datetime import datetime
import json
from string import join

# fix mysterious error for some files (https://github.com/BVLC/caffe/issues/438)
from skimage import io; io.use_plugin('matplotlib')
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

def softmax(w, t = 1.0):
    e = np.exp(np.array(w) / t)
    distribution = e / np.sum(e)
    return distribution


def get_channel_mean(mean_pixel_file):
    proto_data = open(mean_pixel_file, "rb").read()
    a = caffe.io.caffe_pb2.BlobProto.FromString(proto_data)
    mean  = caffe.io.blobproto_to_array(a)[0]
    channel_mean = mean.mean(axis=(1,2))
    return channel_mean


def classify(image_files, model_path, model_name, model_deploy='deploy.prototxt',
         mean_pixel_name='mean.binaryproto',
         gray_range=255, channel_swap=(2,1,0), batch_size=0, gpu_id=-1, verbose=False):
    # paths
    model_configuration = os.path.join(model_path, model_deploy)
    model = os.path.join(model_path, model_name)
    mean_pixel_file = os.path.join(model_path, mean_pixel_name)

    if verbose:
        print "Model used: " + model

    # other stuff
    if verbose:
        print "Getting the mean channel pixel values..."
    channel_mean = get_channel_mean(mean_pixel_file)

    # CPU or GPU mode
    if gpu_id < 0:
        caffe.set_mode_cpu()
        if verbose:
            print "Caffe is running in CPU mode!"
    else:
        caffe.set_mode_gpu()
        caffe.set_device(gpu_id)
        if verbose:
            print "Caffe is running in GPU mode!"

    if verbose:
        print "Building a CNN classifier..."
    net = caffe.Classifier(model_configuration, model, mean=channel_mean,
                           channel_swap=channel_swap, raw_scale=gray_range)
    image_x, image_y = net.blobs['data'].data.shape[-2:]
    channels = net.blobs['data'].data.shape[1]
    if batch_size == 0:
        # batch_size = net.blobs['data'].data.shape[0]
        batch_size = len(image_files)
    if verbose:
        print "Reshaping the data..."
        print "batch size: ", batch_size
        print "number of channels: ", channels
        print "data shape: ", image_x, image_y


    net.blobs['data'].reshape(batch_size, channels, image_x, image_y)

    if verbose:
        print "Loading image(s) to classify..."
    input_images = []
    for image_file in image_files:
        print image_file
        input_images.append(caffe.io.load_image(image_file))

    # batch process the images:
    if verbose:
        print "Predicting the category classes of the image(s)..."
    prediction = net.predict(input_images)
    #out = net.forward()



    #flattend = net.blobs['prob'].data[0].flatten()
        #flattend.sort()
        #print "From within the net: "
        #print flattend[-1:-6:-1]



    # convert to probabilities (if needed):
    probs = []
        #probs = net.blobs['prob'].data[0].flatten()
        #probs.sort()

    for ix, image_file in enumerate(image_files):
        if prediction[ix].sum() == 1 and np.all(prediction[ix] > 0):
            probs.append(prediction[ix])
        else:
            probs.append(softmax(prediction[ix]))

    return probs


def print_classification(probs, image_files, model_path, labels_name='labels.txt'):
    labels_file = os.path.join(model_path, labels_name)
    labels = np.loadtxt(labels_file, str)

    for ix, image_file in enumerate(image_files):
        print 'Predicted class & probabilities (top 5) for image ' + image_file + ":"
        print(zip(labels[probs[ix].argsort()[:-6:-1]], probs[ix][probs[ix].argsort()[:-6:-1]]))
        print("")

def print_json_classification(probs, image_files, model_path, model_name,
        labels_name, mean_pixel_name, model_deploy,
        gray_range, channel_swap, batch_size):
    """
        Print a json representation of the classification result
    """
    labels_file = os.path.join(model_path, labels_name)
    labels = np.loadtxt(labels_file, str)

    data = {
        "type" : "classification",
        "script" : "cnn_classify.py",
        "datetime" : datetime.now().isoformat(),
        "parameters": {
            "model_path": model_path,
            "model_name": model_name,
            "model_deploy": model_deploy,
            "labels_name": labels_name,
            "mean_pixel_name": mean_pixel_name,
            "gray_range": gray_range,
            "channel_swap": channel_swap,
            "batch_size": batch_size
        }
    }

    for ix, image_file in enumerate(image_files):
        tags = "%s" % dict(zip(labels[probs[ix].argsort()[:-6:-1]], probs[ix][probs[ix].argsort()[:-6:-1]]))
        data[image_file] = {
            "tags" : tags
        }
    print json.dumps(data, sort_keys=True, indent=4)

def run(image_files, model_path, model_name, model_deploy,
    labels_name, mean_pixel_name,
    gray_range=255, channel_swap=(2,1,0), batch_size=0, gpu_id=-1, verbose=False, json=False):
    probs = classify(image_files, model_path, model_name, model_deploy=model_deploy,
             mean_pixel_name=mean_pixel_name,
             gray_range=gray_range, channel_swap=channel_swap, batch_size=batch_size,
             gpu_id=gpu_id, verbose=verbose)
    if json:
        print_json_classification(probs, image_files, model_path=model_path, labels_name=labels_name,
            model_name=model_name, mean_pixel_name=mean_pixel_name, model_deploy=model_deploy,
            gray_range=gray_range, channel_swap=channel_swap, batch_size=batch_size)
    else:
        print_classification(probs, image_files, model_path, labels_name=labels_name)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("image_files", help="The filename(s) (including path, full or relative) of the image(s) you want to classify.", nargs="+")

    # model file parameters
    parser.add_argument("-M", "--model_path", help="Model files directory. Should contain the files: snapshot.caffemodel, deploy.prototxt and labels.txt. Any files with other filenames can be given with other parameters (see below).", required=True)
    parser.add_argument("-D", "--data_path", help="Directory path of where the data is mounted. If this script is running whithin a docker it should be the docker local path", default="/data")
    model_group = parser.add_argument_group(title="Model file names.", description="Override the default filenames of the model.")
    model_group.add_argument("--model_snapshot", help="The filename of the caffemodel snapshot in the model directory.", default='snapshot.caffemodel')
    model_group.add_argument("--model_deploy", help="The filename of the deploy file in the model directory.", default='deploy.prototxt')
    model_group.add_argument("--model_labels", help="The filename of the labels file in the model directory.", default='labels.txt')
    model_group.add_argument("--mean_pixel_name", help="Mean pixel file name of the trained model (default: mean.binaryproto).", default='mean.binaryproto')

    output_group = parser.add_argument_group(title="Output format.", description="Define the output format.")
    output_group.add_argument("--json", help="Output json format",action="store_true", default=0)

    parser.add_argument("--gray_range", help="Gray range of the images (default: 255).", type=int, default=255)
    parser.add_argument("--channel_swap", help="Use numbers 0, 1 and 2 to give the order of the color-channels that the model used, for instance 0 1 2 for RGB. Some models swap the channels from RGB to BGR (this is the default: 2 1 0).", nargs=3, default=[2,1,0])
    parser.add_argument("--batch_size", help="Number of images processed simultaneously. Default: taken from model configuration.", type=int, default=0)
    parser.add_argument("--gpu_id", help="To use GPU mode, specify the gpu_id that you want to use. Default: CPU mode (-1).", type=int, default=-1)
    parser.add_argument("-v", "--verbose", help="Verbose mode.", action="store_true", default=0)

    args = parser.parse_args()

    data_path = args.data_path
    image_filenames = [os.path.join(data_path, image_file) for image_file in args.image_files]

    run(image_filenames, args.model_path, args.model_snapshot,
        model_deploy=args.model_deploy, labels_name=args.model_labels,
        mean_pixel_name=args.mean_pixel_name, gray_range=args.gray_range,
        channel_swap=args.channel_swap, batch_size=args.batch_size, gpu_id=args.gpu_id, verbose=args.verbose, json=args.json)
