from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([X728PowerLoss(coordinator, entry.entry_id)])

class X728PowerLoss(CoordinatorEntity, BinarySensorEntity):
    _attr_name = "X728 Power Loss"
    _attr_device_class = "power"

    def __init__(self, coordinator, entry_id):
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry_id}_power_loss"

    @property
    def is_on(self):
        val = self.coordinator.data.get("power_loss")
        return val if val is not None else False

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "x728_ups")},
            "name": "Suptronics X728 UPS",
        }

    @property
    def available(self):
        return self.coordinator.data.get("power_loss") is not None
