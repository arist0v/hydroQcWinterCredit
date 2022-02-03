"""Property for device Hydro Quebec event for Webthings"""

from os import name
from xml.dom.minidom import NamedNodeMap
from gateway_addon import Property
from datetime import datetime

class hqProperty(Property):
    """Property type for HQdata"""
    name = None
    description = None
    
    def __init__(self, device):
        """
        Initialize the object
        
        device -- the device this property belongs to
        name -- name of the property
        """

        #Force to provide description in child class
        if self.name is None:
            raise NotImplementedError('Sublcasses must define description')
        
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
   """Active Event Property"""

   def __init__(self, device, title):
       
       self.description={'@type': 'BooleanProperty', 'title': title, 'type': 'boolean', 'readOnly' : True,}#description of the property
       super().__init__(device)

class hq_datetime_ro_property(hqProperty):
    """Active Event Property"""

    description={'title': title, 'type': 'string', 'readOnly' : True,}#description of the propertybon la reponse semble etre non
    
    def set_RO_Value(self, device, propName, value: datetime):
        """
        modifying the set_RO_Value for datetime object
        """

        value = value.strftime("%Y/%m/%d\n %H:%M:%S")#TODO:Verify if isoformat could replace strftime
        super().set_RO_Value(device, propName, value)

