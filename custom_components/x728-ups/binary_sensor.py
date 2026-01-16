# binary_sensor.py
from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass
import RPi.GPIO as GPIO

def setup_platform(hass, config, add_entities, discovery_info=None):
    add_entities([X728ACSensor(), X728LowBatterySensor()], True)

class X728ACSensor(BinarySensorEntity):
    def __init__(self):
        self._attr_name = "X728 AC Power Status"
        self._attr_device_class = BinarySensorDeviceClass.POWER
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(6, GPIO.IN)

    @property
    def is_on(self):
        # GPIO 6 je HIGH, když je připojen adaptér
        return GPIO.input(6) == GPIO.HIGH

class X728LowBatterySensor(BinarySensorEntity):
    def __init__(self):
        self._attr_name = "X728 Low Battery"
        self._attr_device_class = BinarySensorDeviceClass.BATTERY
        GPIO.setup(26, GPIO.IN)

    @property
    def is_on(self):
        return GPIO.input(26) == GPIO.HIGH
        