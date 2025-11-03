import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, PLATFORMS
from .coordinator import HDFuryCoordinator
from .helpers import fetch_json, get_brd_url, get_conf_url

_LOGGER = logging.getLogger(__name__)

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
