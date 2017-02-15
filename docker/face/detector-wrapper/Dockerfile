# Build:
# cd to deeplearning/docker/face/detector-wrapper, then:

# docker build -t nlescsherlockdl/face:detector-wrapper .
# docker push nlescsherlockdl/face:detector-wrapper

# To run on all files in a data directory with batch size 59:

# docker pull nlescsherlockdl/face:detector-wrapper
# DATADIR=/somewhere/on/your/local/filesystem/with/images
# JSONDIR=/somewhere/else/where/the/input/json/file/is/located
# JSON_INPUT_FILE=input_file_name.json
# OUTDIR=/where/you/want/your/output/json/file/to/go
# JSON_OUTPUT_FILE=output_file_name.json
# nvidia-docker run \
#     -v $DATADIR:/data \
#     -v $JSONDIR:/json \
#     -v $OUTDIR:/output \
#     nlescsherlockdl/face:detector-wrapper \
#     -D /data \
#     --workflow_out="/output/$JSON_OUTPUT_FILE" \
#     "/json/$JSON_INPUT_FILE"

FROM nlescsherlockdl/face:detector

MAINTAINER NLeSC <info@esciencecenter.nl>

COPY face_detection_workflow_wrap.py /scripts/

ENTRYPOINT [""]
