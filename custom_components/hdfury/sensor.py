"""Sensor platform for HDFury Integration."""

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import HDFuryCoordinator
from .entity import HDFuryEntity


SENSORS: list[str] = [
    "RX0",
    "RX1",
    "TX0",
    "TX1",
    "AUD0",
    "AUD1",
    "AUDOUT",
    "SINK0",
    "EDIDA0",
    "SINK1",
    "EDIDA1",
    "SINK2",
    "EDIDA2",
    "EARCRX",
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up buttons using the platform schema."""

    coordinator: HDFuryCoordinator = entry.runtime_data

    entities: list[HDFuryEntity] = [
        HDFurySensor(coordinator, key)
        for key in SENSORS
        if key in coordinator.data["info"]
    ]

    async_add_entities(entities, True)


class HDFurySensor(HDFuryEntity, SensorEntity):
    """Base HDFury Sensor Class."""

    def __init__(self, coordinator: HDFuryCoordinator, key: str) -> None:
        """Register Sensor."""

        super().__init__(coordinator, key)

        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def native_value(self) -> str:
        """Set Sensor Value."""

        return self.coordinator.data["info"].get(self._key)
