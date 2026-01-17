from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data["x728_ups"][entry.entry_id]
    add_entities([
        X728Voltage(coordinator),
        X728Capacity(coordinator),
    ])

class X728Voltage(SensorEntity):
    _attr_name = "X728 Battery Voltage"
    _attr_unit_of_measurement = "V"

    def __init__(self, coordinator):
        self.coordinator = coordinator

    @property
    def state(self):
        return self.coordinator.data.get("voltage")

    async def async_update(self):
        await self.coordinator.async_request_refresh()

class X728Capacity(SensorEntity):
    _attr_name = "X728 Battery Capacity"
    _attr_unit_of_measurement = "%"

    def __init__(self, coordinator):
        self.coordinator = coordinator

    @property
    def state(self):
        return self.coordinator.data["capacity"]

    async def async_update(self):
        await self.coordinator.async_request_refresh()
