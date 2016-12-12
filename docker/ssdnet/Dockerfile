FROM nlescsherlockdl/caffe-nv-ssd

RUN apt install -y wget

COPY models /models
COPY test.py /opt/caffe

WORKDIR $CAFFE_ROOT/data/ilsvrc12
RUN ./get_ilsvrc_aux.sh

