"""Button platform for HDFury Integration."""

import asyncio
import logging

from aiohttp import ClientError

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import HDFuryCoordinator
from .entity import HDFuryEntity
from .helpers import get_cmd_url

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback,
):
    """Set up buttons using the platform schema."""

    coordinator: HDFuryCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    async_add_entities(
        [
            HDFuryRebootButton(coordinator, "reboot", "Reboot"),
            HDFuryIssueHotplugButton(coordinator, "issue_hotplug", "Issue Hotplug"),
        ],
        True,
    )

class HDFuryRebootButton(HDFuryEntity, ButtonEntity):
    """HDFury Reset Button Class."""

    def __init__(self, coordinator: HDFuryCoordinator, key: str, name: str):
        """Register Button."""

        super().__init__(coordinator, key, name)

        self._attr_entity_category = EntityCategory.CONFIG

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

class HDFuryIssueHotplugButton(HDFuryEntity, ButtonEntity):
    """HDFury Issue Hotplug Button Class."""

    def __init__(self, coordinator: HDFuryCoordinator, key: str, name: str):
        """Register Button."""

        super().__init__(coordinator, key, name)

        self._attr_entity_category = EntityCategory.CONFIG

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
