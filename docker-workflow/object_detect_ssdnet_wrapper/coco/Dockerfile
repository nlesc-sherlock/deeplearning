FROM nlescsherlockdl/object_detect_ssdnet_coco

COPY detect_wrapper.py /opt/detect_wrapper.py
RUN chmod +x /opt/detect_wrapper.py

ENTRYPOINT ["/opt/detect_wrapper.py"]
