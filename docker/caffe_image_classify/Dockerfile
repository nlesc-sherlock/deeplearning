# Build:
# cd to deeplearning/caffe_nv_docker, then:
# docker build -t cnn_classify .
# Run:
# cd to directory with images, then:
# docker run -v $PWD:/data cnn_classify -v --gpu_id=-1 --batch_size=59 -m /opt/deeplearning/Models/lotsacars-20151202-170935-03d3/snapshot_iter_334500.caffemodel /data/image1.jpg /data/image2.jpg
# Put " 2> /dev/null " behind it to cut out all the Caffe model setup messages.

FROM nlescsherlockdl/caffe-nv

MAINTAINER NLeSC <info@esciencecenter.nl>

# # A docker container with NVIDIA fork (https://github.com/NVIDIA/caffe) of caffe
# # (caffe.berkeleyvision.org) installed, including GPU mode.

# # Get dependencies
RUN apt-get update
# RUN apt-get update && apt-get install -y \
#   libprotobuf-dev \
#   libleveldb-dev \
#   libsnappy-dev \
#   libopencv-dev \
#   libboost-all-dev \ 
#   libhdf5-serial-dev \ 
#   protobuf-compiler \ 
#   gcc-4.6 \ 
#   g++-4.6 \ 
#   gcc-4.6-multilib \  
#   g++-4.6-multilib \ 
#   gfortran \ 
#   libjpeg62 \ 
#   libfreeimage-dev \  
#   libatlas-base-dev \  
#   git \ 
#   python-dev \  
#   python-pip \ 
#   bc \ 
#   wget \ 
#   curl \ 
#   unzip \ 
#   cmake \ 
#   liblmdb-dev \  
#   libgflags-dev \
#   libgoogle-glog-dev \
#   pkgconf

# Use gcc 4.6
# RUN update-alternatives --install /usr/bin/cc cc /usr/bin/gcc-4.6 30 && \
#   update-alternatives --install /usr/bin/c++ c++ /usr/bin/g++-4.6 30 && \ 
#   update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-4.6 30 && \
#   update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-4.6 30

# Allow it to find CUDA libs
# RUN echo "/usr/local/cuda/lib64" > /etc/ld.so.conf.d/cuda.conf && \
#   ldconfig 

# Clone the Caffe repo 
# RUN cd /opt && \
#   git clone https://github.com/nvidia/caffe.git

# Install python deps
RUN apt-get install -y \
  python-scipy \
  # cython \
  python-matplotlib \
  # ipython \
  # python-h5py \
  # python-networkx \
  # python-pandas \
  # python-dateutil \
  python-protobuf \
  python-yaml \
  python-pil \
  git
  # python-pip

# RUN sudo pip install nose

# Upgrade Cython
# RUN sudo pip install cython --upgrade

# RUN cd /opt/caffe/python && \
#  (pip install -r requirements.txt; easy_install numpy; pip install -r requirements.txt) && \
  # sudo pip install -r requirements.txt

# Build Caffe core
# RUN cd /opt/caffe && \
#   mkdir buildcmake && \
#   cd buildcmake && \
#   cmake .. && \
#   make all -j4

# Numpy include path hack - github.com/BVLC/caffe/wiki/Setting-up-Caffe-on-Ubuntu-14.04
#RUN NUMPY_EGG=`ls /usr/local/lib/python2.7/dist-packages | grep -i numpy` && \
#  ln -s /usr/local/lib/python2.7/dist-packages/$NUMPY_EGG/numpy/core/include/numpy /usr/include/python2.7/numpy

# Build Caffe python bindings and make + run tests
#RUN cd /opt/caffe && \
#  make pycaffe

# Add binaries to path
# RUN bash -c 'echo "export PATH=/opt/caffe/.build_release/tools:\$PATH" >> ~/.bashrc'

# Add PYTHONPATH
# RUN bash -c 'echo "export PYTHONPATH=/opt/caffe/python:\$PYTHONPATH" >> ~/.bashrc'

# Get the deeplearning git repo
RUN cd /opt && \
  git clone https://github.com/nlesc-sherlock/deeplearning.git

ENV PATH /opt/caffe/.build_release/tools:$PATH
ENV PYTHONPATH /opt/caffe/python:$PYTHONPATH

ENTRYPOINT ["/opt/deeplearning/scripts/cnn_classify.py"]
