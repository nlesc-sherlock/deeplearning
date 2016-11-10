Download newest release from https://github.com/NVIDIA/DIGITS/releases
Unpack and `cd` into directory. E.g.:

```bash
wget https://github.com/NVIDIA/DIGITS/archive/v5.0.0-rc.1.tar.gz
tar xzf v5.0.0-rc.1.tar.gz
cd DIGITS-5.0.0-rc.1
```

_Loosely following [this guide](https://github.com/NVIDIA/DIGITS/blob/master/docs/BuildCaffe.md) do this stuff_:

Download cuDNN from https://developer.nvidia.com/rdp/form/cudnn-download-survey and install it according to the install instructions there, which basically just amount to:

- extracting the downloaded archive somewhere and
- adding the path where you extracted it to LD_LIBRARY_PATH
- (for the following, make sure it is also exported into LD_LIBRARY_PATH, e.g. by manually adding it or by logging in again if you put it in `~/.bashrc`)
- also make sure that if you have an older version installed, you remove that entry from the LD_LIBRARY_PATH, otherwise cmake for Caffe later on may not find the correct version

Download Caffe and set a CAFFE_ROOT shell variable so DIGITS can find it easier:
```bash
export CAFFE_ROOT=~/caffe
git clone https://github.com/NVIDIA/caffe.git $CAFFE_ROOT
```

Create a new conda environment and activate it, e.g.:

```bash
conda create --name digits5 python
source activate digits5
```

Install Caffe requirements:

```bash
while read requirement; do conda install --yes $requirement; done < $CAFFE_ROOT/python/requirements.txt
```

Load CUDA 8 modules:

```bash
module load cuda80
```

Another Caffe requirement is OpenCV, which we need to compile against the CUDA stuff:

```bash
export INSTALLITHERE=$HOME/sw
```

```bash
wget https://github.com/Itseez/opencv/archive/2.4.13.zip
mv 2.4.13.zip opencv_2.4.13.zip
unzip opencv_2.4.13.zip
cd opencv-2.4.13/
mkdir build
cd build/
cmake -D CMAKE_BUILD_TYPE=RELEASE -D CUDA_GENERATION=Kepler -D CMAKE_INSTALL_PREFIX=$INSTALLITHERE ..
make -j32
make install
```


Install DIGITS requirements (scikit-fmm is not in conda, apparently, so do that with pip):

```bash
while read requirement; do conda install --yes $requirement; done < requirements.txt
pip install scikit-fmm>=0.0.9
```

