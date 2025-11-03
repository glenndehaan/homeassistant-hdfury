import asyncio
import logging

from aiohttp import ClientError

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import HDFuryCoordinator
from .helpers import get_cmd_url

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback,
):
    """Set up buttons using the platform schema."""

    coordinator: HDFuryCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    async_add_entities([HDFuryRebootButton(coordinator), HDFuryIssueHotplugButton(coordinator)], True)

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

        url = get_cmd_url(self.coordinator.host, "reboot")
        session = async_get_clientsession(self.hass)

        _LOGGER.debug("Sending reboot command to HDFury: %s", url)

        try:
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    _LOGGER.info("Reboot command sent successfully to %s", url)
                else:
                    body = await response.text()
                    _LOGGER.error("Failed to reboot HDFury device (%s): %s", response.status, body)

        except asyncio.TimeoutError:
            _LOGGER.warning("Timeout while sending reboot command to %s", url)
        except ClientError as err:
            _LOGGER.warning("Client error while sending reboot command to %s: %s", url, err)
        except Exception as err:
            _LOGGER.exception("Unexpected error while sending reboot command to %s: %s", url, err)

class HDFuryIssueHotplugButton(CoordinatorEntity, ButtonEntity):
    """HDFury Issue Hotplug Button Class."""

    def __init__(self, coordinator: HDFuryCoordinator):
        """Register Button."""

        super().__init__(coordinator)
        self._attr_name = f"{coordinator.device_name} Issue Hotplug"
        self._attr_unique_id = f"{coordinator.brdinfo['serial']}_issue_hotplug"
        self._attr_device_info = coordinator.device_info
        self._attr_entity_category = EntityCategory.CONFIG
        self._attr_icon = "mdi:restart"

    async def async_press(self):
        """Handle Button Press."""

        url = get_cmd_url(self.coordinator.host, "hotplug")
        session = async_get_clientsession(self.hass)

        _LOGGER.debug("Sending hotplug command to HDFury: %s", url)

        try:
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    _LOGGER.info("Hotplug command sent successfully to %s", url)
                else:
                    body = await response.text()
                    _LOGGER.error("Failed to hotplug HDFury device (%s): %s", response.status, body)

        except asyncio.TimeoutError:
            _LOGGER.warning("Timeout while sending hotplug command to %s", url)
        except ClientError as err:
            _LOGGER.warning("Client error while sending hotplug command to %s: %s", url, err)
        except Exception as err:
            _LOGGER.exception("Unexpected error while sending hotplug command to %s: %s", url, err)
