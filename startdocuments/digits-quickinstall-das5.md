# Digits on DAS5
This manual will allow you to run a digits server on DAS5 with minimal installation.

> You currently need access to the home directory of Patrick and the scratch directory of Berend

## Install Anaconda

Download anaconda and run the installer script. When the installer asks you whether to add anaconda to your path I suggest you do (e.g. type yes)

    wget https://3230d63b5fc54e62148e-c95ac804525aac4b6dba79b00b39d1d3.ssl.cf1.rackcdn.com/Anaconda2-2.5.0-Linux-x86_64.sh
    sh Anaconda2-2.5.0-Linux-x86_64.sh
    export BLAAT=blaat

Install the following conda packages

    conda install pillow protobuf Flask Flask-WTF gunicorn
    conda install --channel https://conda.anaconda.org/pmlandwehr flask-socketio
    pip install --user lmdb pydot2

## Copying digits
Create a directory in you scratch folder (it will get pretty big while you're using digits).

    cd /var/scratch/<username>
    mkdir git

Copy the following from Berend's scratch directory. The bash_profile file sets up the paths for running the digits server. The digits diretory has the digits server.

    cp /var/scratch/bweel/.bash_profile .
    cd git
    cp -r /var/scratch/bweel/git/digits .

# Running digits server
## interactive

Start up on a node with GPU and start the DIGITS server:

    srun --ntasks=1 --time=00:15:00 --gres=gpu:1 -C TitanX --pty bash -i

Load the bash_profile to set the environment variables:

    . ~/.bash_profile

Start the digits server:

    ./digits-devserver
