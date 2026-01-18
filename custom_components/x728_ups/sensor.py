from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

import logging
_LOGGER = logging.getLogger(__name__)
#_LOGGER.info("Pokus")

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data["x728_ups"][entry.entry_id]
    _LOGGER.info("Pred add entity")
    async_add_entities([
        X728Voltage(coordinator),
        X728Capacity(coordinator),
    ])


class X728Voltage(CoordinatorEntity, SensorEntity):
    _attr_name = "X728 Battery Voltage"
    _attr_unit_of_measurement = "V"
    _attr_unique_id = "x728_voltage"

    def __init__(self, coordinator):
        super().__init__(coordinator)

    @property
    def native_value(self):
        return self.coordinator.data.get("voltage")


class X728Capacity(CoordinatorEntity, SensorEntity):
    _attr_name = "X728 Battery Capacity"
    _attr_unit_of_measurement = "%"
    _attr_unique_id = "x728_capacity"

    def __init__(self, coordinator):
        super().__init__(coordinator)

    @property
    def native_value(self):
        return self.coordinator.data.get("capacity")
