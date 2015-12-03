#!/usr/bin/env bash

filepath=$1

bn=$(basename $filepath)
dn=$(dirname $filepath)

cd "$dn"

docker run -v $PWD:/data imagenet data/${bn}

cd -