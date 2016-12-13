FROM nlescsherlockdl/caffe-nv-ssd

RUN apt install -y wget

WORKDIR /
RUN wget http://www.cs.unc.edu/~wliu/projects/SSD/models_VGGNet_ilsvrc15_SSD_500x500.tar.gz && \
    tar zxf models_VGGNet_ilsvrc15_SSD_500x500.tar.gz && \
    rm models_VGGNet_ilsvrc15_SSD_500x500.tar.gz
COPY models /models

WORKDIR $CAFFE_ROOT/data/ilsvrc12
RUN ./get_ilsvrc_aux.sh


COPY detect.py /opt/caffe
RUN chmod +x /opt/caffe/detect.py

ENTRYPOINT ["/opt/caffe/detect.py", "-t", "0.2"]
