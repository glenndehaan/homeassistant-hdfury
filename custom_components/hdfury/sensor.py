import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import HDFuryCoordinator
from .const import DOMAIN, SENSOR_MAP

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback,
):
    """Set up buttons using the platform schema."""

    coordinator: HDFuryCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    entities = []
    for key, (name, icon, category) in SENSOR_MAP.items():
        if key in coordinator.data:
            entities.append(HDFurySensor(coordinator, key, name, icon, category))

    async_add_entities(entities, True)

class HDFurySensor(CoordinatorEntity, SensorEntity):
    """Base HDFury Sensor Class."""

    def __init__(self, coordinator: HDFuryCoordinator, key: str, name: str, icon: str, category: str):
        """Register Sensor."""

        super().__init__(coordinator)
        self._key = key
        self._attr_name = f"{coordinator.device_name} {name}"
        self._attr_icon = icon
        self._attr_unique_id = f"{coordinator.brdinfo['serial']}_{key}"
        self._attr_device_info = coordinator.device_info
        if category == "diagnostic":
            self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def native_value(self):
        """Set Sensor Value."""

        return self.coordinator.data.get(self._key)
