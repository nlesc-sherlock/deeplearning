# Build:
# cd to deeplearning/docker/draw_crop_box, then:
# docker build -t nlescsherlockdl/draw_crop_box .

# Run:
# DATADIR=/somewhere/on/your/local/filesystem/with/an/image
# JSONDIR=/somewhere/else/where/the/boxes/json/file/is/located
# OUTDIR=/where/you/want/your/output/json/file/to/go
# IMAGE_FN=filename_of_your_image
# BOXES_FN=filename_of_your_boxes_json_file
# OUTPUT_FN=filename_of_output_image
# docker run \
#     -v $DATADIR:/data \
#     -v $JSONDIR:/json \
#     -v $OUTDIR:/output \
#     nlescsherlockdl/draw_crop_box \
#     /data/$IMAGE_FN /json/$BOXES_FN
#     --output_file /output/$OUTPUT_FN

FROM nlescsherlockdl/base:image_classify

MAINTAINER NLeSC <info@esciencecenter.nl>

COPY draw_crop_box.py /scripts

ENTRYPOINT ["/scripts/draw_crop_box.py"]
