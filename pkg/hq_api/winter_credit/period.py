"""Class describing a period."""
from .interval import Interval


class Period(Interval):
    """This class describe a period object."""

    def __init__(
        self, date, start, end, datetime_format="%Y-%m-%d %H:%M:%S", critical=False
    ):
        """Period constructor."""
        super().__init__(date, start, end, datetime_format)
        self.critical = critical

    def to_dict(self):
        """Return the current object attributes as a dict."""
        return {
            "date": self.date,
            "start": self.start,
            "end": self.end,
            "start_ts": self.start_ts,
            "end_ts": self.end_ts,
            "start_iso": self.start_iso,
            "end_iso": self.end_iso,
            "critical": self.critical,
        }
