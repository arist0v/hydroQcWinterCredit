"""Device for hqWinterCreditAdapter"""

from wsgiref.simple_server import WSGIRequestHandler
from gateway_addon import Device

import threading
import time

class hqDevice(Device):
    """HQ winter Credit Device"""

    def __init__(self, adapter, _id):
        """
        Initialize the object
        
        adapter -- Adapter managing this device
        _id -- ID of this device
        """

        Device.__init__(self, adapter, _id)

        self._type.append('BinarySensor')
        self.description = 'Hydro Quebec Winter Credit Event 1'
        self.title = 'Hydro Quebec Winter Credit Event 2'
        self.name = 'Hydro Quebec Winter Credit Event 3'
        