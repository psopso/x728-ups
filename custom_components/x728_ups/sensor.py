import logging
from datetime import timedelta
from smbus2 import SMBus
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import PERCENTAGE, UnitOfElectricPotential

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(seconds=30)

def setup_platform(hass, config, add_entities, discovery_info=None):
    try:
        bus = SMBus(1)
        # Testovací čtení
        bus.read_word_data(0x36, 0x02)
        add_entities([
            X728VoltageSensor(bus), 
            X728CapacitySensor(bus),
            X728StatusSensor(bus)
        ], True)
    except Exception as e:
        _LOGGER.error("Nepodařilo se inicializovat X728 přes I2C: %s", e)

class X728SensorBase(SensorEntity):
    def __init__(self, bus):
        self._bus = bus
        self._state = None

    def _read_word_swapped(self, reg):
        read = self._bus.read_word_data(0x36, reg)
        return ((read & 0xFF) << 8) | (read >> 8)

class X728VoltageSensor(X728SensorBase):
    _attr_name = "X728 Battery Voltage"
    _attr_unique_id = "x728_battery_voltage"
    _attr_native_unit_of_measurement = UnitOfElectricPotential.VOLT
    _attr_device_class = "voltage"

    def update(self):
        try:
            val = self._read_word_swapped(0x02)
            self._state = round(val * 1.25 / 1000 / 16, 2)
        except Exception:
            self._state = None

    @property
    def native_value(self):
        return self._state

class X728CapacitySensor(X728SensorBase):
    _attr_name = "X728 Battery Capacity"
    _attr_unique_id = "x728_battery_capacity"
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_device_class = "battery"

    def update(self):
        try:
            val = self._read_word_swapped(0x04)
            self._state = min(100, round(val / 256, 1))
        except Exception:
            self._state = None

    @property
    def native_value(self):
        return self._state

class X728StatusSensor(X728SensorBase):
    _attr_name = "X728 UPS Status"
    _attr_unique_id = "x728_ups_status"
    _attr_icon = "mdi:power-plug"

    def update(self):
        try:
            # Odhad stavu na základě napětí
            # Li-ion baterie nad 4.1V se obvykle nabíjejí nebo jsou plné
            v = self._read_word_swapped(0x02) * 1.25 / 1000 / 16
            self._state = "Nabíjení / AC OK" if v > 4.05 else "Běh z baterie"
        except Exception:
            self._state = "Chyba"

    @property
    def native_value(self):
        return self._state