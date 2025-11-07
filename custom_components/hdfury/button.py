"""Button platform for HDFury Integration."""

from collections.abc import Awaitable, Callable

from hdfury import HDFuryAPI, HDFuryError
from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import HDFuryCoordinator
from .entity import HDFuryEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up buttons using the platform schema."""

    coordinator: HDFuryCoordinator = entry.runtime_data

    async_add_entities(
        [
            HDFuryButton(coordinator, "reboot", lambda client: client.issue_reboot()),
            HDFuryButton(
                coordinator, "issue_hotplug", lambda client: client.issue_hotplug()
            ),
        ],
        True,
    )


class HDFuryButton(HDFuryEntity, ButtonEntity):
    """HDFury Button Class."""

    def __init__(
        self,
        coordinator: HDFuryCoordinator,
        key: str,
        press_fn: Callable[[HDFuryAPI], Awaitable[None]],
    ) -> None:
        """Register Button."""

        super().__init__(coordinator, key)

        self._attr_entity_category = EntityCategory.CONFIG
        self.press_fn = press_fn

    async def async_press(self):
        """Handle Button Press."""

        try:
            await self.press_fn(self.coordinator.client)
        except HDFuryError as error:
            raise HomeAssistantError(
                translation_domain=DOMAIN,
                translation_key="communication_error",
                translation_placeholders={"error": str(error)},
            ) from error
