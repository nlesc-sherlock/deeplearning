# Caffe Image Classifier Docker image

This Docker image is a wrapper around the `cnn_classify.py` script.

* **Input**:
	* a trained Caffe model 
	* an image or a batch of images. It runs the image(s) through the model in a forward pass
	* some parameters (see example below and `cnn_classify.py` for more)
* **Output**: the top 5 of predicted class and corresponding probabilities according to the model, per image.

## Pull

    docker pull nlesc/caffe_image_classify

## Build

    cd deeplearning/docker/caffe_image_classify
    docker build -t nlesc/caffe_image_classify .

## Run

In the command below, replace `$DATADIR` and `$MODELDIR` with the directory in which your image files reside and the directory in which your model files reside, respectively. E.g., one could use `MODELDIR=$GITBASE/deeplearning/Models/lotsacars-20151202-170935-03d3` (where `$GITBASE` is the location of your deeplearning git repo).

Then run it like:

    docker run \
        -v $PWD:/data \
        -v $MODELDIR:/model \
        caffe_image_classify \
        -v --gpu_id=-1 --batch_size=59 \
        -M /model --model_snapshot snapshot_iter_334500.caffemodel \
        -D /data \
        image1.jpg image2.jpg

For convenience, replace `image1.jpg image2.jpg` with `$(ls *.jpg)`.

In this example, the `snapshot_iter_334500.caffemodel` file from the `lotsacars-20151202-170935-03d3` model was used, replace this with the snapshot you want to use.

Optional: Put ` 2> /dev/null` at the end of the command to cut out all the Caffe model setup messages which it sends to `STDERR`.

Step by step, what this does (**TODO: UPDATE AFTER NEW VERSION**):

* `docker run` creates a Docker container out of a Docker image
* `-v $PWD:/data` takes the current working directory on the host (the one with your images, that you `cd`ed to, `$PWD`) and maps it to `/data` inside the Docker container.
* `nlesc/caffe_image_classify` is the name of the Docker image

All the options after the image name are passed on to the `cnn_classify.py` script that is run inside the Docker container. In this example:

* `-v` gives verbose output
* `--gpu_id` sets which GPU to use if the machine has multiple GPUs. The first GPU is `0`, etcetera. Leave this option out or set it to `-1` to use Caffe in CPU mode (default).
* `--batch_size` is a Caffe parameter that can be used to tune performance. Probably depends on your GPU architecture and on the number of images you want to process.
* `-m [MODELFILEPATH]` is a mandatory parameter that sets the model file path to `[MODELFILEPATH]`
* The last parameters are any number of image files, **BUT** their filenames have to be given as `/data/[IMAGEFILENAME]`, where `[IMAGEFILENAME]` is the basename of the image file path (i.e. without the directory). For instance, if you run the Docker container from a directory that contains image files `image1.jpg` and `image2.jpg`, the image filenames must be given as `/data/image1.jpg /data/image2.jpg`.
