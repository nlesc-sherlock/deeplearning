# Build:
# docker build -t nlescsherlockdl/base:caffe-nv
FROM nvidia/cuda:8.0-cudnn5-devel-ubuntu16.04

RUN apt update \ 
    && apt install -y git cmake \
    libatlas-base-dev \
    libboost-all-dev \
    libgflags-dev \
    libgoogle-glog-dev \
    libhdf5-serial-dev \
    libleveldb-dev \
    liblmdb-dev \
    libopencv-dev \
    libprotobuf-dev \
    libsnappy-dev \
    protobuf-compiler \
    python-dev \
    python-numpy \
    python-pip \
    python-scipy \
    python-skimage\
    libboost-all-dev \
    && rm -rf /var/lib/apt/lists/*

ENV CAFFE_ROOT=/opt/caffe

WORKDIR /opt
RUN git clone https://git@github.com/NVIDIA/caffe.git \
    && cd caffe \
    && git checkout tags/v0.15.14

WORKDIR $CAFFE_ROOT
RUN mkdir build \
    && cd build \
    && cmake ${CMAKE_ARGS} .. \
    && make all -j"$(nproc)" \
    && make install

ENV PYCAFFE_ROOT $CAFFE_ROOT/python
ENV PYTHONPATH $PYCAFFE_ROOT:$PYTHONPATH
ENV PATH $CAFFE_ROOT/build/tools:$PYCAFFE_ROOT:$PATH
RUN echo "$CAFFE_ROOT/build/lib" >> /etc/ld.so.conf.d/caffe.conf && ldconfig

# import matplotlib so it builds the font cache, saving time in derived images
RUN python -c "import matplotlib.pyplot as plt"