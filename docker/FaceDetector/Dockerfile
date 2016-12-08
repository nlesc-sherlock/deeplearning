# This is a docker of a command-line tool "facedetect", which is a python wrapper of the Haar face detector in OpenCV. 
# It detects multople faces in an image if they are mostly frontal, well illuminated and not occluded.
# it outputs the bounding boxes (BBes) in format: the X Y coordinates (from the top-left corner), followed by width and height
# the docker could be used as follows:
# docker run -v <path-to-image>:/data nlescsherlockdl/facedetect /data/<image>
# 226 72 37 37
# 371 88 38 38
# for debugging purposes one can generate an ouput image which is th einputwith overlayed BBes:
# docker run -v <path-to-image>:/data nlescsherlockdl/facedetect /data/out.jpg /data/<image>
# 226 72 37 37
# 371 88 38 38
# + file out.jpg with overlayed BBes 

FROM nlescsherlockdl/ubuntu-16.04-cuda-8

RUN apt update

RUN apt-get -y install python python-opencv libopencv-dev

RUN wget https://github.com/wavexx/facedetect/archive/master.zip

RUN apt-get install unzip
RUN unzip  master.zip

ENTRYPOINT ["facedetect-master/facedetect"] 

