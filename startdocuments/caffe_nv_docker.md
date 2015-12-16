# Installation

Installing the Caffe NV Docker image we developed can be done either by downloading it from Docker Hub, or by building it yourself using the Dockerfile.

For both options, you need to have Docker installed.

## Downloading

```sh
docker pull egpbos/cnn_classify
```

## Building

```sh
cd deeplearning/caffe_nv_docker
docker build -t cnn_classify .
```


# Running

In the terminal, cd to a directory with images you want to classify. Then run the Docker image as:

```sh
docker run -v $PWD:/data cnn_classify --gpu_id=-1 --batch_size=59 -m /opt/deeplearning/Models/lotsacars-20151202-170935-03d3/snapshot_iter_334500.caffemodel /data/image1.jpg /data/image2.jpg 2> /dev/null
```

The `2> /dev/null` at the end is optional, but reduces output to the result only. Caffe model setup outputs a lot of messages to `stderr` that the regular user will not be interested in.

Inside the Docker image, the `cnn_classify.py` script is run. It takes as main input a pre-trained model file and image data. Other options can be found in the help message of `cnn_classify.py -h`.