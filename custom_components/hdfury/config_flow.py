import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST

from .const import DOMAIN
from .helpers import get_info_url

class HDFuryConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            host = user_input[CONF_HOST]
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
