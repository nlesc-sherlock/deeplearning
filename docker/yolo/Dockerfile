Description
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

FROM nlescsherlockdl/ubuntu-16.04-cuda-8
RUN apt update
RUN apt -y install git
RUN git clone https://github.com/cwmeijer/darknet.git
WORKDIR /darknet
RUN make
RUN wget http://pjreddie.com/media/files/yolo.weights --output-document=/darknet/yolo.weights
RUN apt -y install python python-pip
RUN pip install docopt
ADD . /scripts
ENTRYPOINT ["python", "/scripts/run_yolo.py"]