# Build:
# cd to deeplearning/image_classify_BASE, then:
# docker build -t nlescsherlockdl/image_classify:base .
# This image is for use as a base image only!

FROM nlescsherlockdl/image_classify:caffe-nv

MAINTAINER NLeSC <info@esciencecenter.nl>

# Get dependencies
RUN apt-get update

# python deps
RUN apt-get install -y \
  python-scipy \
  python-matplotlib \
  python-protobuf \
  python-yaml \
  python-pil \
  git

COPY crablip.py /opt/deeplearning/scripts/                                                                                               
COPY utils/ /opt/deeplearning/scripts/


ENV PATH /opt/caffe/.build_release/tools:$PATH
ENV PYTHONPATH /opt/caffe/python:$PYTHONPATH
