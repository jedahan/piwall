# piwall setup

### Install raspbian

Download and burn raspbian onto an sd card, from your local machine

    curl -OL http://downloads.raspberrypi.org/raspbian_latest -o raspbian.zip
    unzip raspbian.zip
    sudo diskutil umount /dev/rdisk1s1
    sudo dd bs=1m if=2014-06-20-wheezy-raspbian.img of=/dev/rdisk1
    sudo diskutil umount /dev/rdisk1s1
    sudo diskutil eject /dev/rdisk1

### Configure raspbian

Use raspi-config to change the keyboard layout and enable ssh.
Now, update everything.

    sudo apt-get update
    sudo apt-get upgrade

### Add a shared partition

Add a 0B (W95 FAT32) partition where the free space was

    sudo apt-get install dosfstools
    sudo cfdisk /dev/mmcblk0
    sudo reboot

Mount as /shared on boot

    sudo mkfs.msdos /dev/mmcblk0p3
    sudo mkdir /shared
    sudo chown pi:pi /shared
    sudo sh -c "echo '/dev/mmcblk0p3    /mnt/storage    vfat    auto,rw,user,users,exec,noatime,uid=1000,gid=1000,umask=000    0    0' >> /etc/fstab"
    sudo mount -a

### Clone this respository

    git clone https://github.com/jedahan/piwall.git
    cd piwall

### Install the shared files

    cp -r shared/* /shared

### Install a splash screen

    sudo apt-get install fbi
    sudo cp -r initscripts/asplashscreen /etc/init.d
    sudo update-rc.d asplashscreen defaults


### Install piwall

These packages were downloaded from [dl.piwall.co.uk](dl.piwall.co.uk)

    sudo dpkg -i packages/*

### Configure the server

Make sure we can convert video

    sudo apt-get install libav-tools

Install the init script

    sudo cp -r initscripts/piwallserver /etc/init.d
    sudo update-rc.d piwallserver defaults

### Configure the tiles

    sudo cp -r initscripts/piwalltile /etc/init.d
    sudo update-rc.d piwalltile defaults
