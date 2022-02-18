""" Data class for configuration data"""
from dataclasses import dataclass
from datetime import datetime

@dataclass
class hq_config_data:
    #preHeatDelay: int
    #postHeatDelay: int
    lastSync: datetime
    nextEvent: datetime
    #eventTable#TODO: create a table to store multiple next event and not just one