# Digits on DAS5
This manual will allow you to run a digits server on DAS5 with minimal installation. First log in to the headnode of das5.

> You currently need access to the home directory of Patrick and the scratch directory of Berend

## Install Anaconda

Download anaconda and run the installer script. When the installer asks you whether to add anaconda to your path I suggest you do (e.g. type yes)

    wget https://3230d63b5fc54e62148e-c95ac804525aac4b6dba79b00b39d1d3.ssl.cf1.rackcdn.com/Anaconda2-2.5.0-Linux-x86_64.sh
    sh Anaconda2-2.5.0-Linux-x86_64.sh
    
Update your .bashrc

    source .bashrc
    
Install the following conda packages

    conda install pillow protobuf Flask Flask-WTF gunicorn
    conda install --channel https://conda.anaconda.org/pmlandwehr flask-socketio
    pip install --user lmdb pydot2

## Copying DIGITS
Create a directory in you scratch folder (it will get pretty big while you're using DIGITS).

    cd /var/scratch/<username>
    mkdir git

Copy the following from Berend's scratch directory. The bash_profile file sets up the paths for running the digits server. The digits directory has the DIGITS server.

    cp /var/scratch/bweel/.bash_profile .
    cd git
    cp -r /var/scratch/bweel/git/digits .

# Running DIGITS server
## Interactive

Start up on a node with GPU and start the DIGITS server:

    srun --ntasks=1 --time=00:15:00 --gres=gpu:1 -C TitanX --pty bash -i

Please note the available time one can reserve a node. Standart is 15 mins, unless more time it's reserved in advance. Then --time should be adjusted accordingly.

Load the bash_profile to set the environment variables:

    . ~/.bash_profile

To actually access the server you need to get its ip-address, issue the following command and write down (or remember or copy) the ip address (eth0 is a good bet):

    ifconfig

Start the DIGITS server:

    ./digits-devserver


### Set up a tunnel to DAS5
To be able to access the digits server from your local machine you need to set up a proxy tunnel to das5 and update the proxy server of your web browser. On your local machine do:

     ssh -fTnN -D 8080 <username@DAS5>@fs0.das5.cs.vu.nl

*Please note that if 8080  us already in use, use another one, e.g. 8081. *
Now you can direct your browser to use localhost:8080 as a SOCKS proxy and browse to the ip address you wrote down earlier.
