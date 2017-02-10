# Build:
# cd to deeplearning/caffe_nv_docker, then:
# docker build -t nlescsherlockdl/image_classify:cnn_classify .
# Run:
# cd to directory with images, then:
# docker run -v $PWD:/data cnn_classify -v --gpu_id=-1 --batch_size=59 -m /opt/deeplearning/Models/lotsacars-20151202-170935-03d3/snapshot_iter_334500.caffemodel /data/image1.jpg /data/image2.jpg
# Put " 2> /dev/null " behind it to cut out all the Caffe model setup messages.

FROM nlescsherlockdl/image_classify:base

MAINTAINER NLeSC <info@esciencecenter.nl>

COPY cnn_classify.py /opt/deeplearning/scripts/
COPY model /model

ENTRYPOINT ["/opt/deeplearning/scripts/cnn_classify.py"]
