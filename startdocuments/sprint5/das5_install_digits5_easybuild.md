## Install Easybuild

```bash
wget https://raw.githubusercontent.com/hpcugent/easybuild-framework/develop/easybuild/scripts/bootstrap_eb.py
EASYBUILD_PREFIX=$HOME/.local/easybuild
python bootstrap_eb.py $EASYBUILD_PREFIX
module use $EASYBUILD_PREFIX/modules/all
module load EasyBuild
rm bootstrap_eb.py
```

Put some of that in your `~/.bashrc` file to automatically load it during login:

```
export EASYBUILD_PREFIX=$HOME/.local/easybuild
module use $EASYBUILD_PREFIX/modules/all
module load EasyBuild
```

## Install Caffe dependencies

Note that below we use the `--robot` option, which also automatically installs dependencies through easybuild. It will not try to detect whether dependencies are already installed on the system, so there will likely be considerable overhead in here, up to the point of installing GCC, Python and other nonsense. You could try to figure out the exact packages that are strictly necessary and I did that for some packages but not all.

Actually, after some fiddling with this, it seems Easybuild is not at all that easy. Many "packages" (the easyconfig .eb files) are slightly broken, there doesn't seem to be an option to specify that you need 'package X with *at least* version Y', meaning that many redundant packages with specific versions will be installed, downloading zips sometimes fails, etc.

### tl;dr

```bash
RTFM NOOB
```

### HDF5

```bash
eb HDF5-1.8.17-foss-2016a.eb --robot
```

This uses the 

#### When HDF5 fails on GCC

HDF5 depends on GCC, but the GCC easybuilds have some issues, so manually download the necessary files. _(The eb file here is `$EASYBUILD_PREFIX/software/EasyBuild/2.9.0/lib/python2.7/site-packages/easybuild_easyconfigs-2.9.0-py2.7.egg/easybuild/easyconfigs/g/GCCcore/GCCcore-4.9.3.eb`, possibly other files have to be manually downloaded, it seems random which files fail.)_

```bash
cd $EASYBUILD_PREFIX/sources/g/GCCcore/
rm gmp-6.0.0a.tar.bz2
wget http://ftp.snt.utwente.nl/pub/software/gnu/gmp/gmp-6.0.0a.tar.bz2
rm mpfr-3.1.2.tar.gz
wget http://ftp.snt.utwente.nl/pub/software/gnu/mpfr/mpfr-3.1.2.tar.gz
```

Then restart the HDF5 installation:

```bash
eb HDF5-1.8.17-foss-2016a.eb --robot
```

### Protobuf

```bash
eb protobuf-3.0.2-foss-2016a.eb
```

### Boost

```bash
eb Boost-1.61.0-intel-2016a.eb
```



### cuDNN ("optional")

Download cuDNN from https://developer.nvidia.com/rdp/form/cudnn-download-survey and install it according to the install instructions there, which amount to:

- extracting the downloaded archive somewhere, e.g. `mkdir $HOME/cudnn8-5.1; cd $HOME/cudnn8-5.1; tar xzf [cudnn-archive]`, and
- adding the path where you extracted it to LD_LIBRARY_PATH, in this example: `LD_LIBRARY_PATH=$HOME/cudnn8-5.1/cuda/lib64:$LD_LIBRARY_PATH`
- (for the following, make sure it is also exported into LD_LIBRARY_PATH, e.g. by manually adding it or by logging in again if you put it in `~/.bashrc`)
- also make sure that if you have an older version installed, you remove that entry from the LD_LIBRARY_PATH, otherwise cmake for Caffe may not find the correct version

