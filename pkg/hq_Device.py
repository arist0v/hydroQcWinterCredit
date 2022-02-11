"""Device for hqWinterCreditAdapter"""

import datetime
from gateway_addon import Device

from pkg.hq_Property import hq_bool_ro_property, hq_datetime_ro_property, hq_minute_rw_property

from datetime import datetime

class hqDevice(Device):
    """HQ winter Credit Device"""

    def __init__(self, adapter, _id, config):
        """
        Initialize the object
        
        adapter -- Adapter managing this device
        _id -- ID of this device
        config -- config from database
        """

        Device.__init__(self, adapter, _id,)

        self._type.append('BinarySensor')
        #self.description = 'Hydro Quebec Winter Credit Event 1'#not sure where it'S used
        self.title = 'Hydro Quebec Winter Credit Event'#This appear in the text bar when adding the device and is the default name of the device
        self.name = 'Hydro Quebec Winter Credit Event 3'#not sure where it's used
        
        #SETTINGS PROPRETY FOR DEVICE

        #active event property
        activeEvent = hq_bool_ro_property(self, 'Active Event')
        self.properties['ActiveEvent'] = activeEvent
        activeEvent.set_RO_Value(self, 'ActiveEvent', False)

        #pre-heat property
        preHeatEvent = hq_bool_ro_property(self, 'Pre-Heat Event')
        self.properties['PreHeatEvent'] = preHeatEvent
        preHeatEvent.set_RO_Value(self, 'PreHeatEvent', False)

        #post-heat property
        postHeatEvent = hq_bool_ro_property(self, 'Post-Heat Event')
        self.properties['PostHeatEvent'] = postHeatEvent
        postHeatEvent.set_RO_Value(self, 'PostHeatEvent', False)

        #next event property
        nextEvent = hq_datetime_ro_property(self, 'Next Event')
        self.properties['NextEvent'] = nextEvent
        nextEvent.set_RO_Value(self, 'NextEvent', datetime.now())

        #last sync property
        lastSync = hq_datetime_ro_property(self, 'Last Sync')
        self.properties['LastSync'] = lastSync
        lastSync.set_RO_Value(self, 'LastSync', datetime.now())

        #pre-heat duration property
        preHeatDuration = hq_minute_rw_property(self, 'Pre-Heat Duration')
        self.properties['PreHeatDuration'] = preHeatDuration
        preHeatDuration.set_cached_value(config['preHeatDelay'])
        #value = config['preHeatDelay']
        #preHeatDuration.set_value(value)#.set_RO_Value(self, 'PreHeatDuration', config['preHeatDelay'])

        #TODO thing don'T keep value after changing in thing, 
    

        #post heat duration property
        postHeatDuration = hq_minute_rw_property(self, 'Post-Heat Duration')
        self.properties['PostHeatDuration'] = postHeatDuration
        postHeatDuration.set_RO_Value(self, 'PostHeatDuration', config['postHeatDelay'])
        