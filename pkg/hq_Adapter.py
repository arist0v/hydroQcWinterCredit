"""Hydro-Quebec adapter to get winter credit event as a thing for webthings gateway"""

from socket import timeout
import time
from gateway_addon import Adapter, Database
from pkg import hq_Device

_TIMEOUT = 3

class hqAdapter(Adapter):
    """Adapter for Hydro-Quebec winter credit"""

    def __init__(self):
        """initialize the object"""
        self.name = self.__class__.__name__
        Adapter.__init__(self,'hydroQcWinterCredit','hydroQcWinterCredit')#argument: self, id for the package, name of the package
        self.config = self.load_db_config(self.get_id())

        if not config:
            print("Can't load config from Database")
            return

        self.pairing=False
        self.start_pairing(_TIMEOUT)

        
    def start_pairing(self, timeout):
        """Start pairing process"""
        if self.pairing:
            return

        self.pairing = True
        device = hq_Device.hqDevice(self, "hqDevice", self.config)
        self.handle_device_added(device)
        print("Start Pairing")#DEBUG

        time.sleep(timeout)

        self.pairing = False

        self.device = device
    """
    def remove_device(self, device):
        Removing the device from webthings

        #self.handle_device_removed(device)
        #TODO: Error in log: ERROR  : Error getting thing description for thing with id hqDevice12345: Error: Unable to find thing with id: hqDevice12345
        #  at /home/node/webthings/gateway/build/webpack:/src/models/things.js:268:1 TO BE FIXED LATER
    """
    def cancel_pairing(self):
        """Cancel the pairing process"""
        self.pairing = False

    def load_db_config(self, package_name):
        """
        Load configuration from DB

        package_name -- name of the package as shown in the manifest.json

        Return the config object as dict
        """
        database = Database[package_name]
        if not database.open():
            return
        config = database.load_config()
        database.close()

        if not config:
            return

        return config

    def save_config_to_db(self, package_name, config):
        """
        save configuration to DB

        package_name -- name of the package as shown in manifest.json
        config -- config dict to save in DB
        """
        database = Database[package_name]
        database.open()
        database.save_config(config)
        database.close()