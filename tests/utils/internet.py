import subprocess as subp
import re

from gi.repository import GLib, NetworkManager, NMClient

def pingtest(ip, interface):
    """
    pingtest checks whether the IP is reachable on the given
    interface using a single ICMP ping.

    :param ip: The IP address to ping
    :param interface: The interface to use as the origin for the ping
    :return: True on success
    
    """
    response = subp.call(['ping', '-I', interface, ip, '-c', '1'])

    if response == 0:
        return True
    return False

def pingtest_hard(ip, interface, test_class):
    """
    pingtest_hard checks whether the IP is reachable on the given
    interface using a single ICMP ping. Same as pingtest, but throws
    exception on fail.

    :param ip: The IP address to ping
    :param interface: The interface to use as the origin for the ping
    :param test_class: The origin Test class from which the function
                       was called
    """
    success = pingtest(ip, interface)
    if success == False:
       test_class.fail("Ping on interface {0} to ip {1} failed".format(interface, ip));

def get_known(type = ""):
    """
    Returns a list of known (existing) networks in the system
    
    :return: The list of known networks
    
    """
    settings = NMClient.RemoteSettings.new(None);
    connections = settings.list_connections()
    return connections

def connect(ssid, password):
    """ 
    Connects to a ssid, based on whether it exists.
    if it doesn't, makes a new connection, otherwise
    uses the existing
    
    :param ssid: The ssid to connect to
    :param password: The password of the AP to connect to
    
    """ 
    knownNetworks = get_known()

    existing = False

    """ 
    we check for the existance of the ssid in the known networks
    if the network ssid is found, it will connect using its UUID
    if not found, a new connection will be created and connected to
    """
    for con in knownNetworks:
        #cParts = con.split(":") # nmcli -t output is seperated by :
        # see if the ssid exist, and has the correct type
        if con.get_id() == ssid and con.get_connection_type() == "802-11-wireless":
           existing = True
           connected = subp.call(['nmcli', 'con', 'up', 'uuid', con.get_uuid()]) # cParts[1] contains uuid

    # when the network does not yet exist, create a new one
    if existing == False:
        connected = subp.call(['nmcli', 'dev', 'wifi', 'con', ssid, 'password', password])   

    if connected == 0:
        return True
    return False

def get_gateway(interface, test_class):
    """
    Gets the default gateway of the given interface
    
    :param interface: The interface on which to get
    :param test_class: The class to fail when something goes wrong
    :return: String of gateway
    
    """
    # get the default gateway by parsing ip route's output
    gatewayP1 = subp.Popen(['ip', 'route', 'show', 'dev', interface], stdout=subp.PIPE, stderr=subp.PIPE).communicate()[0]
    gatewayMatches = re.search(r'^default\s+via\s+(?P<gw>[^\s]*)\s', gatewayP1, re.MULTILINE)
    
    if gatewayMatches == None:
        return 0;
    gateway = gatewayMatches.group(1)
    
    return gateway
