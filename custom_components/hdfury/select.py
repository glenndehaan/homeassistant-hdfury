import logging

import aiohttp

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import HDFuryCoordinator
from .const import DOMAIN, INPUT_OPTIONS, REVERSE_INPUT_OPTIONS, SELECT_MAP
from .helpers import get_cmd_insel_url

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback,
):
    coordinator: HDFuryCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    entities = []
    for key, (name, icon) in SELECT_MAP.items():
        if key in coordinator.data:
            entities.append(HDFuryPortSelect(coordinator, key, name, icon))

    async_add_entities(entities, True)

class HDFuryPortSelect(CoordinatorEntity, SelectEntity):
    def __init__(self, coordinator, key, name, icon):
        super().__init__(coordinator)
        self._key = key
        self._attr_name = name
        self._attr_icon = icon
        self._attr_unique_id = f"{coordinator.brdinfo['serial']}_{key}"
        self._attr_device_info = coordinator.device_info
        self._attr_options = list(INPUT_OPTIONS.values())

    @property
    def current_option(self):
        # Pull live value from coordinator every update
        raw_value = self.coordinator.data.get("portseltx0", "0")
        return INPUT_OPTIONS.get(raw_value, f"Input {int(raw_value) + 1}")

    async def async_select_option(self, option: str):
        input_number = REVERSE_INPUT_OPTIONS.get(option)
        if input_number is None:
            _LOGGER.warning("Invalid input option selected: %s", option)
            return

        _LOGGER.debug("Setting %s to %s", self._key, input_number)

        url = get_cmd_insel_url(self.coordinator.host, f"{input_number}%204")

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, timeout=5) as response:
                    if response.status != 200:
                        _LOGGER.warning(
                            "Failed to switch input: %s (%s)", url, response.status
                        )
            except Exception as e:
                _LOGGER.error("Error switching input: %s", e)

        # Store and refresh data
        self.coordinator.data[self._key] = option
        await self.coordinator.async_request_refresh()
