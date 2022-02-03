"""Device for hqWinterCreditAdapter"""

import datetime
from gateway_addon import Device

from pkg.hq_Property import hq_bool_ro_property, hq_datetime_ro_property, hqActiveEventProperty, hqNextEventProperty

from datetime import datetime

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

        #active event property
        activeEvent = hq_bool_ro_property(self, 'Active Event')
        self.properties['ActiveEvent'] = activeEvent
        activeEvent.set_RO_Value(self, 'ActiveEvent', False)

        #next event property
        nextEvent = hq_datetime_ro_property(self, 'Next Event')
        self.properties['NextEvent'] = nextEvent
        nextEvent.set_RO_Value(self, 'NextEvent', datetime.now())