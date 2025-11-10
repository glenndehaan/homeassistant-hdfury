"""Switch platform for HDFury Integration."""

from collections.abc import Awaitable, Callable
from typing import Any

from hdfury import HDFuryAPI, HDFuryError

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import DOMAIN, SWITCH_MAP
from .coordinator import HDFuryCoordinator
from .entity import HDFuryEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up switches using the platform schema."""

    coordinator: HDFuryCoordinator = entry.runtime_data

    entities: list[HDFuryEntity] = []
    for key, (set_value_fn) in SWITCH_MAP.items():
        if key in coordinator.data["config"]:
            entities.append(HDFurySwitch(coordinator, key, set_value_fn))

    async_add_entities(entities, True)


class HDFurySwitch(HDFuryEntity, SwitchEntity):
    """Base HDFury Switch Class."""

    def __init__(
        self,
        coordinator: HDFuryCoordinator,
        key: str,
        set_value_fn: Callable[[HDFuryAPI, str], Awaitable[None]],
    ) -> None:
        """Register Switch."""

        super().__init__(coordinator, key)

        self._attr_entity_category = EntityCategory.CONFIG
        self.set_value_fn = set_value_fn

    @property
    def is_on(self) -> bool:
        """Set Switch State."""

        return self.coordinator.data["config"].get(self._key) in ["1", "on", "true"]

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Handle Switch On Event."""

        try:
            await self.set_value_fn(self.coordinator.client, "on")
        except HDFuryError as error:
            raise HomeAssistantError(
                translation_domain=DOMAIN,
                translation_key="communication_error",
                translation_placeholders={"error": str(error)},
            ) from error

        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Handle Switch Off Event."""

        try:
            await self.set_value_fn(self.coordinator.client, "off")
        except HDFuryError as error:
            raise HomeAssistantError(
                translation_domain=DOMAIN,
                translation_key="communication_error",
                translation_placeholders={"error": str(error)},
            ) from error

        await self.coordinator.async_request_refresh()

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Set Select State Attributes."""

        return {"raw_value": self.coordinator.data["config"].get(self._key)}
