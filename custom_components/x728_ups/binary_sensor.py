from homeassistant.components.binary_sensor import BinarySensorEntity
import gpiod
from .const import *

async def async_setup_platform(hass, config, add_entities, discovery_info=None):
    add_entities([X728PowerLoss()])


class X728PowerLoss(BinarySensorEntity):
    _attr_name = "X728 Power Loss"
    _attr_device_class = "power"

    def __init__(self):
        self.chip = gpiod.Chip(GPIO_CHIP)
        self.line = self.chip.get_line(PIN_POWER_LOSS)
        self.line.request(
            consumer="x728",
            type=gpiod.LINE_REQ_DIR_IN
        )
        self._state = False

    def update(self):
        # 0 = napájení pryč
        self._state = self.line.get_value() == 0

    @property
    def is_on(self):
        return self._state
