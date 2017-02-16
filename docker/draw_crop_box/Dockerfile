FROM nlescsherlockdl/base:image_classify

MAINTAINER NLeSC <info@esciencecenter.nl>

COPY draw_crop_box.py /scripts

ENV MPLBACKEND agg

ENTRYPOINT ["/scripts/draw_crop_box.py"]
