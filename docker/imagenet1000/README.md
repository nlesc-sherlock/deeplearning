# ImageNet subset classifier

## Description
This file is a script for docker to build a docker container. The resulting container 
can be given an image as an argument and the container will output labels of things
the CNN recognizes in the image. For each label, the network provides a probability
which indicates how sure the network is of recognizing an object with that label.
The docker image is also available from dockerhub as 'nlesc/imagenet1000'.

## Building the container
Install docker and clone this repository. From the root of this repository run the 
following to build the container and call it 'imagenet'.

     sudo docker build -t imagenet .
 
## Classifying an image
To classify a picture it has to be in your current working directory. The contents of
the current working directory will be mounted in the docker container at /data. To 
classify 'someimage.jpg' in your cwd run the following.
sudo docker run -v $PWD:/data imagenet data/someimage.jpg
Alternatively, use the run_imagenet.sh script (from any directory):

    ./run_imagenet.sh someimage.jpg