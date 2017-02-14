# Build:
# cd to deeplearning/docker/car/model, then:

# docker build -t nlescsherlockdl/car:model .
# docker push nlescsherlockdl/car:model

# To run on all files in a data directory with batch size 59:

# docker pull nlescsherlockdl/car:model
# DATADIR=/somewhere/on/your/local/filesystem/with/images
# nvidia-docker run \
#     -v $DATADIR:/data \
#     nlescsherlockdl/car:model \
#     -v \
#     --batch_size=59 \
#     --json \
#     --gpu_id=0 \
#     -D /data `ls $DATADIR`

FROM nlescsherlockdl/cnn_classify

MAINTAINER NLeSC <info@esciencecenter.nl>

COPY model /model

RUN cd /model && \
  tar xzf 20161123-113355-22b6_epoch_100.0.tar.gz
RUN mv /model/snapshot_iter_249000.caffemodel /model/snapshot.caffemodel
