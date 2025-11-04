"""DataUpdateCoordinator for HDFury Integration."""

from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .helpers import fetch_json, get_conf_url, get_info_url

_LOGGER = logging.getLogger(__name__)

class HDFuryCoordinator(DataUpdateCoordinator):
    """HDFury Device Coordinator Class."""

    def __init__(self, hass: HomeAssistant, host: str, brdinfo: dict, confinfo: dict):
        """Initialize the coordinator."""

        super().__init__(
            hass,
            _LOGGER,
            name="HDFury",
            update_interval=timedelta(seconds=30),
        )
        self.host = host
        self.brdinfo = brdinfo
        self.confinfo = confinfo

    async def _async_update_data(self):
        """Fetch the latest device data."""

        data = await fetch_json(self.hass, get_info_url(self.host))
        if not data:
            raise UpdateFailed(f"Failed to fetch info page from {self.host}")

        conf_data = await fetch_json(self.hass, get_conf_url(self.host))
        if conf_data:
            self.confinfo = conf_data
        else:
            _LOGGER.warning("Failed to fetch config info; retaining previous data")

        return data
