import subprocess as subp
import re
from gi.repository import NM

import gi
gi.require_version('NM', '1.0')
from gi.repository import GLib, NM, GObject
import sys, uuid

main_loop = None

def _ssid_to_utf8(ap):
    """
    Convert ssid to utf8 for human readability. An SSID can contain
    non-printable characters, NM has a util to convert.

    :param: ap NMAccessPoint
    :return: utf8 string containing the SSID
    """
    ssid = ap.get_ssid()
    if not ssid:
        return ""
    return NM.utils_ssid_to_utf8(ssid.get_data())

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
       test_class.fail("Ping on interface {0} to ip {1} failed".format(interface, ip))

def get_known():
    """
    Finds a list of known (existing) networks connections in the system
    
    :return: The list of known networks
    
    """
    client = NM.Client.new(None);
    connections = client.get_connections()
    return connections

def connect(ssid, password, test_class):
    """ 
    Connects to a ssid, based on whether it exists.
    if it doesn't, makes a new connection, otherwise
    uses the existing
    
    :param ssid: The ssid to connect to
    :param password: The password of the AP to connect to, if needed
    
    """ 
    knownNetworks = get_known()

    existing = False

    """ 
    we check for the existance of the ssid in the known networks
    if the network ssid is found, it will connect using its UUID
    if not found, a new connection will be created and connected to
    """
    global main_loop
    main_loop = GLib.MainLoop()
    wifi_dev = get_active_device("wifi", test_class)
    for con in knownNetworks:
        # see if the ssid exist, and has the correct type
        if con.get_id() == ssid and con.get_connection_type() == "802-11-wireless":
            existing = True
            connected = False
            client = NM.Client.new(None)
            client.activate_connection_async(con, wifi_dev, None, None, add_c_finish, connected)
            main_loop.run()

    # when the network does not yet exist, create a new one
    if existing == False:
        client = NM.Client.new(None)
        con = create_wifi_profile(ssid, password, test_class)
        connected = False
        client.add_and_activate_connection_async(con, wifi_dev, None, None, add_c_finish, connected)

        main_loop.run()
     
    if connected == 0:
        return True
    return False

def get_wifi_device():
    nmc = NM.Client.new(None)
    devs = nmc.get_devices()

    for dev in devs:
        if dev.get_device_type() == NM.DeviceType.WIFI:
            if  dev.get_state() == NM.DeviceState.ACTIVATED:
                return dev

def add_c_finish(client, result, data):
    """
    Callback for finished activation connection
    """
    try:
        client.add_connection_finish(result)
        connected = True
    except Exception, e:
        pass
    global main_loop
    main_loop.quit()

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

    test_class.log.debug(gatewayP1)
    if gatewayMatches == None:
        return 0
    gateway = gatewayMatches.group(1)
    return gateway

def get_active_device(if_type, test_class):
    """
    Gets the active network adapter of the given type

    :param if_type: The type of interface to look for (e.g. wifi)
    :param test_class: The class to fail when nothing is found
    :return: First interface of type if_type that is ACTIVATED
    
    """
    devtype = "NM.DeviceType." + if_type.upper()
    devtype = eval(devtype)

    nmc = NM.Client.new(None)
    devs = nmc.get_devices()
    active_states = [NM.DeviceState.ACTIVATED, NM.DeviceState.DISCONNECTED]

    for dev in devs:
        if (dev.get_device_type() != devtype or
            dev.get_state() not in active_states):
            continue
        return dev

    test_class.fail("No activated adapter found of type {0}".format(if_type))

def create_wifi_profile(ssid, password, test_class):
    """
    To be documented.

    :param: ssid The SSID to connect with
    :param: password password of the SSID if needed
    """
    profile = NM.SimpleConnection.new()
    s_con = NM.SettingConnection.new()
    s_wireless = NM.SettingWireless.new()
    s_wireless.set_property(NM.SETTING_WIRELESS_SSID, GLib.Bytes(ssid))
    s_con.set_property(NM.SETTING_CONNECTION_ID, ssid)
    s_con.set_property(NM.SETTING_CONNECTION_UUID, str(uuid.uuid4()))
    s_con.set_property(NM.SETTING_CONNECTION_TYPE, "802-11-wireless")
    
    wifi_dev = get_active_device("wifi", test_class)

    aps = NM.DeviceWifi.get_access_points(wifi_dev)
    ap = False
    # Fetch ap by SSID
    for ap_candidate in aps:
        ssid_tmp = _ssid_to_utf8(ap_candidate)
        if (ssid_tmp == ssid):
            ap = ap_candidate
            break
    if not ap:
        test_class.fail("No such AP found with SSID: {0}".format(ssid))

    ap_flags = NM.AccessPoint.get_flags (ap);
    ap_wpa_flags = NM.AccessPoint.get_wpa_flags (ap);
    ap_rsn_flags = NM.AccessPoint.get_rsn_flags (ap);
    # dirty fix for getting this flag enum bug, see:
    # https://bugzilla.redhat.com/show_bug.cgi?format=multiple&id=767998
    ap_flag_enum = getattr(NM, "80211ApFlags")

    # check For WEP/WPA-PSK security
    if ap_flag_enum.PRIVACY == ap_flags:
        s_wireless_sec = NM.SettingWirelessSecurity.new()
        NM.Connection.add_setting(profile, s_wireless_sec)
        # getting more security flags
        sec_enum = getattr(NM, "80211ApSecurityFlags")
        
        if (sec_enum.NONE == ap_wpa_flags and
            sec_enum.NONE == ap_rsn_flags):
            # WEP security, add to security object
            s_wireless_sec.set_property(NM.SETTING_WIRELESS_SECURITY_KEY_MGMT, "none");
        elif (sec_enum.KEY_MGMT_802_1X is not ap_wpa_flags and
              sec_enum.KEY_MGMT_802_1X is not ap_rsn_flags):
            # WPA security, add to security object
            s_wireless_sec.set_property(NM.SETTING_WIRELESS_SECURITY_PSK, password);
            s_wireless_sec.set_property(NM.SETTING_WIRELESS_SECURITY_KEY_MGMT, "wpa-psk");


    s_ip4 = NM.SettingIP4Config.new()
    s_ip4.set_property(NM.SETTING_IP_CONFIG_METHOD, "auto")

    s_ip6 = NM.SettingIP6Config.new()
    s_ip6.set_property(NM.SETTING_IP_CONFIG_METHOD, "auto")

    profile.add_setting(s_con)
    profile.add_setting(s_ip4)
    profile.add_setting(s_ip6)
    profile.add_setting(s_wireless)
    profile.add_setting(s_wireless_sec)


    return profile

