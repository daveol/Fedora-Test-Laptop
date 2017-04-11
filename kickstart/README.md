==Kickstart files for spinning Fedora Live OS using Livemedia-Creator==

This scripts need to be placed in the /usr/share/spin-kickstarts folder.
To make this work the packages: 

* ```fedora-testing-ws.ks``` - Is the stripped down workstation of Fedora. This file includes de livebase.ws which
is a Fedora Live Base kickstart file with modifications.
* ```livebase.ks``` - In this file we added the ssh keys and avocado package. If we want to use gnome for example,
we just need to include the livebase.

Before spinning a Live OS you need to make sure that SELinux is disabled by ```setenforce 0```
To spin the Live OS run
```sudo livemedia-creator --make-iso --no-virt --ks=./fedora-testing-ws.ks --macboot```.

This will give you a complete Bootable ISO which you can either burn to a USB stick and boot from, or use the script
to extract the iso and place the SquashFS, Kernel and Initramfs on the server.
