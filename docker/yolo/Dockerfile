#FROM recursionbane/darknet-cpu
#RUN wget http://pjreddie.com/media/files/yolo.weights --output-document=/darknet/yolo.weights
#./darknet yolo test cfg/yolo.cfg yolo.weights <image>

FROM nlescsherlockdl/ubuntu-16.04-cuda-8
RUN apt update
RUN apt -y install git
RUN git clone https://github.com/cwmeijer/darknet.git
WORKDIR /darknet
RUN make
RUN wget http://pjreddie.com/media/files/yolo.weights --output-document=/darknet/yolo.weights
RUN apt -y install python python-pip
RUN pip install docopt
ADD . /scripts
ENTRYPOINT ["python", "/scripts/run_yolo.py"]