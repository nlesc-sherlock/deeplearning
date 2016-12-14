# Build:
# cd to deeplearning/docker/person_face_gender, then:

# docker build -t nlescsherlockdl/person_face_gender .
# docker push nlescsherlockdl/person_face_gender

# To run on all files in a data directory with batch size 59:

# docker pull nlescsherlockdl/person_face_gender
# DATADIR=/somewhere/on/your/local/filesystem/with/images
# nvidia-docker run \
#     -v $DATADIR:/data \
#     nlescsherlockdl/person_face_gender \
#     -v \
#     --batch_size=59 \
#     --json \
#     --gpu_id=0 \
#     -D /data `ls $DATADIR`

FROM nlescsherlockdl/image_classify_base

MAINTAINER NLeSC <info@esciencecenter.nl>

# update A if you want to repull
RUN A=2
RUN cd /opt/deeplearning/Models/GoogleNet_AgeGender_Gender && \
  git pull

RUN cd /opt/deeplearning/Models/GoogleNet_AgeGender_Gender && \
  tar xzf 20161108-091520-60bd_epoch_5.0.tar.gz

ENTRYPOINT ["/opt/deeplearning/scripts/cnn_classify.py", "-M", "/opt/deeplearning/Models/GoogleNet_AgeGender_Gender", "--model_snapshot", "snapshot_iter_1665.caffemodel"]
