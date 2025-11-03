from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, PLATFORMS
from .helpers import fetch_json, get_base_url, get_brd_url, get_conf_url, get_info_url

_LOGGER = logging.getLogger(__name__)

class HDFuryCoordinator(DataUpdateCoordinator):
    """HDFury Device Coordinator Class."""

    def __init__(self, hass: HomeAssistant, host: str, brdinfo: dict, confinfo: dict):
        """Register HDFury Device."""

        super().__init__(
            hass,
            _LOGGER,
            name="HDFury",
            update_interval=timedelta(seconds=30),
        )
        self.host = host
        self.brdinfo = brdinfo
        self.confinfo = confinfo
        self.device_name = f"HDFury {brdinfo["hostname"]}"
        self.device_info = DeviceInfo(
            identifiers={(DOMAIN, brdinfo["serial"])},
            name=f"HDFury {brdinfo["hostname"]}",
            manufacturer="HDFury",
            model=brdinfo["hostname"].split('-')[0],
            serial_number=brdinfo["serial"],
            sw_version=brdinfo["version"].removeprefix("FW: "),
            hw_version=brdinfo.get("pcbv"),
            configuration_url=get_base_url(host),
            connections={(dr.CONNECTION_NETWORK_MAC, confinfo["macaddr"])},
        )

    async def _async_update_data(self):
        """Poll HDFury Data."""

        data = await fetch_json(self.hass, get_info_url(self.host))
        if not data:
            raise UpdateFailed("Failed to fetch infopage.ssi")

        # Also update confinfo on every poll
        conf_data = await fetch_json(self.hass, get_conf_url(self.host))
        if conf_data:
            self.confinfo = conf_data
        else:
            _LOGGER.warning("Failed to fetch confinfo.ssi; retaining previous confinfo")

        return data

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up HDFury from a config entry."""

    hass.data.setdefault(DOMAIN, {})

    host = entry.data["host"]
    brdinfo = await fetch_json(hass, get_brd_url(host))
    if not brdinfo:
        _LOGGER.error("Failed to fetch board info from %s", host)
        return False

    confinfo = await fetch_json(hass, get_conf_url(host))
    if not confinfo:
        _LOGGER.error("Failed to fetch config info from %s", host)
        return False

    coordinator = HDFuryCoordinator(hass, host, brdinfo, confinfo)
    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a HDFury config entry."""

    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unloaded:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unloaded

async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Reload integration when options are updated."""

    await hass.config_entries.async_reload(entry.entry_id)
