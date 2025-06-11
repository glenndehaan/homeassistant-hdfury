import asyncio
import logging

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import HDFuryCoordinator
from .const import DOMAIN, SWITCH_MAP
from .helpers import get_cmd_url

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback,
):
    """Set up switches using the platform schema."""

    coordinator: HDFuryCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    entities = []
    for key, (name, cmd, icon, category) in SWITCH_MAP.items():
        if key in coordinator.confinfo:
            entities.append(HDFurySwitch(coordinator, key, name, cmd, icon, category))

    async_add_entities(entities, True)

class HDFurySwitch(CoordinatorEntity, SwitchEntity):
    """Base HDFury Switch Class."""

    def __init__(self, coordinator: HDFuryCoordinator, key: str, name: str, cmd: str, icon: str, category: str):
        """Register Switch."""

        super().__init__(coordinator)
        self._key = key
        self._cmd = cmd
        self._attr_name = f"{coordinator.device_name} {name}"
        self._attr_icon = icon
        self._attr_unique_id = f"{coordinator.brdinfo['serial']}_{key}"
        self._attr_device_info = coordinator.device_info
        if category == "configuration":
            self._attr_entity_category = EntityCategory.CONFIG

    @property
    def is_on(self):
        """Set Switch State."""

        return self.coordinator.confinfo.get(self._key) in ["1", "on", "true"]

    async def async_turn_on(self, **kwargs):
        """Handle Switch On Event."""

        url = get_cmd_url(self.coordinator.host, self._cmd, "on")
        _LOGGER.debug("Sending %s command to HDFury: %s", self._cmd, url)

        async with async_get_clientsession(self.hass).get(url) as response:
            if response.status == 200:
                _LOGGER.info("%s command sent successfully", self._cmd)
                await asyncio.sleep(2)  # Wait for the device to process new state
                await self.coordinator.async_request_refresh()
            else:
                _LOGGER.error("Failed to %s HDFury device: %s", self._cmd, await response.text())

    async def async_turn_off(self, **kwargs):
        """Handle Switch Off Event."""

        url = get_cmd_url(self.coordinator.host, self._cmd, "off")
        async with async_get_clientsession(self.hass).get(url) as response:
            if response.status == 200:
                _LOGGER.info("%s command sent successfully", self._cmd)
                await asyncio.sleep(2)  # Wait for the device to process new state
                await self.coordinator.async_request_refresh()
            else:
                _LOGGER.error("Failed to %s HDFury device: %s", self._cmd, await response.text())

    @property
    def extra_state_attributes(self):
        """Set Select State Attributes."""

        return {
            "raw_value": self.coordinator.confinfo.get(self._key)
        }
