FROM nlescsherlockdl/ssd:base

COPY detect_wrapper.py /opt/detect_wrapper.py
RUN chmod +x /opt/detect_wrapper.py

COPY test/data /data
COPY test/test_input.json /opt/test_input.json

ENTRYPOINT ["/opt/detect_wrapper.py"]
