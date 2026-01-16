import logging
from datetime import timedelta
from smbus2 import SMBus
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import PERCENTAGE, UnitOfElectricPotential

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(seconds=60)

def setup_platform(hass, config, add_entities, discovery_info=None):
    bus = SMBus(1)  # I2C sběrnice 1 na RPi
    add_entities([X728VoltageSensor(bus), X728CapacitySensor(bus)], True)

class X728VoltageSensor(SensorEntity):
    def __init__(self, bus):
        self._bus = bus
        self._state = None
        self._attr_name = "X728 Battery Voltage"
        self._attr_unique_id = "x728_battery_voltage"
        self._attr_native_unit_of_measurement = UnitOfElectricPotential.VOLT

    def update(self):
        try:
            read = self._bus.read_word_data(0x36, 0x02)
            # Přepočet bytů (swap) a následně na Volty
            swapped = ((read & 0xFF) << 8) | (read >> 8)
            self._state = round(swapped * 1.25 / 1000 / 16, 2)
        except Exception as e:
            _LOGGER.error("Chyba čtení napětí z X728: %s", e)

    @property
    def native_value(self):
        return self._state

class X728CapacitySensor(SensorEntity):
    def __init__(self, bus):
        self._bus = bus
        self._state = None
        self._attr_name = "X728 Battery Capacity"
        self._attr_unique_id = "x728_battery_capacity"
        self._attr_native_unit_of_measurement = PERCENTAGE

    def update(self):
        try:
            read = self._bus.read_word_data(0x36, 0x04)
            swapped = ((read & 0xFF) << 8) | (read >> 8)
            self._state = round(swapped / 256, 1)
        except Exception as e:
            _LOGGER.error("Chyba čtení kapacity z X728: %s", e)

    @property
    def native_value(self):
        return self._state