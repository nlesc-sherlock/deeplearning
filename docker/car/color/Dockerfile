# Build:
# cd to deeplearning/docker/car/color, then:

# docker build -t nlescsherlockdl/car:color .
# docker push nlescsherlockdl/car:color

# To run on all files in a data directory with batch size 59:

# docker pull nlescsherlockdl/car:color
# DATADIR=/somewhere/on/your/local/filesystem/with/images
# nvidia-docker run \
#     -v $DATADIR:/data \
#     nlescsherlockdl/car:color \
#     -v \
#     --batch_size=59 \
#     --json \
#     --gpu_id=0 \
#     -D /data `ls $DATADIR`

FROM nlescsherlockdl/cnn_classify

MAINTAINER NLeSC <info@esciencecenter.nl>

COPY model /model

RUN cd /model && \
  tar xzf 20161117-151423-d9a3_epoch_100.0.tar.gz
RUN mv /model/snapshot_iter_63400.caffemodel /model/snapshot.caffemodel