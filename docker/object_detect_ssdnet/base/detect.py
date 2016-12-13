#!/usr/bin/python

import numpy as np

# Make sure that caffe is on the python path:
caffe_root = '/opt/caffe/'
import os
os.chdir(caffe_root)
import sys
sys.path.insert(0, 'python')

os.environ["GLOG_minloglevel"] = "2" # Surpress a bunch of warnings
import caffe
caffe.set_device(0)
caffe.set_mode_gpu()

from google.protobuf import text_format
from caffe.proto import caffe_pb2


def load_labelmap_from_file(labelmap_file):
    file = open(labelmap_file, 'r')
    labelmap = caffe_pb2.LabelMap()
    text_format.Merge(str(file.read()), labelmap)
    return labelmap

def get_labelname(labelmap, labels):
    num_labels = len(labelmap.item)
    labelnames = []
    if type(labels) is not list:
        labels = [labels]
    for label in labels:
        found = False
        for i in xrange(0, num_labels):
            if label == labelmap.item[i].label:
                found = True
                labelnames.append(labelmap.item[i].display_name)
                break
        assert found == True
    return labelnames

def load_model():
    model_def = '/models/VGGNet/ilsvrc15/SSD_500x500/deploy.prototxt'
    model_weights = '/models/VGGNet/ilsvrc15/SSD_500x500/VGG_ilsvrc15_SSD_500x500_iter_480000.caffemodel'

    net = caffe.Net(model_def,      # defines the structure of the model
                    model_weights,  # contains the trained weights
                    caffe.TEST)     # use test mode (e.g., don't perform dropout)
    return net

def create_transformer(net):
    # input preprocessing: 'data' is the name of the input blob == net.inputs[0]
    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
    transformer.set_transpose('data', (2, 0, 1))
    transformer.set_mean('data', np.array([104,117,123])) # mean pixel
    transformer.set_raw_scale('data', 255)  # the reference model operates on images in [0,255] range instead of [0,1]
    transformer.set_channel_swap('data', (2,1,0))  # the reference model has channels in BGR order instead of RGB
    return transformer


def detect_objects(image_paths, threshold):
    net = load_model()
    transformer = create_transformer(net)

    labelmap = load_labelmap_from_file(caffe_root+'data/ILSVRC2016/labelmap_ilsvrc_det.prototxt')

    # set net batch size to 1
    image_resize = 500
    net.blobs['data'].reshape(1,3,image_resize,image_resize)

    input_images = []
    for image_file in image_paths:
        image = caffe.io.load_image(image_file)
        transformed_image = transformer.preprocess('data', image)

        net.blobs['data'].data[...] = transformed_image
        detections = net.forward()['detection_out']
        classify_object(image_file, image, detections, labelmap, threshold)


def classify_object(image_file, image, detections, labelmap, threshold):
    # Parse the outputs.
    det_label = detections[0,0,:,1]
    det_conf = detections[0,0,:,2]
    det_xmin = detections[0,0,:,3]
    det_ymin = detections[0,0,:,4]
    det_xmax = detections[0,0,:,5]
    det_ymax = detections[0,0,:,6]

    # Get detections with confidence higher than 0.6.
    top_indices = [i for i, conf in enumerate(det_conf) if conf >= threshold]

    top_conf = det_conf[top_indices]
    top_label_indices = det_label[top_indices].tolist()
    top_labels = get_labelname(labelmap, top_label_indices)
    top_xmin = det_xmin[top_indices]
    top_ymin = det_ymin[top_indices]
    top_xmax = det_xmax[top_indices]
    top_ymax = det_ymax[top_indices]

    print(image_file)
    for i in xrange(top_conf.shape[0]):
        xmin = int(round(top_xmin[i] * image.shape[1]))
        ymin = int(round(top_ymin[i] * image.shape[0]))
        xmax = int(round(top_xmax[i] * image.shape[1]))
        ymax = int(round(top_ymax[i] * image.shape[0]))
        score = top_conf[i]
        label = int(top_label_indices[i])
        label_name = top_labels[i]
        print('%s: %.2f'%(label_name, score), 'bbox: %i, %i, %i, %i'%(xmin, ymin, xmax-xmin+1, ymax-ymin+1))

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser()

    parser.add_argument("image_files", help="The filename(s) (including path, full or relative) of the image(s) you want to classify.", nargs="+")

    parser.add_argument("-D", "--data_path", help="Directory path of where the data is mounted. If this script is running whithin a docker it should be the docker local path", default="/data")

    parser.add_argument("-t", "--threshold", type=float, help="Threshold to use for output of classes.", required=True)

    args = parser.parse_args()

    data_path = args.data_path
    image_filenames = [os.path.join(data_path, image_file) for image_file in args.image_files]
    
    threshold = args.threshold
    detect_objects(image_filenames, threshold) 
