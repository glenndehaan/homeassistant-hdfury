import asyncio
import logging

from aiohttp import ClientError

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, INPUT_OPTIONS, OPMODE_OPTIONS, SELECT_MAP
from .coordinator import HDFuryCoordinator
from .helpers import get_cmd_url

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

    # Add OPMODE select if present
    if "opmode" in coordinator.data:
        entities.append(HDFuryOpModeSelect(coordinator))

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

    async def async_select_option(self, option: str):
        """Handle Port Select."""

        # Map user-friendly label back to raw input value
        raw_value = self._reverse_map.get(option)
        if raw_value is None:
            _LOGGER.warning("Invalid input option selected: %s", option)
            return

        _LOGGER.debug("Setting %s to %s", self._key, raw_value)

        # Update local data first
        self.coordinator.data[self._key] = raw_value

        # --- Remap both TX0 and TX1 current selections ---
        tx0_raw = self.coordinator.data.get("portseltx0")
        tx1_raw = self.coordinator.data.get("portseltx1")

        # If either missing, skip to avoid incomplete updates
        if tx0_raw is None or tx1_raw is None:
            _LOGGER.error("TX states incomplete: tx0=%s, tx1=%s", tx0_raw, tx1_raw)
            return

        # Construct combined URL (both TX inputs in same command)
        url = get_cmd_url(self.coordinator.host, "insel", f"{tx0_raw}%20{tx1_raw}")
        session = async_get_clientsession(self.hass)

        _LOGGER.debug("Sending combined insel command: %s", url)

        try:
            async with session.get(url, timeout=10) as response:
                if response.status != 200:
                    _LOGGER.warning("Failed to switch input on %s (HTTP %s)", url, response.status)
                else:
                    _LOGGER.debug("Successfully switched input via %s", url)

        except asyncio.TimeoutError:
            _LOGGER.warning("Timeout while switching input on %s", url)
        except ClientError as err:
            _LOGGER.warning("Client error while switching input on %s: %s", url, err)
        except Exception as err:
            _LOGGER.exception("Unexpected error while switching input on %s: %s", url, err)

        # Wait for the device to process new state
        await asyncio.sleep(2)
        # Trigger HA state refresh
        await self.coordinator.async_request_refresh()

class HDFuryOpModeSelect(CoordinatorEntity, SelectEntity):
    """Handle operation mode selection (opmode)."""

    def __init__(self, coordinator: HDFuryCoordinator):
        """Initialize OpMode select entity."""
        super().__init__(coordinator)

        self._key = "opmode"
        self._attr_name = f"{coordinator.device_name} Operation Mode"
        self._attr_icon = "mdi:cogs"
        self._attr_unique_id = f"{coordinator.brdinfo['serial']}_opmode"
        self._attr_device_info = coordinator.device_info
        self._attr_options = list(OPMODE_OPTIONS.values())

        # Build reverse lookup for command sending
        self._reverse_map = {v: k for k, v in OPMODE_OPTIONS.items()}
        self._raw_value = None

    @property
    def current_option(self):
        """Return the current operation mode."""
        raw_value = self.coordinator.data.get(self._key)
        self._raw_value = raw_value
        return OPMODE_OPTIONS.get(raw_value, f"Unknown ({raw_value})")

    @property
    def extra_state_attributes(self):
        """Expose raw value for debugging."""
        return {
            "raw_value": self._raw_value
        }

    async def async_select_option(self, option: str):
        """Change the operation mode."""
        raw_value = self._reverse_map.get(option)
        if raw_value is None:
            _LOGGER.warning("Invalid opmode selected: %s", option)
            return

        _LOGGER.debug("Setting operation mode to %s (%s)", option, raw_value)
        self.coordinator.data[self._key] = raw_value

        # Send command to device
        url = get_cmd_url(self.coordinator.host, "opmode", raw_value)
        session = async_get_clientsession(self.hass)

        _LOGGER.debug("Sending opmode command: %s", url)

        try:
            async with session.get(url, timeout=10) as response:
                if response.status != 200:
                    _LOGGER.warning("Failed to set opmode on %s (HTTP %s)", url, response.status)
                else:
                    _LOGGER.debug("Successfully set opmode on %s", url)

        except asyncio.TimeoutError:
            _LOGGER.warning("Timeout while setting opmode on %s", url)
        except ClientError as err:
            _LOGGER.warning("Client error while setting opmode on %s: %s", url, err)
        except Exception as err:
            _LOGGER.exception("Unexpected error setting opmode on %s: %s", url, err)

        # Wait for the device to process new state
        await asyncio.sleep(2)
        # Trigger HA state refresh
        await self.coordinator.async_request_refresh()
