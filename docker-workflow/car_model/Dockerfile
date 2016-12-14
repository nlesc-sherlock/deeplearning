# Build:
# cd to deeplearning/docker-workflow/car_model, then:

# docker build -t nlescsherlockdl/car_model_workflow .
# docker push nlescsherlockdl/car_model_workflow

# To run on all files in a data directory with batch size 59:

# docker pull nlescsherlockdl/car_model_workflow
# DATADIR=/somewhere/on/your/local/filesystem/with/images
# nvidia-docker run \
#     -v $DATADIR:/data \
#     nlescsherlockdl/car_model_workflow \
#     -v \
#     --batch_size=59 \
#     --json \
#     --gpu_id=0 \
#     -D /data `ls $DATADIR`

FROM nlescsherlockdl/car_model

MAINTAINER NLeSC <info@esciencecenter.nl>

# update A if you want to repull
RUN A=0
RUN cd /opt/deeplearning/ && \
  git pull

ENTRYPOINT ["/opt/deeplearning/scripts/image_classify_workflow_wrap_car_model.py", "-M", "/opt/deeplearning/Models/car_model", "--model_snapshot", "snapshot_iter_249000.caffemodel", "--json"]
