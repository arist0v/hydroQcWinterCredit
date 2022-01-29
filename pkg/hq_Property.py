"""Property for device Hydro Quebec event for Webthings"""

from gateway_addon import Property

class hqProperty(Property):
    """Property type for HQdata"""
    
    def __init__(self, device, name, description, value):
        """
        Initialize the object
        
        device -- the DEvice this property belongs to
        name -- name of the property
        description -- description of the property
        value -- current falue of this property
        """
        Property.__init__(device, name, description)
        self.set_cached_value(value)

