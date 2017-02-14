# Build:
# docker build -t nlescsherlockdl/base:image_classify .
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

# import matplotlib so it builds the font cache, saving time in derived images
RUN python -c "import matplotlib.pyplot as plt"