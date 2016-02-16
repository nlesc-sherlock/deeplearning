# Setting up VM on SURFsara HPC Cloud

## Create VM

Set up SSH key on your account:
https://doc.hpccloud.surfsara.nl/SSHkey

Follow "Import appliances from the AppMarket" and "Adding a GPU device to your VM" sections at:
http://doc.hpccloud.surfsara.nl/gpu-attach
But don't launch the VM yet!

Actually, in the above step you can also add two GPUs to the template.

The AppMarket image is unfortunately too small to fit all software we need. We will use instead the 50GB image that @nielsdrost created. Clone this image (called `sherlock-os-hdd-50Gb-master-image`). In the advanced cloning options, put the image on the `images_ssd_gpu` datastore.

Set image to persistent:
https://doc.hpccloud.surfsara.nl/image_persistence

Update the template created from the AppMarket to use this newly cloned image.

Then instantiate the template.

## Login

    ssh -i .ssh/id_rsa root@145.100.59.54

Using root access you can make new accounts (`adduser [USERNAME]` and then `adduser [USERNAME] sudo` to add the user to the sudoers group).

Now you can login using any of the accounts you created.

Note: when using the default SURFsara VM from the AppMarket (not this 50GB one), the only user you can login as is ubuntu, which has sudo-rights. However, this VM template has disabled SSH password login, so to enable that edit the file '/etc/ssh/sshd_config' and modify or add the line 'PasswordAuthentication yes
'.  Changes only have effect after restarting: `sudo service ssh restart`.

## Update

Since we're not using the SURFsara maintained image/template, we have to manually update our Ubuntu installation.

    sudo apt-get update
    sudo apt-get upgrade
    sudo apt-get dist-upgrade

## Add data disk

The default Ubuntu 14.04 image is still only 50GB, so to save data one has to add a data image.

Follow https://doc.hpccloud.surfsara.nl/create-datablocks. One difference, we do:

    echo "echo 4096 > /sys/block/vdb/queue/read_ahead_kb" > /etc/rc.local

Since `/etc/rc.local` already exists, we don't need to `touch /etc/rc.d/rc.local`. It already has the right permissions as well, so don't do the `chmod` command either.

We also follow the suggestion to add `/dev/vdb /data xfs defaults 0 0` to `/etc/fstab`.

## Install Docker

Follow instructions at https://docs.docker.com/engine/installation/linux/ubuntulinux/

From the optional instructions: `sudo usermod -aG docker [USERNAME]`

## Install NVIDIA drivers

    sudo apt-get install ubuntu-drivers-common

Then run the following command to find the proprietary drivers that are available for installing via `apt-get`:

    sudo ubuntu-drivers devices

Which should give something like:

    == /sys/devices/pci0000:00/0000:00:06.0 ==
    vendor   : NVIDIA Corporation
    model    : GK104GL [GRID K2]
    modalias : pci:v000010DEd000011BFsv000010DEsd0000100Abc03sc00i00
    driver   : nvidia-340 - distro non-free
    driver   : nvidia-352-updates - distro non-free
    driver   : nvidia-304-updates - distro non-free
    driver   : nvidia-352 - distro non-free recommended
    driver   : xserver-xorg-video-nouveau - distro free builtin
    driver   : nvidia-304 - distro non-free
    driver   : nvidia-340-updates - distro non-free

Pick the newest driver (usually) and install it, in our case:

    sudo apt-get install nvidia-352

Then reboot the VM. Once it's restarted, you can check whether the driver is loaded with:

    lspci -vnn | grep -i VGA -A 12

Which should show that the `nvidia` driver is in use, instead of the default `nouveau` driver.

# Untested scratch/work-in-progress part of this document

## Install DIGITS Docker container

    sudo apt-get install git
    git clone https://github.com/NVIDIA/nvidia-docker.git
    
Follow the quick start instructions at https://github.com/NVIDIA/nvidia-docker.

## Start DIGITS container

    nvidia-docker run digits
