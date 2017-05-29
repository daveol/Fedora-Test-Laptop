%packages
#based on the fedora workstation packages.ks but without libreoffice and firefox
# Exclude unwanted groups that fedora-live-base.ks pulls in
-@dial-up
-@input-methods
-@standard

# Make sure to sync any additions / removals done here with
# workstation-product-environment in comps
@base-x
@core
@fonts
@gnome-desktop
@guest-desktop-agents
@hardware-support
@networkmanager-submodules
@printing
@workstation-product

# Branding for the installer
fedora-productimg-workstation

# Exclude unwanted packages from @anaconda-tools group
-gfs2-utils
-reiserfs-utils

%end

