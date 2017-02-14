# Build:
# docker build -t nlescsherlockdl/base:caffe-nv .
# This image is for use as a base image only!

FROM nlescsherlockdl/base:caffe-nv

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

COPY crablip.py /scripts/                                                                                               
COPY utils/ /scripts/


ENV PATH /opt/caffe/.build_release/tools:$PATH
ENV PYTHONPATH /opt/caffe/python:$PYTHONPATH
