#!/usr/bin/env bash

DATADIR=$PWD
MODELDIR=/home/patrick/sw/git/deeplearning/Models/lotsacars-20151202-170935-03d3

FILES="01f46a40ae3c24.jpg 0e7e71c3887b54.jpg"

FILES_CONTAINER=""
for fn in $FILES; do
  FILES_CONTAINER+="/data/$fn "
done

docker run \
  -v ${DATADIR}:/data \
  -v ${MODELDIR}:/model \
  -v ${HOME}/sw/git/deeplearning:/opt/deeplearning \
  caffe_image_classify \
  -v --gpu_id=-1 --batch_size=59 \
  -M /model \
  $FILES_CONTAINER
