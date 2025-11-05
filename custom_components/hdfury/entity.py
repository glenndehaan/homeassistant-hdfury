"""Base class for HDFury entities."""

from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import HDFuryCoordinator
from .helpers import get_base_url


class HDFuryEntity(CoordinatorEntity[HDFuryCoordinator]):
    """Common elements for all entities."""

    def __init__(
            self,
            coordinator: HDFuryCoordinator,
            key: str
    ) -> None:
        """Initialize the entity."""

        super().__init__(coordinator)

        self._key = key

        self._attr_unique_id = f"{coordinator.data["board"]["serial"]}_{key}"
        self._attr_translation_key = key.lower()
        self._attr_has_entity_name = True
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.data["board"]["serial"])},
            name=f"HDFury {coordinator.data["board"]["hostname"]}",
            manufacturer="HDFury",
            model=coordinator.data["board"]["hostname"].split("-")[0],
            serial_number=coordinator.data["board"]["serial"],
            sw_version=coordinator.data["board"]["version"].removeprefix("FW: "),
            hw_version=coordinator.data["board"].get("pcbv"),
            configuration_url=get_base_url(coordinator.host),
            connections={(dr.CONNECTION_NETWORK_MAC, coordinator.data["config"]["macaddr"])},
        )
