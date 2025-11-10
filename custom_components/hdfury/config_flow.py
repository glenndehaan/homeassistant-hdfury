"""Config flow for HDFury Integration."""

import logging
from typing import Any

from hdfury import HDFuryAPI, HDFuryError
import voluptuous as vol

from homeassistant.config_entries import ConfigEntry, ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_HOST
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN
from .options_flow import HDFuryOptionsFlow

_LOGGER = logging.getLogger(__name__)


class HDFuryConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle Config Flow for HDFury."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle Initial Setup."""

        errors = {}

        if user_input is not None:
            host = user_input[CONF_HOST]

            # Check for existing entry with same host
            for entry in self._async_current_entries():
                if entry.data.get("host") == host:
                    errors["base"] = "already_configured"
                    break

            # Proceed normally (And check connection)
            if not errors:
                if await self._validate_connection(host):
                    return self.async_create_entry(
                        title=f"HDFury ({host})", data=user_input
                    )
                else:
                    errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required(CONF_HOST): str}),
            errors=errors,
        )

    async def _validate_connection(self, host: str) -> bool:
        """Try to fetch data to confirm it's a valid HDFury device."""

        client: HDFuryAPI = HDFuryAPI(host, async_get_clientsession(self.hass))

        try:
            await client.get_board()
        except HDFuryError as error:
            _LOGGER.error("%s", error)
            return False

        return True

    @staticmethod
    def async_get_options_flow(config_entry: ConfigEntry) -> HDFuryOptionsFlow:
        """Register Options Flow for HDFury."""

        return HDFuryOptionsFlow()
