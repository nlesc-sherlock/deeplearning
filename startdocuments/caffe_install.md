# These are the steps we did to install Caffe (NVIDIA flavour) on DAS-5

## Basics

Do this every time you want to build this stuff or run it:

```sh
module load cuda70/toolkit
module load cuda70/blas
module load hdf5_18/1.8.12
module load openblas
```

Edit these for your own installation paths:

```sh
export GITBASE=$HOME/git
export BUILDBASE=$HOME/build
export INSTALLITHERE=$HOME/sw
```

Possibly you'll need to setup an SSH key for GitHub on the machine first:
https://help.github.com/articles/generating-ssh-keys/


## EasyBuild

Following http://easybuild.readthedocs.org/en/latest/Installation.html (with a few additions):

```sh
export PATH=$PATH:/cm/local/apps/environment-modules/3.2.10/bin
EBPREFIX=$HOME/.local/easybuild
curl -O https://raw.githubusercontent.com/hpcugent/easybuild-framework/develop/easybuild/scripts/bootstrap_eb.py
python bootstrap_eb.py $EBPREFIX
module use $EBPREFIX/modules/all
module load EasyBuild
```

Add stuff to `~/.bash_profile`:

```sh
export EBPREFIX=$HOME/.local/easybuild

export PYTHONPATH=$HOME/.local/easybuild/software/EasyBuild/2.4.0/lib/python2.7/site-packages/:$PYTHONPATH

module use $EBPREFIX/modules/all
module load EasyBuild
```

