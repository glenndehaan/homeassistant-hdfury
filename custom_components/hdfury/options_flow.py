import voluptuous as vol

from homeassistant import config_entries

from .const import INPUT_LABELS

class HDFuryOptionsFlow(config_entries.OptionsFlow):
    """Handle Options Flow for HDFury."""

    def __init__(self, config_entry):
        """Register Options Flow."""

        super().__init__()

    async def async_step_init(self, user_input=None):
        """Handle Options."""

        if user_input is not None:
            return self.async_create_entry(title="", data={"option_labels": user_input})

        current_labels = self.config_entry.options.get("option_labels", {})
        schema = vol.Schema({
            vol.Optional(opt, default=current_labels.get(opt, INPUT_LABELS[opt])): str
            for opt in INPUT_LABELS
        })

        return self.async_show_form(
            step_id="init",
            data_schema=schema,
            description_placeholders={"entity": self.config_entry.title},
        )
