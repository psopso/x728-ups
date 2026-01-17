from homeassistant.components.button import ButtonEntity
from homeassistant.core import HomeAssistant
from .const import DOMAIN

async def async_setup_platform(hass, config, add_entities, discovery_info=None):
    add_entities([X728ShutdownButton(hass)])


class X728ShutdownButton(ButtonEntity):
    _attr_name = "X728 Shutdown Host"
    _attr_icon = "mdi:power"

    def __init__(self, hass: HomeAssistant):
        self.hass = hass

    async def async_press(self):
        await self.hass.services.async_call(
            DOMAIN,
            "shutdown_host",
            {}
        )
