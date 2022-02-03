"""Property for device Hydro Quebec event for Webthings"""

from gateway_addon import Property
from datetime import datetime

class hqProperty(Property):
    """Property type for HQdata"""
    name = None
    description = None
    
    def __init__(self, device):
        """
        Initialize the object
        
        device -- the DEvice this property belongs to
        """
        #Force to provide name in child class
        if self.name is None:
            raise NotImplementedError('Subclasses must define name')
        
        #Force to provide description in child class
        if self.description is None:
            raise NotImplementedError('Sublcasses must define description')


        super().__init__(device, self.name, self.description)

    def set_RO_Value(self, device, propName, value):
        """
        Set a read-only value
        
        device -- device who own the property
        propName -- property to update
        value -- value of the property
        """

        prop = device.find_property(propName)
        prop.set_cached_value_and_notify(value)

class hqActiveEventProperty(hqProperty):
   """Active Event Property"""
   name = 'Active Event'#name of the property
   description={'@type': 'BooleanProperty', 'title': 'Active Event', 'type': 'boolean', 'readOnly' : True,}#description of the property

class hqNextEventProperty(hqProperty):
    """Active Event Property"""
    name = 'Next Event'#name of the property
    description={'title': 'Next Event', 'type': 'string', 'readOnly' : True,}#description of the propertybon la reponse semble etre non
    
    def set_RO_Value(self, device, propName, value: datetime):
        """
        modifying the set_RO_Value for datetime object
        """

        value = value.strftime("%Y/%m/%d\n %H:%M:%S")#TODO:Verify if isoformat could replace strftime
        super().set_RO_Value(device, propName, value)

