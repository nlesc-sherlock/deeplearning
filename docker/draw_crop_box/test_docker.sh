#!/usr/bin/env bash
# Run from deeplearning git repo
DATADIR=visualization/dl-sherlock-app/images
JSONDIR=docker/draw_crop_box
OUTDIR=docker/draw_crop_box
IMAGE_FN=person_horse.jpg
BOXES_FN=boxes_example_docker.json
OUTPUT_FN=person_horse_boxes_test.jpg
docker run \
    -v $(readlink $DATADIR):/data \
    -v $(readlink $JSONDIR):/json \
    -v $(readlink $OUTDIR):/output \
    nlescsherlockdl/draw_crop_box \
    /data/$IMAGE_FN /json/$BOXES_FN
    --output_file /output/$OUTPUT_FN
