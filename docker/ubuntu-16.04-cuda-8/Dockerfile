FROM ubuntu:16.04

RUN apt update \
    && apt upgrade -y \
    && apt install -y wget build-essential kmod pkg-config

ENV CUDA_INSTALLER=https://developer.nvidia.com/compute/cuda/8.0/prod/local_installers/cuda_8.0.44_linux-run
ENV INSTALLER_LOCATION=/opt/nvidia_installers

WORKDIR /opt
RUN wget $CUDA_INSTALLER \
  && sh cuda_8.0.44_linux-run -extract=$INSTALLER_LOCATION

WORKDIR $INSTALLER_LOCATION
RUN ./NVIDIA-Linux-x86_64-367.48.run -s -N --no-kernel-module

WORKDIR $INSTALLER_LOCATION
RUN ./cuda-linux64-rel-8.0.44-21122537.run -noprompt

WORKDIR /opt
RUN rm -rf $INSTALLER_LOCATION \
    && rm cuda_8.0.44_linux-run

RUN echo '/usr/local/cuda-8.0/lib64' > /etc/ld.so.conf.d/cuda.conf \
    && ldconfig

ENV PATH=$PATH:/usr/local/cuda-8.0/bin

# Clean up install
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*