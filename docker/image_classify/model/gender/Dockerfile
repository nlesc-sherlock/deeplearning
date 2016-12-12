# Build:
# cd to deeplearning/image_classify/model/gender, then:

# docker build -t nlescsherlockdl/image_classify_gender .
# docker push nlescsherlockdl/image_classify_gender

# To run on all files in a data directory with batch size 59:

# docker pull nlescsherlockdl/image_classify_gender
# DATADIR=/somewhere/on/your/local/filesystem/with/images
# nvidia-docker run \
#     -v $DATADIR:/data \
#     nlescsherlockdl/image_classify_gender \
#     -v \
#     --batch_size=59 \
#     --json \
#     --gpu_id=0 \
#     -D /data `ls $DATADIR`

FROM nlescsherlockdl/image_classify_base

MAINTAINER NLeSC <info@esciencecenter.nl>

# update A if you want to repull
RUN A=0
RUN cd /opt/deeplearning/Models/GoogleNet_AgeGender_Gender && \
  git pull

RUN tar xzf 20161108-091520-60bd_epoch_5.0.tar.gz

ENTRYPOINT ["/opt/deeplearning/scripts/cnn_classify.py -M /opt/deeplearning/Models/GoogleNet_AgeGender_Gender --model_snapshot snapshot_iter_1665.caffemodel"]
