# Build:
# cd to deeplearning/docker/face/gender, then:

# docker build -t nlescsherlockdl/face:gender .
# docker push nlescsherlockdl/face:gender

# To run on all files in a data directory with batch size 59:

# docker pull nlescsherlockdl/face:gender
# DATADIR=/somewhere/on/your/local/filesystem/with/images
# nvidia-docker run \
#     -v $DATADIR:/data \
#     nlescsherlockdl/face:gender \
#     -v \
#     --batch_size=59 \
#     --json \
#     --gpu_id=0 \
#     -D /data `ls $DATADIR`

FROM nlescsherlockdl/base:image_classify

MAINTAINER NLeSC <info@esciencecenter.nl>

COPY model /model

RUN cd /model && \
  tar xzf GoogleNet_AgeGender_Gender_20161108-091520-60bd_epoch_5.0.tar.gz && \
  mv snapshot_iter_1665.caffemodel snapshot.caffemodel
