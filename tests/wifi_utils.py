import subprocess as subp
import yaml

class WifiUtils():
    """ 
    Should be integrated in fed_laptoptest/ ?

    A utility class for tests which make use of common commands for wifi
    functionality
    """
    @staticmethod
    # the pingtest method sees if response succeeds on a single ping on
    # the given interface
    def pingtest(ip, interface):
        return subp.call(['ping', '-I', interface, ip, '-c', '1'])

    @staticmethod # should be moved to a more generic class
    def load_yaml(master, path):
        with open(path, 'r') as stream:
            try:
                return yaml.load(stream)
            except yaml.YAMLError as exc:
                master.log.debug(exc)
    @staticmethod
    # returns a list of known (existing) networks in the system
    def get_known():
        return subp.Popen(['nmcli', '-t', '--fields', 'NAME,UUID,ACTIVE,TYPE', 'c'], stdout=subp.PIPE, stderr=subp.PIPE)
    @staticmethod
    # returns the ssid of the connected ssid on the given interface
    def connected_to(interface):
        # get the SSID connected on the interface
        connectedP = subp.Popen(['iwgetid', interface, '-r'], stdout=subp.PIPE, stderr=subp.PIPE)
        stdout, stderr = connectedP.communicate()
        # return stdout with trimmed whitespace = connected ssid
        return stdout.rstrip()