Run some tests (load github key first? doesn't seem to make a difference...)

```sh
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa_github
ssh -T git@github.com

python -m test.framework.suite
python -m test.easyblocks.suite
python -m test.easyconfigs.suite
```

The last two didn't run for me.

### protobuf 2.5.0 with eb

```sh
eb protobuf-2.5.0.eb
module load protobuf
```

## Dependencies

### boost

Roughly following http://wiki.tiker.net/BoostInstallationHowto:

```sh
cd $BUILDBASE
wget http://downloads.sourceforge.net/project/boost/boost/1.59.0/boost_1_59_0.tar.bz2
mv boost_1_59_0.tar.bz2\?r\=http\:%2F%2Fsourceforge.net%2Fprojects%2Fboost%2Ffiles%2Fboost%2F1.59.0%2F boost_1_59_0.tar.bz2
tar xjf boost_1_59_0.tar.bz2
cd boost_1_59_0
./bootstrap.sh --prefix=$INSTALLITHERE --libdir=$INSTALLITHERE/lib
./b2 -j 16
./b2 install
```

### glog

```sh
cd $GITBASE
git clone git@github.com:google/glog.git
cd glog
git checkout tags/v0.3.4
touch configure.ac aclocal.m4 configure Makefile.am Makefile.in
./configure --prefix=$INSTALLITHERE
make
make install
```

### cmake

The version on DAS5 was too low for gflags (25 Nov 2015).

```sh
cd $BUILDBASE
wget https://cmake.org/files/v3.4/cmake-3.4.0.tar.gz
tar xzf cmake-3.4.0.tar.gz 
cd cmake-3.4.0
cmake . -DCMAKE_INSTALL_PREFIX:PATH=$INSTALLITHERE
make -j16
make install
```

Put in your `~/.profile` or `~/.bash_profile`:
```sh
export PATH=$INSTALLITHERE/bin:$PATH
```
Re-source it for the current session:
```sh
. ~/.bash_profile
```

### gflags

```sh
cd $GITBASE
git clone git@github.com:gflags/gflags.git
cd gflags
mkdir build && cd build
CXXFLAGS="-fPIC" cmake .. -DCMAKE_INSTALL_PREFIX:PATH=$INSTALLITHERE
make
make install
```

## Non-optional optional packages

The installation guide mentions a few packages as optional. This may be true
for the official Berkeley version (we didn't try that), but it certainly is not
for the NVIDIA version. The flags to turn off the optional dependencies are
missing in Makefile.config, so they can't be turned off the regular way. So,
let's just build them too.


### opencv2

```sh
cd $BUILDBASE
wget https://github.com/Itseez/opencv/archive/2.4.11.zip
mv 2.4.11.zip opencv_2.4.11.zip
unzip opencv_2.4.11.zip
cd opencv-2.4.11/
mkdir build
cd build/
cmake -D CMAKE_BUILD_TYPE=RELEASE -D CUDA_GENERATION=Kepler -D CMAKE_INSTALL_PREFIX=$INSTALLITHERE ..
make -j16
make install
```

### snappy

```sh
cd $GITBASE
git clone git@github.com:google/snappy.git
cd snappy/
./autogen.sh
./configure --prefix=$INSTALLITHERE
make -j16
make install
```

### leveldb

```sh
cd $GITBASE
git clone git@github.com:google/leveldb.git
cd leveldb
make -j16
cp libleveldb.* $INSTALLITHERE/lib
cp -r include/leveldb $INSTALLITHERE/include
```

### lmdb

```sh
cd $GITBASE
git clone git@github.com:LMDB/lmdb.git
cd lmdb/libraries/liblmdb
make -j16
cp liblmdb.* $INSTALLITHERE/lib
cp lmdb.h $INSTALLITHERE/include
```

## Actually optional

### cuDNN

For this you need to register for NVIDIA's developer/researcher program.
  Register here: https://developer.nvidia.com/cudnn, wait a day or two and
  download it from their webpage. Copy the file to DAS from your machine:

```sh
scp cudnn-7.0-linux-x64-v3.0-prod.tgz das5vu:./build/
```

and install:

```sh
cd $BUILDBASE
tar xzf cudnn-7.0-linux-x64-v3.0-prod.tgz
ln -s $BUILDBASE/cuda/lib64/* $INSTALLITHERE/lib/
ln -s $BUILDBASE/cuda/include/* $INSTALLITHERE/include/
```

Note that this installs the files as links, so keep the build dir there!


## Caffe-nv

We're using the NVIDIA version of Caffe, since we need that for DIGITS.

```sh
cd $GITBASE
git clone git@github.com:NVIDIA/caffe.git
mv caffe caffe_nv
cd caffe_nv
```

Build:

```sh
mkdir buildcmake
cd buildcmake
cmake .. -DCMAKE_INSTALL_PREFIX:PATH=$INSTALLITHERE

ccmake ..
```

In `ccmake`:
- We set BLAS to Open (Enter Enter). Press c.
- Two options:
  - Option 1:
  If you installed Anaconda Python, cmake will find a `ATLAS CBLAS` include dir
  and also the `OpenBLAS_INCLUDE_DIR` and `OpenBLAS_LIB` (press t to check if you
  like).
  We want to fill in `BLAS_INCLUDE` and `BLAS_LIB` ourselves, so press t (advanced)
  and scroll down until you find them.
  - Option 2:
  You get an error saying it can't find openblas. Press e. `BLAS_INCLUDE` and
  `BLAS_LIB` will now show on top as `BLABLA-NOTFOUND`.
  Fill in the openblas paths from `module show openblas`:
```sh
    BLAS_INCLUDE := /cm/shared/apps/openblas/0.2.8/include/openblas
    BLAS_LIB := /cm/shared/apps/openblas/0.2.8/lib/libopenblas.so
```
- Then press c again twice. Press g to generate and exit.

```sh
make all -j16
```

It might happen that you get errors like:

```sh
... compilation terminated.
The bug is not reproducible, so it is likely a hardware or OS problem.
```
  This is a race condition thing; apparently the caffe `Makefile` isn't robust
  enough to do multiple jobs (-j16). Just run again and it'll likely be
  fixed.

```sh
make install
```

Add `$INSTALLITHERE` to `PYTHONPATH` in `~/.profile` or `~/.bash_profile`:

```sh
PYTHONPATH=$HOME/sw/lib/python2.7/site-packages:$PYTHONPATH
PYTHONPATH=$HOME/sw/python:$PYTHONPATH
PYTHONPATH=$HOME/.local/lib/python2.7/site-packages:$PYTHONPATH

export PYTHONPATH
```

## DIGITS

Web-based front-end to Caffe-nv.

First we install some Python modules with anaconda. Not with pip as the
  package authors suggest, since then we have to compile SciPy, for which we
  need to point pip to BLAS libraries at non-default locations. Anaconda is less
  of a hassle.

```sh
cd $BUILDBASE
wget https://3230d63b5fc54e62148e-c95ac804525aac4b6dba79b00b39d1d3.ssl.cf1.rackcdn.com/Anaconda2-2.4.0-Linux-x86_64.sh
sh Anaconda2-2.4.0-Linux-x86_64.sh
```

Follow the instructions to install Anaconda. Logout, login. Reload the modules
  and export the paths (top of the file). Then:

```sh
conda install pillow protobuf Flask Flask-WTF gunicorn
conda install --channel https://conda.anaconda.org/pmlandwehr flask-socketio
pip install --user lmdb pydot2

cd $GITBASE
git clone git@github.com:NVIDIA/DIGITS.git digits
cd digits
pip install --user -r requirements.txt
```

That's it for installation!
