"""Hydro-Quebec adapter to get winter credit event as a thing for webthings gateway"""

from gateway_addon import Adapter, Database

_TIMEOUT = 3

class hqAdapter(Adapter):
    """Adapter for Hydro-Quebec winter credit"""

    def __init__(self):
        """initialize the object"""
        self.name = self.__class__.__name__
        Adapter.__init__(self)
        database = Database('hydroQcWinterCredit')
        print("poulet")

