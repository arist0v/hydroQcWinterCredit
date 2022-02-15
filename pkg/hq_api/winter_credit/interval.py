"""Class describing an interval of time."""


class Interval:
    """This class describe an interval of time."""

    def __init__(self, date, start, end, datetime_format="%Y-%m-%d %H:%M:%S"):
        """Period constructor."""
        self._datetime_format = datetime_format
        self.date_dt = date
        self.start_dt = start
        self.end_dt = end

    @property
    def date(self):
        """Give period date."""
        return self.date_dt.strftime("%Y-%m-%d")

    @property
    def start(self):
        """Give period start time as hour (without date)."""
        return self.start_dt.strftime(self._datetime_format)

    @property
    def end(self):
        """Give period end time as hour (without date)."""
        return self.end_dt.strftime(self._datetime_format)

    @property
    def start_ts(self):
        """Give period start time as timestamp."""
        return self.start_dt.timestamp()

    @property
    def end_ts(self):
        """Give period end time as timestamp."""
        return self.end_dt.timestamp()

    @property
    def start_iso(self):
        """Give period start time as isoformat."""
        return self.start_dt.isoformat()

    @property
    def end_iso(self):
        """Give period end time as isoformat."""
        return self.end_dt.isoformat()
