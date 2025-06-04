import logging

import aiohttp

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import HDFuryCoordinator
from .const import DOMAIN, INPUT_OPTIONS, SELECT_MAP
from .helpers import get_cmd_insel_url

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback,
):
    """Set up selects using the platform schema."""

    coordinator: HDFuryCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    # Load custom labels if present
    custom_labels = config_entry.options.get("option_labels", {})

    entities = []
    for key, (name, icon) in SELECT_MAP.items():
        if key in coordinator.data:
            tx_index = 0 if "0" in key else 1
            copy_label = f"Copy TX{1 - tx_index}"

            # Build a custom label map for this TX selector
            label_map = {
                k: (custom_labels.get(v, v) if k != "4" else copy_label)
                for k, v in INPUT_OPTIONS.items()
            }
            reverse_label_map = {v: k for k, v in label_map.items()}

            entities.append(HDFuryPortSelect(
                coordinator, key, name, icon, label_map, reverse_label_map
            ))

    async_add_entities(entities, True)

class HDFuryPortSelect(CoordinatorEntity, SelectEntity):
    """Class to handle fetching and storing HDFury Port Select data."""

    def __init__(self, coordinator: HDFuryCoordinator, key: str, name: str, icon: str, label_map: dict[str, str], reverse_map: dict[str, str]):
        """Register Select."""

        super().__init__(coordinator)
        self._key = key
        self._label_map = label_map          # Maps raw values to user-friendly labels
        self._reverse_map = reverse_map      # Maps labels back to raw values
        self._raw_value = None

        self._attr_name = f"{coordinator.device_name} {name}"
        self._attr_icon = icon
        self._attr_unique_id = f"{coordinator.brdinfo['serial']}_{key}"
        self._attr_device_info = coordinator.device_info
        self._attr_options = list(label_map.values())

    @property
    def current_option(self):
        """Set Current Select Option."""

        raw_value = self.coordinator.data.get(self._key)
        self._raw_value = raw_value
        return self._label_map.get(raw_value, f"Unknown ({raw_value})")

    @property
    def extra_state_attributes(self):
        """Set Select State Attributes."""

        return {
            "raw_value": self._raw_value
        }

    @property
    def available(self) -> bool:
        """Disable Port Select when following other TX."""

        return self._raw_value != "4"

    async def async_select_option(self, option: str):
        """Handle Port Select."""

        raw_value = self._reverse_map.get(option)
        if raw_value is None:
            _LOGGER.warning("Invalid input option selected: %s", option)
            return

        _LOGGER.debug("Setting %s to %s", self._key, raw_value)
        url = get_cmd_insel_url(self.coordinator.host, f"{raw_value}%204")

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, timeout=5) as response:
                    if response.status != 200:
                        _LOGGER.warning(
                            "Failed to switch input: %s (%s)", url, response.status
                        )
            except Exception as e:
                _LOGGER.error("Error switching input: %s", e)

        self.coordinator.data[self._key] = raw_value
        await self.coordinator.async_request_refresh()
