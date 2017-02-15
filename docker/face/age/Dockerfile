# Build:
# cd to deeplearning/docker/face/age, then:

# docker build -t nlescsherlockdl/face:age .
# docker push nlescsherlockdl/face:age

# To run on all files in a data directory with batch size 59:

# docker pull nlescsherlockdl/face:age
# DATADIR=/somewhere/on/your/local/filesystem/with/images
# nvidia-docker run \
#     -v $DATADIR:/data \
#     nlescsherlockdl/face:age \
#     -v \
#     --batch_size=59 \
#     --json \
#     --gpu_id=0 \
#     -D /data `ls $DATADIR`

FROM nlescsherlockdl/cnn_classify

MAINTAINER NLeSC <info@esciencecenter.nl>

COPY model /model

RUN cd /model && \
  tar xzf GoogleNet_AgeGender_Age_20161201-160310-8255_epoch_300.0.tar.gz && \
  mv snapshot_iter_197700.caffemodel snapshot.caffemodel