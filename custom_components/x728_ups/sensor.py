from homeassistant.components.sensor import SensorEntity
from smbus2 import SMBus
from .const import *

async def async_setup_platform(hass, config, add_entities, discovery_info=None):
    bus = SMBus(I2C_BUS)
    add_entities([
        X728Voltage(bus),
        X728Capacity(bus),
    ])


class X728Voltage(SensorEntity):
    _attr_name = "X728 Battery Voltage"
    _attr_unit_of_measurement = "V"
    _attr_icon = "mdi:battery"

    def __init__(self, bus):
        self.bus = bus
        self._state = None

    def update(self):
        raw = self.bus.read_word_data(I2C_ADDR, REG_VOLTAGE)
        raw = ((raw >> 8) | (raw << 8)) & 0xFFFF
        self._state = round(raw * 1.25 / 1000, 2)

    @property
    def state(self):
        return self._state


class X728Capacity(SensorEntity):
    _attr_name = "X728 Battery Capacity"
    _attr_unit_of_measurement = "%"
    _attr_icon = "mdi:battery-percent"

    def __init__(self, bus):
        self.bus = bus
        self._state = None

    def update(self):
        raw = self.bus.read_word_data(I2C_ADDR, REG_CAPACITY)
        raw = ((raw >> 8) | (raw << 8)) & 0xFFFF
        self._state = round(raw / 256, 1)

    @property
    def state(self):
        return self._state
