"""Property for device Hydro Quebec event for Webthings"""

from os import name
from xml.dom.minidom import NamedNodeMap
from gateway_addon import Property
from datetime import datetime

class hqProperty(Property):
    """Property type for HQdata"""
    description = None
    
    def __init__(self, device):
        """
        Initialize the object
        
        device -- the device this property belongs to
        """
        
        #Force to provide description in child class
        if self.description is None:
            raise NotImplementedError('Sublcasses must define description')

        super().__init__(device, name, self.description)
        

    def set_RO_Value(self, device, propName, value):
        """
        Set a read-only value
        
        device -- device who own the property
        propName -- property to update
        value -- value of the property
        """

        prop = device.find_property(propName)
        prop.set_cached_value_and_notify(value)

class hq_bool_ro_property(hqProperty):
   """Boolean Property Read Only"""

   def __init__(self, device, name):
       """
       Initialize the objects

       name -- name of the property
       """
       self.description={'@type': 'BooleanProperty', 'title': name, 'type': 'boolean', 'readOnly' : True,}#description of the property
       super().__init__(device)

   def set_RO_Value(self, device, propName, value: bool):
        super().set_RO_Value(device, propName, value)

class hq_datetime_ro_property(hqProperty):
    """datetime Property Read Only"""

    def __init__(self, device, name):
        """
        Initialize the object

        name -- name of the property
        """
        self.description={'title': name, 'type': 'string', 'readOnly' : True,}#description of the property
        super().__init__(device)    
    
    def set_RO_Value(self, device, propName, value: datetime):
        """
        modifying the set_RO_Value for datetime object

        value -- value of the property, must be datetime
        """

        value = value.strftime("%Y/%m/%d\n %H:%M:%S")#TODO:Verify if isoformat could replace strftime
        super().set_RO_Value(device, propName, value)
"""
#Those class will be disabled since property will only be keep in add-on settings page for now
class hq_minute_rw_property(hqProperty):
    """"""Number property, read and write""""""

    def __init__(self, device, name):
        """"""
        Initialize the object
        
        name -- name of the property
        """"""

        self.description={'@type':'LevelProperty' ,'title': name, 'type': 'number','minimum': 0,}#description of the property
        super().__init__(device)

    def set_RO_Value(self, device, propName, value: int):
        super().set_RO_Value(device, propName, value)
    
"""