# Description
# ---
# Object detection on an image
# ---
# To detect objects in a picture, using the YOLO algorithm, the picture has to be in your
# current working directory. The contents of
# the current working directory will be mounted in the docker container at /data. To
# detect objects in 'someimage.jpg' in your cwd run the following.
# sudo docker run -v $PWD:/data imagenet data/someimage.jpg
# Alternatively, use the run_imagenet.sh script (from any directory):
# docker run -v $PWD:/data/ nlescsherlockdl/yolo /data/someimage.jpg

FROM nvidia/cuda:8.0-cudnn5-devel-ubuntu16.04
RUN apt update
RUN apt install -y git ca-certificates wget python python-pip && \
    pip install -U pip

WORKDIR /
RUN git clone https://github.com/cwmeijer/darknet.git && cd darknet && make

WORKDIR /darknet
RUN wget http://pjreddie.com/media/files/yolo.weights
COPY . /scripts

ENTRYPOINT [""]

