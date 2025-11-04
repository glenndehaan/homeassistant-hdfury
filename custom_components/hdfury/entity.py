"""Base class for HDFury entities."""

from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.entity import DeviceInfo

from .const import DOMAIN
from .coordinator import HDFuryCoordinator
from .helpers import get_base_url

class HDFuryEntity(CoordinatorEntity[HDFuryCoordinator]):
    """Common elements for all entities."""

    def __init__(
            self,
            coordinator: HDFuryCoordinator,
            key: str,
            name: str
    ) -> None:
        """Initialize the entity."""

        super().__init__(coordinator)

        self._key = key

        self._attr_name = name
        self._attr_unique_id = f"{coordinator.brdinfo['serial']}_{key}"
        self._attr_translation_key = key
        self._attr_has_entity_name = True
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.brdinfo["serial"])},
            name=f"HDFury {coordinator.brdinfo['hostname']}",
            manufacturer="HDFury",
            model=coordinator.brdinfo["hostname"].split("-")[0],
            serial_number=coordinator.brdinfo["serial"],
            sw_version=coordinator.brdinfo["version"].removeprefix("FW: "),
            hw_version=coordinator.brdinfo.get("pcbv"),
            configuration_url=get_base_url(coordinator.host),
            connections={(dr.CONNECTION_NETWORK_MAC, coordinator.confinfo["macaddr"])},
        )
