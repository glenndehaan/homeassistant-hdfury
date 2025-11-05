"""DataUpdateCoordinator for HDFury Integration."""

from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN
from .helpers import fetch_json, get_brd_url, get_conf_url, get_info_url

_LOGGER = logging.getLogger(__name__)

class HDFuryCoordinator(DataUpdateCoordinator):
    """HDFury Device Coordinator Class."""

    def __init__(self, hass: HomeAssistant, host: str):
        """Initialize the coordinator."""

        super().__init__(
            hass,
            _LOGGER,
            name="HDFury",
            update_interval=timedelta(seconds=30),
        )
        self.host = host
        self.data = {
            "board": {},
            "info": {},
            "config": {},
        }

    async def _async_update_data(self):
        """Fetch the latest device data."""

        board = await fetch_json(self.hass, get_brd_url(self.host))
        if not board:
            _LOGGER.error("Failed to fetch board info from %s", get_brd_url(self.host))
            raise UpdateFailed(
                translation_domain=DOMAIN,
                translation_key="connection_error",
                translation_placeholders={"endpoint": str(get_brd_url(self.host))},
            )

        info = await fetch_json(self.hass, get_info_url(self.host))
        if not info:
            _LOGGER.error("Failed to fetch info page from %s", get_info_url(self.host))
            raise UpdateFailed(
                translation_domain=DOMAIN,
                translation_key="connection_error",
                translation_placeholders={"endpoint": str(get_info_url(self.host))},
            )

        config = await fetch_json(self.hass, get_conf_url(self.host))
        if not config:
            _LOGGER.error("Failed to fetch config info from %s", get_conf_url(self.host))
            raise UpdateFailed(
                translation_domain=DOMAIN,
                translation_key="connection_error",
                translation_placeholders={"endpoint": str(get_conf_url(self.host))},
            )

        return {
            "board": board,
            "info": info,
            "config": config,
        }
