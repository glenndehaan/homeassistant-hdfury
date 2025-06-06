import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST

from .const import DOMAIN
from .helpers import get_info_url
from .options_flow import HDFuryOptionsFlow

class HDFuryConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle Config Flow for HDFury."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle Initial Setup."""

        errors = {}

        if user_input is not None:
            host = user_input[CONF_HOST]

            # Check for existing entry with same host
            for entry in self._async_current_entries():
                if entry.data.get("host") == host:
                    errors["base"] = "already_configured"
                    break

            if not errors:
                # Proceed normally
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

    async def _validate_connection(self, host):
        """Try to fetch data to confirm it's a valid HDFury device."""

        url = get_info_url(host)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=5) as resp:
                    return resp.status == 200
        except Exception:
            return False
        return False

    def async_get_options_flow(config_entry):
        """Register Options Flow for HDFury."""

        return HDFuryOptionsFlow(config_entry)
