"""The HDFury Integration."""

from awesomeversion import AwesomeVersion

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform, __version__ as HA_VERSION
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import issue_registry as ir

from .const import DOMAIN
from .coordinator import HDFuryCoordinator

PLATFORMS = [
    Platform.BUTTON,
    Platform.SELECT,
    Platform.SENSOR,
    Platform.SWITCH,
]

CORE_VERSION = AwesomeVersion("2026.2.0")


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up HDFury as config entry."""

    coordinator = HDFuryCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    if AwesomeVersion(HA_VERSION) < CORE_VERSION:
        return True

    ir.async_create_issue(
        hass,
        DOMAIN,
        "custom_component_migration",
        learn_more_url="https://github.com/glenndehaan/homeassistant-hdfury#migration-to-core",
        is_fixable=False,
        is_persistent=False,
        severity=ir.IssueSeverity.WARNING,
        translation_key="custom_component_migration",
    )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a HDFury config entry."""

    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
