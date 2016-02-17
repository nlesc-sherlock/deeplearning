# *(Image, Model) -> Class* Docker image

## Build

    cd deeplearning/caffe_nv_docker
    docker build -t cnn_classify .

## Run

`cd` to directory with your images, then:

    docker run -v $PWD:/data cnn_classify -v --gpu_id=-1 --batch_size=59 -m /opt/deeplearning/Models/lotsacars-20151202-170935-03d3/snapshot_iter_334500.caffemodel /data/image1.jpg /data/image2.jpg

Optional: Put ` 2> /dev/null` at the end of the command to cut out all the Caffe model setup messages which it sends to `STDERR`.

Step by step, what this does:

* `docker run` creates a Docker container out of a Docker image
* `-v $PWD:/data` takes the current working directory on the host (the one with your images, that you `cd`ed to, `$PWD`) and maps it to `/data` inside the Docker container.
* `cnn_classify` is the name of the Docker image

All the options after the image name are passed on to the `cnn_classify.py` script that is run inside the Docker container. In this example:

* `-v` gives verbose output
* `--gpu_id` sets which GPU to use if the machine has multiple GPUs. The first GPU is `0`, etcetera. Leave this option out or set it to `-1` to use Caffe in CPU mode (default).
* `--batch_size` is a Caffe parameter that can be used to tune performance. Probably depends on your GPU architecture and on the number of images you want to process.
* `-m [MODELFILEPATH]` is a mandatory parameter that sets the model file path to `[MODELFILEPATH]`
* The last parameters are any number of image files, **BUT** their filenames have to be given as `/data/[IMAGEFILENAME]`, where `[IMAGEFILENAME]` is the basename of the image file path (i.e. without the directory). For instance, if you run the Docker container from a directory that contains image files `image1.jpg` and `image2.jpg`, the image filenames must be given as `/data/image1.jpg /data/image2.jpg`.