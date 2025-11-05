"""Diagnostics for HDFury Integration."""

from typing import Any

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .coordinator import HDFuryCoordinator


async def async_get_config_entry_diagnostics(
        hass: HomeAssistant, entry: ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator: HDFuryCoordinator = hass.data[DOMAIN][entry.entry_id]

    return async_redact_data(
        coordinator.data, ["ipaddress", "serial", "staticip", "activeip", "macaddr"]
    )
