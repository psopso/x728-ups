from homeassistant.components.binary_sensor import BinarySensorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data["x728_ups"][entry.entry_id]
    add_entities([X728PowerLoss(coordinator)])

class X728PowerLoss(BinarySensorEntity):
    _attr_name = "X728 Power Loss"
    _attr_device_class = "power"

    def __init__(self, coordinator):
        self.coordinator = coordinator

    @property
    def is_on(self):
        return bool(self.coordinator.data.get("power_loss"))

    async def async_update(self):
        await self.coordinator.async_request_refresh()
