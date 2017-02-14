# Build:
# cd to deeplearning/docker-workflow/car_color, then:

# docker build -t nlescsherlockdl/car_color_workflow .
# docker push nlescsherlockdl/car_color_workflow

# To run on all files in a data directory with batch size 59:

# docker pull nlescsherlockdl/car_color_workflow
# DATADIR=/somewhere/on/your/local/filesystem/with/images
# JSONDIR=/somewhere/else/where/the/input/json/file/is/located
# JSON_INPUT_FILE=input_file_name.json
# OUTDIR=/where/you/want/your/output/json/file/to/go
# JSON_OUTPUT_FILE=output_file_name.json
# nvidia-docker run \
#     -v $DATADIR:/data \
#     -v $JSONDIR:/json \
#     -v $OUTDIR:/output \
#     nlescsherlockdl/car_color_workflow \
#     -v \
#     --batch_size=59 \
#     --gpu_id=0 \
#     -D /data \
#     --workflow_out="/output/$JSON_OUTPUT_FILE" \
#     "/json/$JSON_INPUT_FILE"

FROM nlescsherlockdl/car_color

MAINTAINER NLeSC <info@esciencecenter.nl>

# update A if you want to repull
RUN A=0
RUN cd /opt/deeplearning/ && \
  git checkout python-workflow

ENTRYPOINT ["/opt/deeplearning/scripts/image_classify_workflow_wrap_car_color.py", "-M", "/opt/deeplearning/Models/car_color", "--model_snapshot", "snapshot_iter_63400.caffemodel", "--json"]
