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
	# Configuration example
	model_path = '/home/pbos/git/deeplearning/Models/lotsacars_20151201-173534-9b16_E60/'
	model_name = 'snapshot_iter_66900.caffemodel'

	image_file = '/home/pbos/ferrari-09.jpg'

	run(image_file, model_path, model_name)
