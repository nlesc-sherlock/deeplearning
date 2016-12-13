# Build:
# cd to deeplearning/docker/car_model, then:

# docker build -t nlescsherlockdl/car_model .
# docker push nlescsherlockdl/car_model

# To run on all files in a data directory with batch size 59:

# docker pull nlescsherlockdl/car_model
# DATADIR=/somewhere/on/your/local/filesystem/with/images
# nvidia-docker run \
#     -v $DATADIR:/data \
#     nlescsherlockdl/car_model \
#     -v \
#     --batch_size=59 \
#     --json \
#     --gpu_id=0 \
#     -D /data `ls $DATADIR`

FROM nlescsherlockdl/image_classify_base

MAINTAINER NLeSC <info@esciencecenter.nl>

RUN cd /opt/deeplearning/Models/car_model && \
  git pull

RUN cd /opt/deeplearning/Models/car_model && \
  tar xzf 20161123-113355-22b6_epoch_100.0.tar.gz

ENTRYPOINT ["/opt/deeplearning/scripts/cnn_classify.py", "-M", "/opt/deeplearning/Models/car_model", "--model_snapshot", "snapshot_iter_249000.caffemodel"]
