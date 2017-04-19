==Kickstart files for spinning Fedora Live OS using Livemedia-Creator==

To use this files you need to install the lorax package.

This scripts need to be placed in the /usr/share/spin-kickstarts folder. We have built our LiveOS by modifying two files:
* ```livebase.ks``` - In this file we added the ssh keys and avocado package. If we want to use gnome for example,
we just need to include the livebase.
* ```fedora-testing-ws.ks``` - This is the stripped down version of Fedora Workstation. We removed the installer screen and libreoffice packages. This file includes de livebase.ws which
is a Fedora Live Base kickstart file with modifications.

Before spinning a LiveOS you need to make sure that SELinux is disabled by running: ```setenforce 0```


To spin the LiveOS run:
```sudo livemedia-creator --make-iso --no-virt --ks=./fedora-testing-ws.ks --macboot```.

After this command you will end up with an ISO which contains the LiveOS. The iso-to-pxe script can be used to put the iso on the pxe server (see https://github.com/daveol/Fedora-Test-Laptop/tree/master/iso-to-pxe).

For more information about the livemedia-creator: http://lorax.readthedocs.io/en/latest/livemedia-creator.html
