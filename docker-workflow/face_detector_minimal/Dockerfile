# Build:
# cd to deeplearning/docker-workflow/face_detector_minimal, then:

# docker build -t nlescsherlockdl/face_detector_workflow .
# docker push nlescsherlockdl/face_detector_workflow

# To run on all files in a data directory with batch size 59:

# docker pull nlescsherlockdl/face_detector_workflow
# DATADIR=/somewhere/on/your/local/filesystem/with/images
# JSONDIR=/somewhere/else/where/the/input/json/file/is/located
# JSON_INPUT_FILE=input_file_name.json
# OUTDIR=/where/you/want/your/output/json/file/to/go
# JSON_OUTPUT_FILE=output_file_name.json
# nvidia-docker run \
#     -v $DATADIR:/data \
#     -v $JSONDIR:/json \
#     -v $OUTDIR:/output \
#     nlescsherlockdl/face_detector_workflow \
#     -D /data \
#     --workflow_out="/output/$JSON_OUTPUT_FILE" \
#     "/json/$JSON_INPUT_FILE"

# FROM nlescsherlockdl/face_detector

FROM nlescsherlockdl/cuda7.5-cudnn5-devel

MAINTAINER NLeSC <info@esciencecenter.nl>

RUN apt update && \
  apt-get -y install python python-opencv libopencv-dev unzip

# Get the needed files from the local deeplearning git repo
RUN A=0
COPY face_detection_workflow_wrap.py /opt
COPY wrap_lib.py /opt

RUN wget https://github.com/wavexx/facedetect/archive/master.zip

RUN unzip master.zip && \
  cp facedetect-master/facedetect /opt/facedetect.py

ENTRYPOINT ["/opt/face_detection_workflow_wrap.py"]
