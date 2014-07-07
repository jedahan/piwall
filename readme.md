# Changing the videos and splash screens

## Changing the video

Place test.avi in the 'Untitled' volume.

## Changing the splash screen

Place splash.jpg in the 'Untitled' volume. It will take 2 full boots for the screen to be fully updated.

# Setting up from scratch

Here are all the steps required to get from a blank sd card to this working setup.

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

### Clone this respository

    git clone https://github.com/jedahan/piwall.git
    cd piwall

### Update the distribution

    sudo apt-get update
    sudo apt-get upgrade
    sudo rpi-update

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

### Install the shared files

    cp shared/* /shared/

### Install a splash screen & the splash screen updater

    sudo apt-get install fbi
    sudo cp -r initscripts/splashscreen /etc/init.d
    sudo update-rc.d asplashscreen defaults
    sudo cp -r initscripts/updatesplash /etc/init.d
    sudo update-rc.d updatesplash defaults

### Hide the boot text

    sudo sed -e 's/tty1/tty3' -e 's/$/ loglevel=3 vt.global_cursor_default=0 logo.nologo' -i /boot/cmdline.txt

### Install piwall

These packages were downloaded from [dl.piwall.co.uk](dl.piwall.co.uk)

    sudo dpkg -i packages/*

## For each the tiles

Install the init script

    sudo cp -r init/*tile* /etc/init.d
    sudo update-rc.d piwalltile defaults

Change the config to be correct for each tile

    sudo nano /etc/init.d/starttile.sh
    cp .piwall /home/pi

Copy the appropriate config for the left or right tile

    cp .pitile-left /home/pi/.pitile

## For the Server

Make sure we can convert video

    sudo apt-get install libav-tools

Install the init script

    sudo cp -r initscripts/*server* /etc/init.d
    sudo update-rc.d piwallserver defaults

### Change the networking

Install the network changing scripts

    sudo cp /etc/network/interfaces{,.bak}
    alias lan=/home/pi/piwall/network/localnetwork.sh
    alias wan=/home/pi/piwall/network/globalnetwork.sh

Make sure to choose different octets for each pi

    nano network/interfaces.local

Now you can switch just by doing `lan` or `wan`

    lan
