# Build:
# cd to deeplearning/docker/image_classify/workflow_wrap/gender, then:

# docker build -t nlescsherlockdl/image_classify_gender_workflow .
# docker push nlescsherlockdl/image_classify_gender_workflow

# To run on all files in a data directory with batch size 59:

# docker pull nlescsherlockdl/image_classify_gender_workflow
# DATADIR=/somewhere/on/your/local/filesystem/with/images
# JSONDIR=/somewhere/else/where/the/input/json/file/is/located
# JSON_INPUT_FILE=input_file_name.json
# OUTDIR=/where/you/want/your/output/json/file/to/go
# JSON_OUTPUT_FILE=output_file_name.json
# nvidia-docker run \
#     -v $DATADIR:/data \
#     -v $JSONDIR:/json \
#     -v $OUTDIR:/output \
#     nlescsherlockdl/image_classify_gender_workflow \
#     -v \
#     --batch_size=59 \
#     --gpu_id=0 \
#     -D /data \
#     --workflow_out="/output/$JSON_OUTPUT_FILE" \
#     "/json/$JSON_INPUT_FILE"

FROM nlescsherlockdl/image_classify_gender

MAINTAINER NLeSC <info@esciencecenter.nl>

# update A if you want to repull
RUN A=1
RUN cd /opt/deeplearning/ && \
  git pull

ENTRYPOINT ["/opt/deeplearning/scripts/image_classify_workflow_wrap_gender.py", "-M", "/opt/deeplearning/Models/GoogleNet_AgeGender_Gender", "--model_snapshot", "snapshot_iter_1665.caffemodel", "--json"]
