from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN
from .helpers import fetch_json, get_base_url, get_conf_url, get_info_url

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
        self.device_name = f"HDFury {brdinfo['hostname']}"
        self.device_info = DeviceInfo(
            identifiers={(DOMAIN, brdinfo["serial"])},
            name=self.device_name,
            manufacturer="HDFury",
            model=brdinfo["hostname"].split("-")[0],
            serial_number=brdinfo["serial"],
            sw_version=brdinfo["version"].removeprefix("FW: "),
            hw_version=brdinfo.get("pcbv"),
            configuration_url=get_base_url(host),
            connections={(dr.CONNECTION_NETWORK_MAC, confinfo["macaddr"])},
        )

    async def _async_update_data(self):
        """Fetch the latest device data."""

        data = await fetch_json(self.hass, get_info_url(self.host))
        if not data:
            raise UpdateFailed("Failed to fetch infopage.ssi")

        conf_data = await fetch_json(self.hass, get_conf_url(self.host))
        if conf_data:
            self.confinfo = conf_data
        else:
            _LOGGER.warning("Failed to fetch confinfo.ssi; retaining previous confinfo")

        return data
