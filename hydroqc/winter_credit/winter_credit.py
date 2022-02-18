"""Winter credit processing."""
import datetime
import logging
import time

from dateutil import parser
import pytz

from hydroqc.winter_credit.event import Event
from hydroqc.winter_credit.period import Period

log = logging.getLogger(__name__)

DEFAULT_MORNING_PEAK_START = "06:00:00"
DEFAULT_MORNING_PEAK_END = "09:00:00"
DEFAULT_EVENING_PEAK_START = "16:00:00"
DEFAULT_EVENING_PEAK_END = "20:00:00"
DEFAULT_ANCHOR_START_OFFSET = 5
DEFAULT_ANCHOR_DURATION = 3
DEFAULT_EVENT_REFRESH_SECONDS = 300
DEFAULT_PRE_HEAT_START_OFFSET = 3
DEFAULT_PRE_HEAT_END_OFFSET = 0
EST_TIMEZONE = "Canada/Eastern"


def _date_time_from_string(date_string):
    """Convert string in the YYYY-MM-DD HH:MM:SS to a datetime object.

    :param: date_string: date in YYYY-MM-DD HH:MM:SS format

    :return: datetime object

    :rtype: datetime
    """
    return pytz.timezone(EST_TIMEZONE).localize(
            datetime.datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S"))


def _timestamp_from_string(date_string):
    """Convert a date string in format YYYY-MM-DD HH:MM:SS to a timestamp.

    :param: date_string in YYYY-MM-DD HH:MM:SS format

    :return: timestamp

    :rtype: float
    """
    return _date_time_from_string(date_string).timestamp()


def _get_today_anchor_periods(peak_periods, start_offset, duration):
    """Calculate anchor periods from the specified offset.

    :params: peak_periods: list of Period objects representing the peak periods
             start_offset: datetime.timedelta configured with the defined offset
             duration: datetime.timedelta configured with duration of anchor periods

    :return:  dict having morning and evening Period objects reprensenting anchor periods.
    """
    peak_periods["morning"] = peak_periods["morning"]
    peak_periods["evening"] = peak_periods["evening"]

    today_anchor_morning_start = peak_periods["morning"].start_dt - start_offset
    today_anchor_morning_end = today_anchor_morning_start + duration
    today_anchor_evening_start = peak_periods["evening"].start_dt - start_offset
    today_anchor_evening_end = today_anchor_evening_start + duration

    morning = Period(
        date=today_anchor_morning_start,
        start=today_anchor_morning_start,
        end=today_anchor_morning_end,
    )
    evening = Period(
        date=today_anchor_evening_start,
        start=today_anchor_evening_start,
        end=today_anchor_evening_end,
    )

    return {"morning": morning, "evening": evening}


def _winter_credit_enabled(func):
    """Decorate any methods that use self.data to avoid useless calls."""

    async def myfunction(self):
        if self.is_enabled:
            return await func(self)
        log.info("Winter credit not enabled.")
        return None

    return myfunction


class WinterCreditHandler:
    """Winter Credit extra logic.

    This class supplements Hydro API data by providing calculated values for pre_heat period,
    anchor period detection as well as next event information.
    """

    def __init__(
        self,
        webuser_id,
        customer_id,
        contract_id,
        hydro_client,
        datetime_format="%Y-%m-%d %H:%M:%S",
    ):
        """Winter Credit constructor."""
        self._no_partenaire_demandeur = webuser_id
        self._no_partenaire_titulaire = customer_id
        self._no_contrat = contract_id
        self._hydro_client = hydro_client
        self._datetime_format = datetime_format

        self.events = {}
        self.event_in_progress = False
        self._last_update = 0
        self.data = {}
        self.state_data = {}
        self.dates = {}

    @property
    def webuser_id(self):
        """Get webuser id."""
        return self._no_partenaire_demandeur

    @property
    def customer_id(self):
        """Get customer id."""
        return self._no_partenaire_titulaire

    @property
    def contract_id(self):
        """Get contract id."""
        return self._no_contrat

    @property
    def is_enabled(self):
        """Is winter credit mode actived."""
        if "optionTarifActuel" not in self.data:
            # If we don't know, let's try to get the information
            return True
        return self.data["optionTarifActuel"] == "CPC"

    def _set_attributes(self):
        """Populate attributes calculated by _get_current_state."""
        for key in self.state_data.keys():
            if not isinstance(self.state_data[key], dict):
                setattr(self, "value_" + key, self.state_data[key])
            else:
                for subkey in self.state_data[key].keys():
                    if not isinstance(self.state_data[key][subkey], dict):
                        name = "value_" + key + "_" + subkey
                        setattr(self, name, self.state_data[key][subkey])
                    else:
                        for lastkey in self.state_data[key][subkey].keys():
                            name = "value_" + key + "_" + subkey + "_" + lastkey
                            setattr(self, name, self.state_data[key][subkey][lastkey])

    async def refresh_data(self, full_refresh=True):
        """Refresh data if data is older than the config event_refresh_seconds parameter."""
        # DATES
        self.dates["ref_date"] = pytz.timezone(EST_TIMEZONE).localize(datetime.datetime.now())
        # To test the date can be modified artificially here.
        # self.dates['ref_date'] = _date_time_from_string("2022-01-18 00:00:00")
        self.dates["today"] = pytz.timezone(EST_TIMEZONE).localize(datetime.datetime.now())
        self.dates["today_date"] = self.dates["today"].strftime("%Y-%m-%d")
        self.dates["today_noon_ts"] = _timestamp_from_string(
            self.dates["today_date"] + " 12:00:00"
        )

        self.dates["tomorrow"] = self.dates["today"] + datetime.timedelta(days=1)
        self.dates["tomorrow_date"] = self.dates["tomorrow"].strftime("%Y-%m-%d")
        self.dates["tomorrow_noon_ts"] = _timestamp_from_string(
            self.dates["tomorrow_date"] + " 12:00:00"
        )

        log.debug("Checking if we need to update the Data")
        if time.time() > (self._last_update + DEFAULT_EVENT_REFRESH_SECONDS):
            log.debug("Refreshing data")
            self.data = await self._hydro_client.get_winter_credit(
                self.webuser_id, self.customer_id, self.contract_id
            )
            if not self.is_enabled:
                log.info("Winter credit not actived on the account.")
                return
            events_data = self._get_winter_credit_events()
            self.events = events_data["events"]
            self.event_in_progress = events_data["event_in_progress"]
            self._last_update = time.time()
        else:
            log.debug("Data is up to date")
        log.debug("Refreshing current state")
        if full_refresh:
            self.state_data = await self._get_current_state()
            self._set_attributes()

    def _get_winter_credit_events(self):
        """Return winter peak events in a more structured way.

        :return:

        JSON Object with current_winter, past_winters and next event.
        Current winter have past and future events
        Events have timestamp as key (easier to sort). See Event class for more info

        :example:

            ::

                events = {
                            'current_winter': {
                                'past': { [Event, ...] },
                                'future': { [Event, ...] }
                            },
                            'past_winters': { [Event, ...] },
                            'next': { [Event, ...] }
                        }

        :rtype: dict

        :notes:

        - The next event will be returned only when the current event is completed to avoid
          interfering with automations
        - The timestamp is the timestamp of the end of the event
        - Future events have a 'pre_heat' datetime as a helper for homeassistant
          pre-event automations (offset -3h)
        """
        events = {
            "current_winter": {"past": {}, "future": {}},
            "past_winters": {},
            "next": {},
        }
        if "periodesEffacementsHivers" in self.data:
            for season in self.data["periodesEffacementsHivers"]:
                winter_start = parser.isoparse(season["dateDebutPeriodeHiver"]).date()
                winter_end = parser.isoparse(season["dateFinPeriodeHiver"]).date()
                current = bool(winter_start <= datetime.date.today() <= winter_end)

                if "periodesEffacementHiver" in season:
                    for hydro_event in season["periodesEffacementHiver"]:
                        date = parser.isoparse(hydro_event["dateEffacement"])
                        event = Event(
                            date=date,
                            start=_date_time_from_string(
                                date.strftime("%Y-%m-%d")
                                + " "
                                + hydro_event["heureDebut"]
                            ),
                            end=_date_time_from_string(
                                date.strftime("%Y-%m-%d")
                                + " "
                                + hydro_event["heureFin"]
                            ),
                        )

                        future = False
                        if event.end_ts >= self.dates["ref_date"].timestamp():
                            future = True
                        if current:
                            if future:
                                events["current_winter"]["future"][event.end_ts] = event
                            else:
                                events["current_winter"]["past"][event.end_ts] = event
                        else:
                            events["past_winter"][event.end_ts] = event

        next_event = self._get_next_event(events)
        events["next"] = next_event["next"]

        return {"events": events, "event_in_progress": next_event["event_in_progress"]}

    @_winter_credit_enabled
    async def get_future_events(self):
        """Return future events object.

        :return: future events list

        :rtype: list
        """
        await self.refresh_data(False)
        future_events = []
        for future_ts in self.events["current_winter"]["future"]:
            future_events.append(
                self.events["current_winter"]["future"][future_ts].to_dict()
            )

        return future_events

    async def get_all_events(self):
        """Return future and past events (Current winter only) object.

        :return: events list

        :rtype: list
        """
        await self.refresh_data(False)
        events = []
        for future_ts in self.events["current_winter"]["future"]:
            events.append(self.events["current_winter"]["future"][future_ts])
        for past_ts in self.events["current_winter"]["past"]:
            events.append(self.events["current_winter"]["past"][past_ts])
        return events

    async def get_next_event(self):
        """Return next event object.

        :return: next event object

        :rtype: dict
        """
        await self.refresh_data(False)
        return self.events["next"]

    def _get_today_peak_periods(self):
        """Calculate today's peak periods.

        :return: dict having morning and evening Period objects reprensenting peak periods.
        """
        # PEAK PERIODS
        today_peak_morning_start = _date_time_from_string(
            self.dates["today_date"] + " " + DEFAULT_MORNING_PEAK_START
        )
        today_peak_morning_end = _date_time_from_string(
            self.dates["today_date"] + " " + DEFAULT_MORNING_PEAK_END
        )
        today_peak_evening_start = _date_time_from_string(
            self.dates["today_date"] + " " + DEFAULT_EVENING_PEAK_START
        )
        today_peak_evening_end = _date_time_from_string(
            self.dates["today_date"] + " " + DEFAULT_EVENING_PEAK_END
        )

        morning = Period(
            date=today_peak_morning_start,
            start=today_peak_morning_start,
            end=today_peak_morning_end,
        )
        evening = Period(
            date=today_peak_evening_start,
            start=today_peak_evening_start,
            end=today_peak_evening_end,
        )

        return {"morning": morning, "evening": evening}

    @_winter_credit_enabled
    async def _get_current_state(self):
        """Calculate current periods and state.

        This method compile the data from hydro API and compute periods accordingly
        It will also give a number of states to help with automation

        :return: dict

        :schema:
        '''
        {
            "state": {
                "current_period": string (see lexicon),
                "current_period_time_of_day": string (see lexicon),
                "current_composite_state" : string (see lexicon),
                "critical": true / false,
                "event_in_progress": true / false,
                "pre_heat": true / false,
                "upcoming_event":  true / false,
                "morning_event_today": true / false,
                "evening_event_today": true / false,
                "morning_event_tomorrow": true / false,
                "evening_event_tomorrow": true / false,
            },
            "next_periods": {
                "peak": Period
                "anchor": Period
            },
            "anchor_periods": {
                "morning": Period
                "evening": Period
            },
            "peak_periods": {
                "morning": Period
                "evening": Period
            },
            "next": Event,
            "cumulated_credit": float
            "last_update": datetime string
        }
        '''
        """
        # await self.refresh_data()

        peak_periods = self._get_today_peak_periods()
        next_event = await self.get_next_event()

        anchor_start_offset = datetime.timedelta(hours=DEFAULT_ANCHOR_START_OFFSET)
        anchor_duration = datetime.timedelta(hours=DEFAULT_ANCHOR_DURATION)
        anchor_periods = _get_today_anchor_periods(
            peak_periods, anchor_start_offset, anchor_duration
        )

        # Calculation for the next periods.
        if self.dates["today"].timestamp() <= peak_periods["morning"].end_ts:
            next_peak_period_start = peak_periods["morning"].start_dt
            next_peak_period_end = peak_periods["morning"].end_dt
        elif (
            peak_periods["morning"].end_ts
            <= self.dates["today"].timestamp()
            <= peak_periods["evening"].end_ts
        ):
            next_peak_period_start = peak_periods["evening"].start_dt
            next_peak_period_end = peak_periods["evening"].end_dt
        else:
            next_peak_period_start = peak_periods[
                "morning"
            ].start_dt + datetime.timedelta(days=1)
            next_peak_period_end = peak_periods["morning"].end_dt + datetime.timedelta(
                days=1
            )

        if (
            peak_periods["morning"].start_ts
            <= self.dates["today"].timestamp()
            <= peak_periods["morning"].end_ts
        ):
            current_period = "peak"
            current_period_time_of_day = "peak_morning"
        elif (
            peak_periods["evening"].start_ts
            <= self.dates["today"].timestamp()
            <= peak_periods["evening"].end_ts
        ):
            current_period = "peak"
            current_period_time_of_day = "peak_evening"
        elif (
            anchor_periods["morning"].start_ts
            <= self.dates["today"].timestamp()
            <= anchor_periods["morning"].end_ts
        ):
            current_period = "anchor"
            current_period_time_of_day = "anchor_morning"
        elif (
            anchor_periods["evening"].start_ts
            <= self.dates["today"].timestamp()
            <= anchor_periods["evening"].end_ts
        ):
            current_period = "anchor"
            current_period_time_of_day = "anchor_evening"
        else:
            current_period = "normal"
            current_period_time_of_day = "normal"

        pre_heat = False
        morning_event_today = False
        evening_event_today = False
        morning_event_tomorrow = False
        evening_event_tomorrow = False
        upcoming_event = False
        next_peak_critical = False
        next_event_dict = {
            "start_iso": "",
            "end_iso": "",
        }
        if isinstance(next_event, Event) and next_event.pre_heat_start_ts:
            if (
                next_event.pre_heat_start_ts
                <= self.dates["today"].timestamp()
                <= next_event.pre_heat_end_ts
            ):
                pre_heat = True
            next_event_dict = next_event.to_dict()
        for event in await self.get_all_events():
            if event.date:
                if event.date == self.dates["today_date"]:
                    if event.start_ts < self.dates["today_noon_ts"]:
                        morning_event_today = True
                    else:
                        evening_event_today = True
                    if event.end_ts == next_peak_period_end.timestamp():
                        next_peak_critical = True
                elif event.date == self.dates["tomorrow_date"]:
                    if event.start_ts < self.dates["tomorrow_noon_ts"]:
                        morning_event_tomorrow = True
                    else:
                        evening_event_tomorrow = True
                if event.start_ts > self.dates["today"].timestamp():
                    upcoming_event = True

        if next_peak_critical:
            current_composite_state = current_period_time_of_day + "_critical"
        else:
            current_composite_state = current_period_time_of_day + "_normal"

        next_peak_period = Period(
            date=next_peak_period_start,
            start=next_peak_period_start,
            end=next_peak_period_end,
            critical=next_peak_critical,
        )

        next_anchor_period = Period(
            date=next_peak_period_start - anchor_start_offset,
            start=next_peak_period_start - anchor_start_offset,
            end=next_peak_period_start - anchor_start_offset + anchor_duration,
            critical=next_peak_critical,
        )

        peak_periods["morning"].critical = morning_event_today
        peak_periods["evening"].critical = evening_event_today

        response = {
            "state": {
                "current_period": current_period,
                "current_period_time_of_day": current_period_time_of_day,
                "current_composite_state": current_composite_state,
                "critical": next_peak_critical,
                "event_in_progress": self.event_in_progress,
                "pre_heat": pre_heat,
                "upcoming_event": upcoming_event,
                "morning_event_today": morning_event_today,
                "evening_event_today": evening_event_today,
                "morning_event_tomorrow": morning_event_tomorrow,
                "evening_event_tomorrow": evening_event_tomorrow,
            },
            "next_periods": {
                "peak": next_peak_period.to_dict(),
                "anchor": next_anchor_period.to_dict(),
            },
            "anchor_periods": {
                "morning": anchor_periods["morning"].to_dict(),
                "evening": anchor_periods["evening"].to_dict(),
            },
            "peak_periods": {
                "morning": peak_periods["morning"].to_dict(),
                "evening": peak_periods["evening"].to_dict(),
            },
            "next": next_event_dict,
            "cumulated_credit": float(self.data["montantEffaceProjete"]),
            "last_update": self.dates["today"].strftime(self._datetime_format),
        }
        return response

    def _get_pre_heat(self, start):
        """Calculate pre_heat period according to event start date.

        :param: start: datetime object representing the start of the next event

        :return: pre_heat period

        :rtype: dict
        """
        pre_heat_start_offset = datetime.timedelta(hours=DEFAULT_PRE_HEAT_START_OFFSET)
        pre_heat_start = start - pre_heat_start_offset
        pre_heat_end_offset = datetime.timedelta(hours=DEFAULT_PRE_HEAT_END_OFFSET)
        pre_heat_end = start - pre_heat_end_offset
        pre_heat = {
            "pre_heat_start": pre_heat_start.strftime(self._datetime_format),
            "pre_heat_end": pre_heat_end.strftime(self._datetime_format),
            "pre_heat_start_ts": pre_heat_start.timestamp(),
            "pre_heat_end_ts": pre_heat_end.timestamp(),
        }
        return pre_heat

    def _get_next_event(self, events):
        """Calculate the next events.

        :param: events: the events object we have built from hydro API self.data

        :return: event object

        :rtype: dict
        """
        event_in_progress = False
        next_event_timestamp = None
        next_event = {}
        if events["current_winter"]["future"]:
            for timestamp in events["current_winter"]["future"]:
                event = events["current_winter"]["future"][timestamp]
                pre_heat = self._get_pre_heat(event.start_dt)
                event.add_preheat(
                    pre_heat["pre_heat_start"],
                    pre_heat["pre_heat_end"],
                    pre_heat["pre_heat_start_ts"],
                    pre_heat["pre_heat_end_ts"],
                )

                if event.start_ts <= self.dates["ref_date"].timestamp() <= event.end_ts:
                    event_in_progress = True
                    next_event_timestamp = timestamp
                    break

            if not event_in_progress:
                next_event_timestamp = min(
                    events["current_winter"]["future"], key=float
                )
        if next_event_timestamp:
            next_event = events["current_winter"]["future"][next_event_timestamp]

        return {"next": next_event, "event_in_progress": event_in_progress}
