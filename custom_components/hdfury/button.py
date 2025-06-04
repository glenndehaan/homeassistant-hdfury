import logging

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import HDFuryCoordinator
from .const import DOMAIN
from .helpers import get_cmd_rst_url

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback,
):
    """Set up buttons using the platform schema."""

    coordinator: HDFuryCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    async_add_entities([HDFuryRebootButton(coordinator)], True)

class HDFuryRebootButton(CoordinatorEntity, ButtonEntity):
    """HDFury Reset Button Class."""

    def __init__(self, coordinator: HDFuryCoordinator):
        """Register Button."""

        super().__init__(coordinator)
        self._attr_name = f"{coordinator.device_name} Reboot"
        self._attr_unique_id = f"{coordinator.brdinfo['serial']}_reboot"
        self._attr_device_info = coordinator.device_info
        self._attr_entity_category = EntityCategory.CONFIG
        self._attr_icon = "mdi:restart"

    async def async_press(self):
        """Handle Button Press."""

        url = get_cmd_rst_url(self.coordinator.host)
        _LOGGER.debug("Sending reboot command to HDFury: %s", url)

        async with async_get_clientsession(self.hass).get(url) as response:
            if response.status == 200:
                _LOGGER.info("Reboot command sent successfully")
            else:
                _LOGGER.error("Failed to reboot HDFury device: %s", await response.text())
