# Lessons learnt

## Day 1

We have learnt about neural networks and deep learning basics from 
[A Deep Learning Tutorial: from Perceptrons to Deep Networks]
(http://www.toptal.com/machine-learning/an-introduction-to-deep-learning-from-perceptrons-to-deep-networks). 
Types of network elements: Perceptron, Autoencoders and Restricted Boltzman Machines (RMB) and how to train them.
We have learnt about Convolutional Neural Networks (CNN) and how they are used for image classification. 
We have looked at the MNIST hand written digit recognition example from
http://cs.stanford.edu/people/karpathy/convnetjs/demo/mnist.html.

We have started the Caffe hands-on tutorial
[DIY Deep Learning with Caffe](https://docs.google.com/presentation/d/1UeKXVgRvvxg9OUdh_UiC5G71UMscNPlvArsWER41PsU/edit?pli=1#slide=id.gc2fcdcce7_216_101) 
When at the classification IPython notebook example we ran into the problem of how to run such a notebook from 
within the docker container with Caffe. 
We have figured it out as described in our 
[startup guide](https://github.com/nlesc-sherlock/Sherlock/blob/master/topics/deeplearning/startupguide.md).

## Day 2 morning

We completed the first assignment in the DIY-deeplearning-with-caffe tutorial. We classified a single photo of a cat with a pretrained network and visualized both the filters and their activations on this image. After the first 2 conv layers the activations start to look quite abstract and we cannot interpret it anymore. Some questions we have are:
- If we have one conv layer with n filters, we would expect the input of the next layer to have size n in one of its dimensions (and width and height etc in the others). Often however we only see size n/2 appear as an input for the next conv filter. This also happens for the image size but we know this is because of a pooling layer. Maybe the pooling layer is not of size 2x2 but 2x2x2 so also subsampling from the different feature maps.
