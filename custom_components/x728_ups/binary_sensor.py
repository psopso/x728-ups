from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data["x728_ups"][entry.entry_id]
    async_add_entities([X728PowerLoss(coordinator)])


class X728PowerLoss(CoordinatorEntity, BinarySensorEntity):
    _attr_name = "X728 Power Loss"
    _attr_device_class = "power"
    _attr_unique_id = "x728_power_loss"

    def __init__(self, coordinator):
        super().__init__(coordinator)

    @property
    def is_on(self):
        return bool(self.coordinator.data.get("power_loss"))
