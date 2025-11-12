"""Select platform for HDFury Integration."""

from typing import Any

from hdfury import OPERATION_MODES, TX0_INPUT_PORTS, TX1_INPUT_PORTS, HDFuryError

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import DOMAIN
from .coordinator import HDFuryCoordinator
from .entity import HDFuryEntity


SELECT_PORTS: dict[str, dict[str, str]] = {
    "portseltx0": TX0_INPUT_PORTS,
    "portseltx1": TX1_INPUT_PORTS,
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up selects using the platform schema."""

    coordinator: HDFuryCoordinator = entry.runtime_data

    # Load custom labels if present
    custom_labels = entry.options.get("option_labels", {})

    entities: list[HDFuryEntity] = []
    for key, (labels) in SELECT_PORTS.items():
        if key in coordinator.data["info"]:
            # Build a custom label map for this TX selector
            label_map = {
                k: (custom_labels.get(v, v))
                for k, v in labels.items()
            }

            entities.append(HDFuryPortSelect(coordinator, key, label_map))

    # Add OPMODE select if present
    if "opmode" in coordinator.data["info"]:
        entities.append(HDFuryOpModeSelect(coordinator, "opmode"))

    async_add_entities(entities, True)


class HDFuryPortSelect(HDFuryEntity, SelectEntity):
    """Class to handle fetching and storing HDFury Port Select data."""

    def __init__(
        self, coordinator: HDFuryCoordinator, key: str, label_map: dict[str, str]
    ) -> None:
        """Register Select."""

        super().__init__(coordinator, key)

        self._attr_options = list(label_map.values())
        self._raw_value = None

        # Maps raw values to user-friendly labels
        self._label_map = label_map
        # Build reverse lookup for command sending
        self._reverse_map = {v: k for k, v in label_map.items()}

    @property
    def current_option(self) -> str:
        """Set Current Select Option."""

        raw_value = self.coordinator.data["info"].get(self._key)
        self._raw_value = raw_value
        return self._label_map.get(raw_value, f"Unknown ({raw_value})")

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Set Select State Attributes."""

        return {"raw_value": self._raw_value}

    async def async_select_option(self, option: str) -> None:
        """Handle Port Select."""

        # Map user-friendly label back to raw input value
        raw_value = self._reverse_map.get(option)
        if raw_value is None:
            raise HomeAssistantError(
                translation_domain=DOMAIN,
                translation_key="data_error",
                translation_placeholders={"error": str(f"Invalid input option selected: {option}")},
            )

        # Update local data first
        self.coordinator.data["info"][self._key] = raw_value

        # Remap both TX0 and TX1 current selections
        tx0_raw = self.coordinator.data["info"].get("portseltx0")
        tx1_raw = self.coordinator.data["info"].get("portseltx1")

        # If either missing, raise exception to avoid incomplete updates
        if tx0_raw is None or tx1_raw is None:
            raise HomeAssistantError(
                translation_domain=DOMAIN,
                translation_key="data_error",
                translation_placeholders={"error": str(f"TX states incomplete: tx0={tx0_raw}, tx1={tx1_raw}")},
            )

        # Send command to device
        try:
            await self.coordinator.client.set_port_selection(tx0_raw, tx1_raw)
        except HDFuryError as error:
            raise HomeAssistantError(
                translation_domain=DOMAIN,
                translation_key="communication_error",
                translation_placeholders={"error": str(error)},
            ) from error

        # Trigger HA state refresh
        await self.coordinator.async_request_refresh()


class HDFuryOpModeSelect(HDFuryEntity, SelectEntity):
    """Handle operation mode selection (opmode)."""

    def __init__(self, coordinator: HDFuryCoordinator, key: str) -> None:
        """Initialize OpMode select entity."""

        super().__init__(coordinator, key)

        self._attr_options = list(OPERATION_MODES.values())
        self._raw_value = None

        # Build reverse lookup for command sending
        self._reverse_map = {v: k for k, v in OPERATION_MODES.items()}

    @property
    def current_option(self) -> str:
        """Return the current operation mode."""

        raw_value = self.coordinator.data["info"].get(self._key)
        self._raw_value = raw_value
        return OPERATION_MODES.get(raw_value, f"Unknown ({raw_value})")

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Expose raw value for debugging."""

        return {"raw_value": self._raw_value}

    async def async_select_option(self, option: str) -> None:
        """Change the operation mode."""

        # Map user-friendly label back to raw input value
        raw_value = self._reverse_map.get(option)
        if raw_value is None:
            raise HomeAssistantError(
                translation_domain=DOMAIN,
                translation_key="data_error",
                translation_placeholders={"error": str(f"Invalid input option selected: {option}")},
            )

        # Update local data first
        self.coordinator.data["info"][self._key] = raw_value

        # Send command to device
        try:
            await self.coordinator.client.set_operation_mode(raw_value)
        except HDFuryError as error:
            raise HomeAssistantError(
                translation_domain=DOMAIN,
                translation_key="communication_error",
                translation_placeholders={"error": str(error)},
            ) from error

        # Trigger HA state refresh
        await self.coordinator.async_request_refresh()
