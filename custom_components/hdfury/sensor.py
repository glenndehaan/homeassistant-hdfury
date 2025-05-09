from datetime import timedelta
import json
import logging

import aiohttp

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import (
    DIAGNOSTIC_KEYS,
    DOMAIN,
    SENSOR_MAP,
    get_base_url,
    get_brd_url,
    get_info_url,
)

_LOGGER = logging.getLogger(__name__)

async def fetch_json(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    text = await resp.text()
                    return json.loads(text)
                _LOGGER.error("Non-200 response: %s", resp.status)
    except Exception as e:
        _LOGGER.error("Error fetching %s: %s", url, e)
    return {}

class HDFuryCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, host: str, brdinfo: dict):
        super().__init__(
            hass,
            _LOGGER,
            name="HDFury VRROOM",
            update_interval=timedelta(seconds=10),
        )
        self.host = host
        self.brdinfo = brdinfo
        self.device_info = DeviceInfo(
            identifiers={(DOMAIN, brdinfo["serial"])},
            name=brdinfo["hostname"],
            manufacturer="HDFury",
            model="VRROOM",
            serial_number=brdinfo["serial"],
            sw_version=brdinfo["version"].removeprefix("FW: "),
            hw_version=brdinfo["pcbv"],
            configuration_url=get_base_url(host),
        )

    async def _async_update_data(self):
        data = await fetch_json(get_info_url(self.host))
        if not data:
            raise UpdateFailed("Failed to fetch infopage.ssi")
        return data

async def async_setup_entry(
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback,
):
    host = config_entry.data["host"]
    brdinfo = await fetch_json(get_brd_url(host))
    if not brdinfo:
        _LOGGER.error("Failed to fetch board info from %s", host)
        return

    coordinator = HDFuryCoordinator(hass, host, brdinfo)
    await coordinator.async_config_entry_first_refresh()

    entities = []
    for key, (name, icon) in SENSOR_MAP.items():
        if key in coordinator.data:
            entities.append(HDFurySensor(coordinator, key, name, icon))

    async_add_entities(entities, True)

class HDFurySensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: HDFuryCoordinator, key: str, name: str, icon: str):
        super().__init__(coordinator)
        self._key = key
        self._attr_name = name
        self._attr_icon = icon
        self._attr_unique_id = f"{coordinator.brdinfo['serial']}_{key}"
        self._attr_device_info = coordinator.device_info
        if key in DIAGNOSTIC_KEYS:
            self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def native_value(self):
        return self.coordinator.data.get(self._key)
