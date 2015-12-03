#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import sys
import caffe
import os

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


def classify(image_files, model_path, model_name, model_conf_name='deploy.prototxt',
	     mean_pixel_name='mean.binaryproto',
	     gray_range=255, channel_swap=(2,1,0), batch_size=0, gpu_id=-1, verbose=0):
	# paths
	model_configuration = os.path.join(model_path, model_conf_name)
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
		print "Builging a CNN classifier..."
	net = caffe.Classifier(model_configuration, model, mean=channel_mean,
	                       channel_swap=channel_swap, raw_scale=gray_range)
	image_x, image_y = net.blobs['data'].data.shape[-2:]
	channels = net.blobs['data'].data.shape[1]
	if batch_size == 0:
	    batch_size = net.blobs['data'].data.shape[0]
	if verbose:
		print "Reshaping the data..."
		print "batch size: ", batch_size
		print "number of channels: ", channels
		print "data shape: ", image_x, image_y
	
			
	net.blobs['data'].reshape(batch_size, channels, image_x, image_y)

	print "Loading image(s) to classify..."
	input_images = []
	for image_file in image_files:
	    input_images.append(caffe.io.load_image(image_file))

	# batch process the images:
	if verbose:
		print "Predicting the category classes of the image(s)..."
	prediction = net.predict(input_images)

	# convert to probabilities (if needed):
	probs = []
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


def run(image_files, model_path, model_name, model_conf_name='deploy.prototxt',
	labels_name='labels.txt', mean_pixel_name='mean.binaryproto',
	gray_range=255, channel_swap=(2,1,0), batch_size=0, gpu_id=-1, verbose=0):
	probs = classify(image_files, model_path, model_name, model_conf_name=model_conf_name,
			 mean_pixel_name=mean_pixel_name,
			 gray_range=gray_range, channel_swap=channel_swap, batch_size=batch_size,
			 gpu_id=gpu_id, verbose=verbose)
	print_classification(probs, image_files, model_path, labels_name=labels_name)

	
if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	
	parser.add_argument("image_files", help="The filename(s) (including path, full or relative) of the image(s) you want to classify.", nargs="+", type=argparse.FileType('r'))
	parser.add_argument("-m", "--model_file", help="The full filename of the caffemodel snapshot in the model (including path). We assume the directory of this file contains deploy.prototxt, labels.txt, mean.binaryproto and the caffemodel file as well. Otherwise, specify the filenames of those files with relative paths starting from the model_file path.", type=argparse.FileType('r'), required=True)

	parser.add_argument("--model_conf_name", help="The deploy file name (default: deploy.prototxt).", default='deploy.prototxt')
	parser.add_argument("--labels_name", help="Labels file name (default: labels.txt).", default='labels.txt')
	parser.add_argument("--mean_pixel_name", help="Mean pixel file name of the trained model (default: mean.binaryproto).", default='mean.binaryproto')
	parser.add_argument("--gray_range", help="Gray range of the images (default: 255).", type=int, default=255)
	parser.add_argument("--channel_swap", help="Use numbers 0, 1 and 2 to give the order of the color-channels that the model used, for instance 0 1 2 for RGB. Some models swap the channels from RGB to BGR (this is the default: 2 1 0).", nargs=3, default=[2,1,0])
	parser.add_argument("--batch_size", help="Number of images processed simultaneously. Default: taken from model configuration.", type=int, default=0)
	parser.add_argument("--gpu_id", help="To use GPU mode, specify the gpu_id that you want to use. Default: CPU mode (-1).", type=int, default=-1)
	parser.add_argument("-v", "--verbose", help="Duh.", action="store_true")

	args = parser.parse_args()

	model_path, model_name = os.path.split(args.model_file.name)

	image_filenames = [image_file.name for image_file in args.image_files]

	run(image_filenames, model_path, model_name,
	    model_conf_name=args.model_conf_name, labels_name=args.labels_name,
 	    mean_pixel_name=args.mean_pixel_name, gray_range=args.gray_range,
	    channel_swap=args.channel_swap, batch_size=args.batch_size, gpu_id=args.gpu_id, verbose=args.verbose)
