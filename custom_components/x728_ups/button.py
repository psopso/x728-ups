from homeassistant.components.button import ButtonEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data["x728_ups"][entry.entry_id]
    add_entities([X728ShutdownButton(coordinator)])

class X728ShutdownButton(ButtonEntity):
    _attr_name = "X728 Shutdown Host"
    _attr_icon = "mdi:power"

    def __init__(self, coordinator):
        self.coordinator = coordinator

    async def async_press(self):
        await self.coordinator.shutdown_host()
