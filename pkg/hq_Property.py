"""Property for device Hydro Quebec event for Webthings"""

from gateway_addon import Property, Device

class hqProperty(Property):
    """Property type for HQdata"""
    name = None
    description = None
    
    def __init__(self, device):
        """
        Initialize the object
        
        device -- the DEvice this property belongs to
        value -- current falue of this property
        """
        #Force to provide name in child class
        if self.name == None:
            raise NotImplementedError('Subclasses must define name')
        else:
            name = self.name
        
        #Force to provide description in child class
        if self.description == None:
            raise NotImplementedError('Sublcasses must define description')
        else:
            description = self.description

        Property.__init__(self, device, name, description)

    def set_RO_Value(self, device, value):
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

   def __init__(self, device, value):
       """
       Initialize the Property
       
       device -- device who own the property
       value -- starting value of the property
       """
       
       hqProperty.__init__(self, device)

       self.set_RO_Value(device, value)


