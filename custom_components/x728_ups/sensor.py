from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        X728Voltage(coordinator, entry.entry_id),
        X728Capacity(coordinator, entry.entry_id),
    ])

class X728Voltage(CoordinatorEntity, SensorEntity):
    _attr_name = "X728 Battery Voltage"
    _attr_unit_of_measurement = "V"

    def __init__(self, coordinator, entry_id):
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry_id}_voltage"

    @property
    def native_value(self):
        return self.coordinator.data.get("voltage")

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "x728_ups")},
            "name": "Suptronics X728 UPS",
        }

    @property
    def available(self):
        return self.coordinator.data.get("voltage") is not None

class X728Capacity(CoordinatorEntity, SensorEntity):
    _attr_name = "X728 Battery Capacity"
    _attr_unit_of_measurement = "%"

    def __init__(self, coordinator, entry_id):
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry_id}_capacity"

    @property
    def native_value(self):
        return self.coordinator.data.get("capacity")

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "x728_ups")},
            "name": "Suptronics X728 UPS",
        }

    @property
    def available(self):
        return self.coordinator.data.get("capacity") is not None
