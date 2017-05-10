import subprocess as subp
import yaml



def pingtest(ip, interface):
    """pingtest checks whether the IP is reachable on the given
    interface using a single ICMP ping.

    :param ip: The IP address to ping
    :param interface: The interface to use as the origin for the ping
    :return: True on success
    """
    response = subp.call(['ping', '-I', interface, ip, '-c', '1'])

    if (re
    return subp.call(['ping', '-I', interface, ip, '-c', '1'])

def pingtest_hard(ip, interface, test_class):
    """pingtest checks whether the IP is reachable on the given
    interface using a single ICMP ping.

    :param ip: The IP address to ping
    :param interface: The interface to use as the origin for the ping
    :param test_class: The origin Test class from which the function
                       was called
    """
    fail = subp.call(['ping', '-I', interface, ip, '-c', '1'])
    if fail != 0:
       test_class.fail("Ping on interface {0} to ip {1} failed".format(interface, ip));

# should be moved to a more generic class
def load_yaml(test_class, path):
    with open(path, 'r') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exc:
            test_class.log.debug(exc)

# returns a list of known (existing) networks in the system
def get_known():
    return subp.Popen(['nmcli', '-t', '--fields', 'NAME,UUID,ACTIVE,TYPE', 'c'], stdout=subp.PIPE, stderr=subp.PIPE)

# returns the ssid of the connected ssid on the given interface
def connected_to(interface):
    # get the SSID connected on the interface
    connectedP = subp.Popen(['iwgetid', interface, '-r'], stdout=subp.PIPE, stderr=subp.PIPE)
    stdout, stderr = connectedP.communicate()
    # return stdout with trimmed whitespace = connected ssid
    return stdout.rstrip()
""" 
connects to a ssid, based on whether it exists.
if it doesn't, makes a new connection, otherwise
uses the existing
""" 

def connect(ssid, password):
    knownNetworks = InternetUtils.get_known()

    stdout, stderr = knownNetworks.communicate()

    # each connection is seperated by '\n'
    connectionList = stdout.split("\n")
    existing = False

    """ 
    we check for the existance of the ssid in the known networks
    if the network ssid is found, it will connect using its UUID
    if not found, a new connection will be created and connected to
    """
    for con in connectionList:
        cParts = con.split(":") # nmcli -t output is seperated by :
        # see if the ssid exist, and has the correct type
        if ssid in cParts and cParts[3] == "802-11-wireless":
           existing = True
           if cParts[2] != "yes": # yes means active => don't reconnect
              subp.call(['nmcli', 'con', 'up', 'uuid', cParts[1]]) # cParts[1] contains uuid

    # when the network does not yet exist, create a new one
    if existing == False:
        switch = subp.call(['nmcli', 'dev', 'wifi', 'con', ssid, 'password', password])        
