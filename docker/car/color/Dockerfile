# Build:
# cd to deeplearning/docker/car_color, then:

# docker build -t nlescsherlockdl/car_color .
# docker push nlescsherlockdl/car_color

# To run on all files in a data directory with batch size 59:

# docker pull nlescsherlockdl/car_color
# DATADIR=/somewhere/on/your/local/filesystem/with/images
# nvidia-docker run \
#     -v $DATADIR:/data \
#     nlescsherlockdl/car_color \
#     -v \
#     --batch_size=59 \
#     --json \
#     --gpu_id=0 \
#     -D /data `ls $DATADIR`

FROM nlescsherlockdl/image_classify_base

MAINTAINER NLeSC <info@esciencecenter.nl>

COPY model /models
COPY image_classify_workflow_wrap_car_color.py /opt/deeplearning/scripts

RUN cd /models && \
  tar xzf 20161117-151423-d9a3_epoch_100.0.tar.gz

ENTRYPOINT ["/opt/deeplearning/scripts/cnn_classify.py", "-M", "/models", "--model_snapshot", "snapshot_iter_63400.caffemodel"]
