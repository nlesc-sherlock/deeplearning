FROM nlescsherlockdl/caffe-nv

RUN pip install --upgrade pip

WORKDIR /opt
RUN git clone https://git@github.com/NVIDIA/DIGITS.git

WORKDIR /opt/DIGITS/
RUN git checkout tags/v5.0.0-rc.1 \
    && pip install -r requirements.txt

EXPOSE 5000
CMD /opt/DIGITS/digits-devserver
