# Build:
# cd to deeplearning/docker/face/gender-wrapper, then:

# docker build -t nlescsherlockdl/face:gender-wrapper .
# docker push nlescsherlockdl/face:gender-wrapper

# To run on all files in a data directory with batch size 59:

# docker pull nlescsherlockdl/face:gender-wrapper
# DATADIR=/somewhere/on/your/local/filesystem/with/images
# JSONDIR=/somewhere/else/where/the/input/json/file/is/located
# JSON_INPUT_FILE=input_file_name.json
# OUTDIR=/where/you/want/your/output/json/file/to/go
# JSON_OUTPUT_FILE=output_file_name.json
# nvidia-docker run \
#     -v $DATADIR:/data \
#     -v $JSONDIR:/json \
#     -v $OUTDIR:/output \
#     nlescsherlockdl/face:gender-wrapper \
#     -v \
#     --batch_size=59 \
#     --gpu_id=0 \
#     -D /data \
#     --workflow_out="/output/$JSON_OUTPUT_FILE" \
#     "/json/$JSON_INPUT_FILE"

FROM nlescsherlockdl/face:gender

MAINTAINER NLeSC <info@esciencecenter.nl>

COPY image_classify_workflow_wrap_gender.py /scripts

ENTRYPOINT [""]
