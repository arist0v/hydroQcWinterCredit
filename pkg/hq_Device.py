"""Device for hqWinterCreditAdapter"""

from wsgiref.simple_server import WSGIRequestHandler
from gateway_addon import Device, Property

from pkg.hq_Property import hqActiveEventProperty

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
        #self.description = 'Hydro Quebec Winter Credit Event 1'#not sure where it'S used
        self.title = 'Hydro Quebec Winter Credit Event'#This appear in the text bar when adding the device and is the default name of the device
        self.name = 'Hydro Quebec Winter Credit Event 3'#not sure where it's used
        
        #SETTINGS PROPRETY FOR DEVICE

        activeEvent = hqActiveEventProperty(self, False)
        self.properties['ActiveEvent'] = activeEvent

        activeEvent.set_RO_Value(self, False)

        """
        self.properties['ActiveEvent'] = Property(self, 'Active Event', 
        {
            '@type': 'BooleanProperty',
            'title': 'Active Event',
            'type': 'boolean',
            'readOnly' : True,
        })
        prop = self.find_property('ActiveEvent')
        prop.set_cached_value_and_notify(False)
        """
        #print(prop)
        #prop.update(False)
        #self.notify_property_changed(prop)
        #self.notify_property_changed(self.find_property('ActiveEvent'))