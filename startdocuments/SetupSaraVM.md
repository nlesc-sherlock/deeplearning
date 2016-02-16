# Setting up VM on SURFsara HPC Cloud

## Create VM

Set up SSH key on your account:
https://doc.hpccloud.surfsara.nl/SSHkey

Follow "Import appliances from the AppMarket" and "Adding a GPU device to your VM" sections at:
http://doc.hpccloud.surfsara.nl/gpu-attach
But don't launch the VM yet!

Set image to persistent:
https://doc.hpccloud.surfsara.nl/image_persistence

Then instantiate the template.

## Login

    ssh -i .ssh/id_rsa ubuntu@145.100.59.54

The ubuntu user has sudo rights. Using this user you can make new accounts (`sudo adduser [USERNAME]` and then `sudo adduser [USERNAME] sudo` to add the user to the sudoers group). However, this VM template has disabled SSH password login, so to enable that edit the file '/etc/ssh/sshd_config' and modify or add the line 'PasswordAuthentication yes
'. 
Changes only have effect after restarting: `sudo service ssh restart`.

Now you can login using any of the accounts you created.

## Add data disk

The default Ubuntu 14.04 image is only 10GB, so to save data one has to add a data image.

Follow https://doc.hpccloud.surfsara.nl/create-datablocks. One difference, we do:

    echo "echo 4096 > /sys/block/vdb/queue/read_ahead_kb" > /etc/rc.local

Since `/etc/rc.local` already exists, we don't need to `touch /etc/rc.d/rc.local`. It already has the right permissions as well, so don't do the `chmod` command either.

We also follow the suggestion to add `/dev/vdb /data xfs defaults 0 0` to `/etc/fstab`.
