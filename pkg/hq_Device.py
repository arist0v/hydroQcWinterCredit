"""Device for hqWinterCreditAdapter"""

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
        
        


