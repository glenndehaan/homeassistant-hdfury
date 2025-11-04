"""Sensor platform for HDFury Integration."""

import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, SENSOR_MAP
from .coordinator import HDFuryCoordinator
from .entity import HDFuryEntity

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback,
):
    """Set up buttons using the platform schema."""

    coordinator: HDFuryCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    entities = []
    for key, (name, category) in SENSOR_MAP.items():
        if key in coordinator.data:
            entities.append(HDFurySensor(coordinator, key, name, category))

    async_add_entities(entities, True)

class HDFurySensor(HDFuryEntity, SensorEntity):
    """Base HDFury Sensor Class."""

    def __init__(self, coordinator: HDFuryCoordinator, key: str, name: str, category: str):
        """Register Sensor."""

        super().__init__(coordinator, key, name)

        if category == "diagnostic":
            self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def native_value(self):
        """Set Sensor Value."""

        return self.coordinator.data.get(self._key)
