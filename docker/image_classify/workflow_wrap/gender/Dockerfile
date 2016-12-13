# Build:
# cd to deeplearning/image_classify/workflow_wrap/gender, then:

# docker build -t nlescsherlockdl/image_classify_gender_workflow .
# docker push nlescsherlockdl/image_classify_gender_workflow

# To run on all files in a data directory with batch size 59:

# docker pull nlescsherlockdl/image_classify_gender_workflow
# DATADIR=/somewhere/on/your/local/filesystem/with/images
# JSONDIR=/somewhere/else/where/the/input/json/file/is/located
# JSON_INPUT_FILE=input_file_name.json
# nvidia-docker run \
#     -v $DATADIR:/data \
#     -v $JSONDIR:/json \
#     nlescsherlockdl/image_classify_gender_workflow \
#     -v \
#     --batch_size=59 \
#     --json \
#     --gpu_id=0 \
#     -D /data "/json/$JSON_INPUT_FILE"

FROM nlescsherlockdl/image_classify_gender

MAINTAINER NLeSC <info@esciencecenter.nl>

ENTRYPOINT ["/opt/deeplearning/scripts/image_classify_workflow_wrap_gender.py"]
