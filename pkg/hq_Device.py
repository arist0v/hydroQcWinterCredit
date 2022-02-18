"""Device for hqWinterCreditAdapter"""

from gateway_addon import Device

from pkg.hq_Property import hq_bool_ro_property, hq_datetime_ro_property
from pkg.hq_DataClass import hq_config_data
from pkg.hq_webuser import hq_webuser

from datetime import datetime, time

_POLL_INTERVAL = 5 #interval to check if data changed

class hqDevice(Device):
    """HQ winter Credit Device"""

    def __init__(self, adapter, _id):
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

        datas = hq_config_data(adapter.config['preHeatDelay'], adapter.config['postHeatDelay'], datetime.now(), datetime.now)#for developement purpose, data will be change later
        
        #SETTINGS PROPRETY FOR DEVICE

        #active event property
        activeEvent = hq_bool_ro_property(self, 'Active Event')
        self.properties['ActiveEvent'] = activeEvent
        #activeEvent.set_RO_Value(self, 'ActiveEvent', False)

        #pre-heat property
        preHeatEvent = hq_bool_ro_property(self, 'Pre-Heat Event')
        self.properties['PreHeatEvent'] = preHeatEvent
        #preHeatEvent.set_RO_Value(self, 'PreHeatEvent', False)

        #post-heat property
        postHeatEvent = hq_bool_ro_property(self, 'Post-Heat Event')
        self.properties['PostHeatEvent'] = postHeatEvent
        #postHeatEvent.set_RO_Value(self, 'PostHeatEvent', False)

        #next event property
        nextEvent = hq_datetime_ro_property(self, 'Next Event')
        self.properties['NextEvent'] = nextEvent
       #nextEvent.set_RO_Value(self, 'NextEvent', datetime.now())

        #last sync property
        lastSync = hq_datetime_ro_property(self, 'Last Sync')
        self.properties['LastSync'] = lastSync
        #lastSync.set_RO_Value(self, 'LastSync', datetime.now())
        """
        #Those property will be disabled and only keep in add-on settings page for now

        #pre-heat duration property
        preHeatDuration = hq_minute_rw_property(self, 'Pre-Heat Duration')
        self.properties['PreHeatDuration'] = preHeatDuration
        #preHeatDuration.set_cached_value(config['preHeatDelay'])
        #value = config['preHeatDelay']
        #preHeatDuration.set_value(value)#.set_RO_Value(self, 'PreHeatDuration', config['preHeatDelay'])    

        #post heat duration property
        postHeatDuration = hq_minute_rw_property(self, 'Post-Heat Duration')
        self.properties['PostHeatDuration'] = postHeatDuration
        #postHeatDuration.set_RO_Value(self, 'PostHeatDuration', config['postHeatDelay'])
        """
    def poll(self):
        """
        poll for changes
        must be called in a thread
        """
        #TODO: fetch data
        #compare data
        ##if fetched data is different,  update it with prop.set_RO_Value()
        username = self.adapter.config['hydroQcUsername']
        password = self.adapter.config['hydroQcPassword']
        webUser = hq_webuser(username, password)
        
        while True:
            nextEvent = None
            time.sleep(_POLL_INTERVAL)
            now = datetime.now()
            
            events = webUser.get_events()
            for event in events:
                startEvent= datetime.strptime(event['start'])
                if startEvent > now:
                    if not nextEvent == None:
                        if startEvent < nextEvent['start']:
                            nextEvent = event
            
            #nextEvent is now the closest event
                            
            #NOTE: preHeat event = nextEvent - dateime.timedelta(preHeatDelay)
            #do check and update for every property
            """
            for prop in self.properties:

                if prop.name == 'NextEvent':
                    #do every update for next event
                    if prop.value == datas.nextEvent:
                        continue
                    else:
                        prop.set_RO_Value(self, prop.name, datas.nextEvent)
                
                if prop.name == 'LastSync':
                    if prop.value == datas.lastSync:
                        continue
                    else:
                        prop.set_RO_Value(self, prop.name, datas.lastSync)

                if prop.name == 'ActiveEvent':
                    #do every check and update for active event
                    print("must do something here")

                if prop.name == 'PreHeatEvent':
                    #do pre heat event check and update
                    print("must do something here")

                if prop.name == 'PostHeatEvent':
                    #do post heat event check and update
                    print("must do something here")
            """