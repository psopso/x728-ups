from homeassistant.components.button import ButtonEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data["x728_ups"][entry.entry_id]
    async_add_entities([X728ShutdownButton(coordinator)])


class X728ShutdownButton(CoordinatorEntity, ButtonEntity):
    _attr_name = "X728 Shutdown Host"
    _attr_icon = "mdi:power"
    _attr_unique_id = "x728_shutdown_button"

    def __init__(self, coordinator):
        super().__init__(coordinator)

    async def async_press(self):
        await self.coordinator.shutdown_host()
