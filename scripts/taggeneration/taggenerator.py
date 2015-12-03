import numpy as np
import sys
import caffe
import os

def generate_tags(input_image_file):
    """Returns tags of objects recognized in the image at the specified path.
    """
    # Make sure that caffe is on the python path:
    caffe_root = '/opt/caffe/'
    sys.path.insert(0, caffe_root + 'python')
    # model location
    model_path  = 'models/bvlc_reference_caffenet/'
    model_conf_name  = 'deploy.prototxt'
    model_name = 'bvlc_reference_caffenet.caffemodel'
    model_configuration_path = caffe_root + model_path + model_conf_name
    model = caffe_root + model_path + model_name
    # download script
    download_script = '../scripts/download_model_binary.py'
    # mean pixel file
    mean_pixel_file_path  = caffe_root + 'python/caffe/imagenet/ilsvrc_2012_mean.npy'
    # ImageNet labels filename
    imagenet_labels_filename = caffe_root + 'data/ilsvrc12/synset_words.txt'


    assert_file_exists(model)
    assert_file_exists(input_image_file)

    mode = caffe.TEST
    caffe.set_mode_cpu()
    net = caffe.Net(model_configuration_path, model, mode)

    batch_size =1
    channels  = 3
    gray_range = 255
    image_size = 227

    transformer = create_transformer(net, mean_pixel_file_path, gray_range)
    net.blobs['data'].reshape(batch_size,channels, image_size, image_size)
    image = caffe.io.load_image(input_image_file)
    net.blobs['data'].data[...] = transformer.preprocess('data', image)

    out = net.forward()
    labels = load_labels(imagenet_labels_filename)

    top_k = net.blobs['prob'].data[0].flatten().argsort()[::-1]
    probs = net.blobs['prob'].data[0].flatten()

    min_p = 0.1 # Minimum acceptable probability for a tag
    return [(labels[i], probs[i]) for i in top_k if probs[i] > min_p]

def load_labels(labels_filename):
    try:
        return np.loadtxt(labels_filename, str, delimiter='\t')
    except:
        raise Exception("Could not load labels file.")

def assert_file_exists(path):
    if os.path.isfile(path):
        pass
    else:
        raise Exception("The specified file (" + path + ") cannot be found.")

def create_transformer(net, mean_pixel_file_path, gray_range):
    # input preprocessing: 'data' is the name of the input blob == net.inputs[0]
    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
    transformer.set_transpose('data', (2,0,1))
    transformer.set_mean('data', np.load(mean_pixel_file_path).mean(1).mean(1)) # mean pixel
    transformer.set_raw_scale('data', gray_range)  # the reference model operates on images in [0,255] range instead of [0,1]
    transformer.set_channel_swap('data', (2,1,0))  # the reference model has channels in BGR order instead of RGB
    return transformer
