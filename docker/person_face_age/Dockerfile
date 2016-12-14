# Build:
# cd to deeplearning/docker/person_face_age, then:

# docker build -t nlescsherlockdl/person_face_age .
# docker push nlescsherlockdl/person_face_age

# To run on all files in a data directory with batch size 59:

# docker pull nlescsherlockdl/person_face_age
# DATADIR=/somewhere/on/your/local/filesystem/with/images
# nvidia-docker run \
#     -v $DATADIR:/data \
#     nlescsherlockdl/person_face_age \
#     -v \
#     --batch_size=59 \
#     --json \
#     --gpu_id=0 \
#     -D /data `ls $DATADIR`

FROM nlescsherlockdl/image_classify_base

MAINTAINER NLeSC <info@esciencecenter.nl>

# update A if you want to repull
RUN A=1
RUN cd /opt/deeplearning && \
  git pull

RUN cd /opt/deeplearning/Models/GoogleNet_AgeGender_Age && \
  tar xzf 20161201-160310-8255_epoch_300.0.tar.gz

ENTRYPOINT ["/opt/deeplearning/scripts/cnn_classify.py", "-M", "/opt/deeplearning/Models/GoogleNet_AgeGender_Age", "--model_snapshot", "snapshot_iter_197700.caffemodel"]
