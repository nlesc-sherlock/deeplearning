FROM nlescsherlockdl/ssd:caffe-nv

RUN apt install -y wget

WORKDIR /
RUN wget http://www.cs.unc.edu/~wliu/projects/SSD/models_VGGNet_VOC0712Plus_SSD_512x512_ft.tar.gz && \
    tar zxf models_VGGNet_VOC0712Plus_SSD_512x512_ft.tar.gz && \
    rm models_VGGNet_VOC0712Plus_SSD_512x512_ft.tar.gz
COPY models /models

COPY detect.py /opt/
RUN chmod +x /opt/detect.py

ENTRYPOINT ["/opt/detect.py", "-t", "0.2"]
