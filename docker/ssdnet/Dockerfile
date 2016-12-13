FROM nlescsherlockdl/caffe-nv-ssd

RUN apt install -y wget


RUN mkdir /models
WORKDIR /models
RUN wget http://www.cs.unc.edu/~wliu/projects/SSD/models_VGGNet_ilsvrc15_SSD_500x500.tar.gz
COPY models /models

COPY test.py /opt/caffe

WORKDIR $CAFFE_ROOT/data/ilsvrc12
RUN ./get_ilsvrc_aux.sh

