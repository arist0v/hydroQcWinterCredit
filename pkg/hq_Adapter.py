"""Hydro-Quebec adapter to get winter credit event as a thing for webthings gateway"""

from socket import timeout
import time
from gateway_addon import Adapter, Database

_TIMEOUT = 3

class hqAdapter(Adapter):
    """Adapter for Hydro-Quebec winter credit"""

    def __init__(self):
        """initialize the object"""
        self.name = self.__class__.__name__
        Adapter.__init__(self,'hydroQcWinterCredit','hydroQcWinterCredit')#argument: self, id for the package, name of the package
        database = Database('hydroQcWinterCredit')
        print("poulet")#use print to print info in log #DEBUG

        self.pairing=False
        self.start_pairing(_TIMEOUT)

        
    def start_pairing(self, timeout):
        """Start pairing process"""
        if self.pairing:
            return

        self.pairing = True
        print("Pairing")#DEBUG

        time.sleep(timeout)

        self.pairing = False

