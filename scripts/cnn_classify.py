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


def classify(image_file, model_path, model_name, model_conf_name='deploy.prototxt',
			 mean_pixel_name='mean.binaryproto',
			 gray_range=255, channel_swap=(2,1,0)):
	# paths
	model_configuration = model_path + model_conf_name
	model = model_path + model_name
	mean_pixel_file  = model_path + mean_pixel_name

	# other stuff
	channel_mean = get_channel_mean(mean_pixel_file)
	
	net = caffe.Classifier(model_configuration, model, mean=channel_mean,
	                       channel_swap=channel_swap, raw_scale=gray_range)

	input_image = caffe.io.load_image(image_file)

	prediction = net.predict([input_image])
	if prediction[0].sum() == 1 and np.all(prediction[0] > 0):
		probs = prediction[0]
	else:
		probs = softmax(prediction[0])
	
	return probs


def print_classification(probs, model_path, labels_name='labels.txt'):
	labels_file = model_path + labels_name
	labels = np.loadtxt(labels_file, str)
	
	print 'Predicted class & probabilities (top 5):', zip(labels[probs.argsort()[:-6:-1]],
													 probs[probs.argsort()[:-6:-1]])


def run(image_file, model_path, model_name, model_conf_name='deploy.prototxt',
		labels_name='labels.txt', mean_pixel_name='mean.binaryproto',
		gray_range=255, channel_swap=(2,1,0)):
	probs = classify(image_file, model_path, model_name, model_conf_name=model_conf_name,
					 mean_pixel_name=mean_pixel_name,
					 gray_range=gray_range, channel_swap=channel_swap)
	print_classification(probs, model_path, labels_name=labels_name)

	
if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	
	parser.add_argument("image_file", help="The filename (including path, full or relative) of the image you want to classify.", type=argparse.FileType('r'))
	parser.add_argument("model_name", help="The filename of the caffemodel snapshot in the model (without path, since it is assumed to be in model_path).")
	parser.add_argument("model_path", help="The path to your model files. We assume this directory contains deploy.prototxt, labels.txt, mean.binaryproto and the caffemodel file. Default: current directory.", nargs='?', default=os.getcwd() + "/")

	parser.add_argument("--model_conf_name", help="The deploy file name (default: deploy.prototxt).", default='deploy.prototxt')
	parser.add_argument("--labels_name", help="Labels file name (default: labels.txt).", default='labels.txt')
	parser.add_argument("--mean_pixel_name", help="Mean pixel file name of the trained model (default: mean.binaryproto).", default='mean.binaryproto')
	parser.add_argument("--gray_range", help="Gray range of the images (default: 255).", type=int, default=255)
	parser.add_argument("--channel_swap", help="Use numbers 0, 1 and 2 to give the order of the color-channels that the model used, for instance 0 1 2 for RGB. Some models swap the channels from RGB to BGR (this is the default: 2 1 0).", nargs=3, default=[2,1,0])

	args = parser.parse_args()

	# Configuration example
	#model_path = '/home/pbos/git/deeplearning/Models/lotsacars_20151201-173534-9b16_E60/'
	#model_name = 'snapshot_iter_66900.caffemodel'
	#image_file = '/home/pbos/ferrari-09.jpg'

	run(args.image_file.name, args.model_path, args.model_name,
	    model_conf_name=args.model_conf_name, labels_name=args.labels_name,
 	    mean_pixel_name=args.mean_pixel_name, gray_range=args.gray_range,
	    channel_swap=args.channel_swap)
