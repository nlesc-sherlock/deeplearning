FROM nlescsherlockdl/ubuntu-16.04-cuda-8

RUN apt install -y git cmake \
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
    python-skimage

RUN apt install -y --no-install-recommends libboost-all-dev

ENV CAFFE_ROOT=/opt/caffe

WORKDIR /opt
RUN git clone https://github.com/weiliu89/caffe.git \
    && cd caffe \
    && git checkout ssd

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