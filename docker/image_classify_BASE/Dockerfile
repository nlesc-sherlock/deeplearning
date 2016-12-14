# Build:
# cd to deeplearning/image_classify_BASE, then:
# docker build -t nlescsherlockdl/image_classify_base .
# This image is for use as a base image only!

FROM nlescsherlockdl/caffe-nv

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

# Get the deeplearning git repo
RUN A=4
RUN cd /opt && \
  git clone https://github.com/nlesc-sherlock/deeplearning.git

ENV PATH /opt/caffe/.build_release/tools:$PATH
ENV PYTHONPATH /opt/caffe/python:$PYTHONPATH
