#!/usr/bin/env python

import numpy as np
# import matplotlib.pyplot as plt
import os
import json
from datetime import datetime
import crablip

os.environ['GLOG_minloglevel'] = '2' # Surpress a lot of building messages
import caffe

# fix mysterious error for some files (https://github.com/BVLC/caffe/issues/438)
# import skimage; skimage.io.use_plugin('matplotlib')
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


def softmax(w, t=1.0):
    e = np.exp(np.array(w) / t)
    distribution = e / np.sum(e)
    return distribution


def get_channel_mean(mean_pixel_file):
    proto_data = open(mean_pixel_file, "rb").read()
    a = caffe.io.caffe_pb2.BlobProto.FromString(proto_data)
    mean = caffe.io.blobproto_to_array(a)[0]
    channel_mean = mean.mean(axis=(1, 2))
    return channel_mean


def classify(image_files, model_path, model_name, model_deploy='deploy.prototxt',
             mean_pixel_name='mean.binaryproto',
             gray_range=255, channel_swap=(2, 1, 0), batch_size=0,
             gpu_id=-1, verbose=False):
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
        input_images.append(caffe.io.load_image(image_file))

    # batch process the images:
    if verbose:
        print "Predicting the category classes of the image(s)..."
    prediction = net.predict(input_images, oversample=False)

    # convert to probabilities (if needed):
    probs = []

    for ix, image_file in enumerate(image_files):
        if prediction[ix].sum() == 1 and np.all(prediction[ix] > 0):
            probs.append(prediction[ix])
        else:
            probs.append(softmax(prediction[ix]))

    return probs


def get_labels_from_file(labels_filename):
    with open(labels_filename, 'r') as fp:
        labels = fp.readlines()
    return labels


def print_classification(probs, image_files, model_path, labels_name='labels.txt'):
    labels_file = os.path.join(model_path, labels_name)
    labels = get_labels_from_file(labels_file)

    ind = min(len(labels), 5)

    for ix, image_file in enumerate(image_files):
        print 'Predicted class & probabilities (top) for image ' + image_file + ":"
        ix_topN = probs[ix].argsort()[::-1][:ind]
        topN_labels = [labels[ix] for ix in ix_topN]
        topN_classes = zip(topN_labels, probs[ix][ix_topN])
        print(topN_classes)
        print("")


def print_json_classification(probs, image_files, model_path, model_name,
                              labels_name, mean_pixel_name, model_deploy,
                              gray_range, channel_swap, batch_size, outfile):
    """
        Print a json representation of the classification result
    """
    labels_file = os.path.join(model_path, labels_name)
    labels = get_labels_from_file(labels_file)

    data = {
        "type": "classification",
        "script": "cnn_classify.py",
        "datetime": datetime.now().isoformat(),
        "parameters": {
            "model_path": model_path,
            "model_name": model_name,
            "model_deploy": model_deploy,
            "labels_name": labels_name,
            "mean_pixel_name": mean_pixel_name,
            "gray_range": gray_range,
            "channel_swap": channel_swap,
            "batch_size": batch_size
        },
        "predictions": {}
    }

    ind = min(len(labels), 5)

    for ix, image_file in enumerate(image_files):
        ix_topN = probs[ix].argsort()[::-1][:ind]
        # need pure python floats for json.dumps serialization:
        topN_probs = [float(p) for p in probs[ix][ix_topN]]
        topN_labels = [labels[ix] for ix in ix_topN]
        topN_classes = zip(topN_labels, topN_probs)
        # tags = "%s" % dict(topN_classes)
        tags = dict(topN_classes)
        data["predictions"][image_file] = {
            "tags": tags
        }

    json_string = json.dumps(data, sort_keys=True, indent=4, ensure_ascii=False)
    outfile.write(json_string)


def run(image_files, model_path, model_name, model_deploy,
        labels_name, mean_pixel_name, outfile,
        gray_range=255, channel_swap=(2, 1, 0), batch_size=0, gpu_id=-1,
        verbose=False, json=False):
    probs = classify(image_files, model_path, model_name,
                     model_deploy=model_deploy, mean_pixel_name=mean_pixel_name,
                     gray_range=gray_range, channel_swap=channel_swap,
                     batch_size=batch_size, gpu_id=gpu_id, verbose=verbose)
    if json:
        print_json_classification(probs, image_files, model_path=model_path,
                                  labels_name=labels_name,
                                  model_name=model_name,
                                  mean_pixel_name=mean_pixel_name,
                                  model_deploy=model_deploy,
                                  gray_range=gray_range,
                                  channel_swap=channel_swap,
                                  batch_size=batch_size, outfile=outfile)
    else:
        print_classification(probs, image_files, model_path, labels_name=labels_name)


if __name__ == '__main__':
    parser = crablip.get_default_argument_parser()

    # The default mode for the cnn_classify script is to give it filenames of
    # images. This can be changed in derivative scripts by importing
    # cnn_classify and defining a different argument, e.g. a JSON file.
    parser.add_argument("image_files", help="The filename(s) (including path, full or relative) of the image(s) you want to classify.", nargs="+")

    args = parser.parse_args()
    print args

    data_path = args.data_path
    image_filenames = [os.path.join(data_path, image_file) for image_file in args.image_files]

    run(image_filenames, args.model_path, args.model_snapshot,
        model_deploy=args.model_deploy, labels_name=args.model_labels,
        mean_pixel_name=args.mean_pixel_name, gray_range=args.gray_range,
        channel_swap=args.channel_swap, batch_size=args.batch_size,
        gpu_id=args.gpu_id, verbose=args.verbose, json=args.json,
        outfile=args.outfile)
