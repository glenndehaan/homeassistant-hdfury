from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers import device_registry as dr

from .const import DOMAIN, PLATFORMS
from .helpers import fetch_json, get_base_url, get_brd_url, get_conf_url, get_info_url

_LOGGER = logging.getLogger(__name__)

class HDFuryCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, host: str, brdinfo: dict, confinfo: dict):
        super().__init__(
            hass,
            _LOGGER,
            name="HDFury",
            update_interval=timedelta(seconds=10),
        )
        self.host = host
        self.brdinfo = brdinfo
        self.confinfo = confinfo
        self.device_info = DeviceInfo(
            identifiers={(DOMAIN, brdinfo["serial"])},
            name=brdinfo["hostname"],
            manufacturer="HDFury",
            model=brdinfo["hostname"].split('-')[0],
            serial_number=brdinfo["serial"],
            sw_version=brdinfo["version"].removeprefix("FW: "),
            hw_version=brdinfo["pcbv"],
            configuration_url=get_base_url(host),
            connections={(dr.CONNECTION_NETWORK_MAC, confinfo["macaddr"])},
        )

    async def _async_update_data(self):
        data = await fetch_json(get_info_url(self.host))
        if not data:
            raise UpdateFailed("Failed to fetch infopage.ssi")
        return data

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    hass.data.setdefault(DOMAIN, {})

    host = entry.data["host"]
    brdinfo = await fetch_json(get_brd_url(host))
    if not brdinfo:
        _LOGGER.error("Failed to fetch board info from %s", host)
        return False

    confinfo = await fetch_json(get_conf_url(host))
    if not confinfo:
        _LOGGER.error("Failed to fetch config info from %s", host)
        return False

    coordinator = HDFuryCoordinator(hass, host, brdinfo, confinfo)
    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unloaded:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unloaded
