# Build:
# cd to deeplearning/docker/face/detector, then:

# docker build -t nlescsherlockdl/face:detector .
# docker push nlescsherlockdl/face:detector

# This is a docker of a command-line tool "facedetect", which is a python wrapper of the Haar face detector in OpenCV. 
# It detects multiple faces in an image if they are mostly frontal, well illuminated and not occluded.
# it outputs the bounding boxes (BBes) in format: the X Y coordinates (from the top-left corner), followed by width and height
# the docker could be used as follows:
# docker run -v <path-to-image>:/data nlescsherlockdl/face:detector /data/<image>
# 226 72 37 37
# 371 88 38 38
# for debugging purposes one can generate an ouput image which is the input with overlayed BBes:
# docker run -v <path-to-image>:/data nlescsherlockdl/face:detector -o /data/out.jpg /data/<image>
# 226 72 37 37
# 371 88 38 38
# + file out.jpg with overlayed BBes 

FROM nlescsherlockdl/base:image_classify

MAINTAINER NLeSC <info@esciencecenter.nl>

RUN apt update && \
  apt-get -y install python-opencv libopencv-dev unzip

RUN wget https://github.com/wavexx/facedetect/archive/master.zip

RUN unzip master.zip && \
  cp facedetect-master/facedetect /scripts/facedetect.py

ENTRYPOINT ["facedetect-master/facedetect"] 
