"""Class describing an event."""
from .interval import Interval


class Event(Interval):
    """This class describe an event object."""

    def __init__(self, date, start, end, datetime_format="%Y-%m-%d %H:%M:%S"):
        """Event constructor."""
        super().__init__(date, start, end, datetime_format)
        self.pre_heat_start = None
        self.pre_heat_end = None
        self.pre_heat_start_ts = None
        self.pre_heat_end_ts = None

    def to_dict(self):
        """Return the current object attributes as a dict."""
        if self.pre_heat_start:
            return {
                "date": self.date,
                "start": self.start,
                "end": self.end,
                "start_ts": self.start_ts,
                "end_ts": self.end_ts,
                "start_iso": self.start_iso,
                "end_iso": self.end_iso,
                "pre_heat_start": self.pre_heat_start,
                "pre_heat_end": self.pre_heat_end,
                "pre_heat_start_ts": self.pre_heat_start_ts,
                "pre_heat_end_ts": self.pre_heat_end_ts,
            }
        return {
            "date": self.date,
            "start": self.start,
            "end": self.end,
            "start_ts": self.start_ts,
            "end_ts": self.end_ts,
            "start_iso": self.start_iso,
            "end_iso": self.end_iso,
        }

    def add_preheat(self, start, end, start_ts, end_ts):
        """Add a pre-heat period in the event."""
        # TODO: Make it an interval ??
        self.pre_heat_start = start
        self.pre_heat_end = end
        self.pre_heat_start_ts = start_ts
        self.pre_heat_end_ts = end_ts
