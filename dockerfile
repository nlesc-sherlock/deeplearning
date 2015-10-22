# sudo docker run -u $UID -v $PWD:/data sfm_image

FROM tleyden5iwx/caffe-cpu-master
RUN pip install jupyter
# Download the trained model
RUN /opt/caffe/scripts/download_model_binary.py /opt/caffe/models/bvlc_reference_caffenet
# Download the labels/classes
RUN /opt/caffe/data/ilsvrc12/get_ilsvrc_aux.sh
ADD . /deeplearning
RUN sudo pip install -r /deeplearning/scripts/requirements.txt
ENTRYPOINT ["python", "/deeplearning/scripts/generatetags.py"]
CMD ["/deeplearning/testdata/guncase.jpg"]
# For Jupyter
#EXPOSE 8888
