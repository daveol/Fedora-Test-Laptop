==ISO to PXE script explaination and usage instructions==

***Should be run after generating a new testing ISO.

This script will be used to unpack the file system from an ISO (generated from kickstart files)
and move the files of interest to appropriate location. These files are requisit for booting PXE.
The files and the dirs they will be moved to are listed below.

Usage of command arguments:

      -i ISO_FILE --  The ISO file location to be unpacked
      -t TFTP_DIR --  This is the dir in which the TFTP files are stored, pxelinux.0 file should be 
                      located here. The new kernel (vmlinuz) will be stored in this dir in under the
                      NAME folder.
      -w WEB_DIR  --  This is the url at which the PXE server is hosted and the squashfs.img will
                      be stored.
      -n NAME     --  This is the general name of the newly created image.
