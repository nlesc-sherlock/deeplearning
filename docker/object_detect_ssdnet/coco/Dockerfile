FROM nlescsherlockdl/caffe-nv-ssd

RUN apt install -y wget

RUN a=2
WORKDIR /
RUN wget http://www.cs.unc.edu/~wliu/projects/SSD/models_VGGNet_coco_SSD_300x300.tar.gz && \
    tar zxf models_VGGNet_coco_SSD_300x300.tar.gz && \
    rm models_VGGNet_coco_SSD_300x300.tar.gz
COPY models/VGGNet/coco/SSD_300x300/deploy.prototxt /models/VGGNet/coco/SSD_300x300/deploy.prototxt


COPY detect.py /opt/
RUN chmod +x /opt/detect.py

ENTRYPOINT ["/opt/detect.py", "-t", "0.2"]
