## Ansible playbook usage guide ##

Ansible should be configured with a [local-server] group in the network to configure
the DHCP/PXE server through ansible. Tweaking may be required based on IP addresses.
Depending on seperation of these servers additional config in the playbook may be
needed.

Running the playbook can be done with the following command

`$ ansible-playbook playbook.yml`
