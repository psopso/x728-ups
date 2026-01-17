from homeassistant.components.binary_sensor import BinarySensorEntity
import gpiod
from gpiod.line import Direction, Value
from .const import GPIO_CHIP, PIN_POWER_LOSS

import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(hass, config, add_entities, discovery_info=None):
    add_entities([X728PowerLoss()])


class X728PowerLoss(BinarySensorEntity):
    _attr_name = "X728 Power Loss"
    _attr_device_class = "power"

    def __init__(self):
        self._state = False

        self.chip = gpiod.Chip(GPIO_CHIP)

        settings = gpiod.LineSettings(
            direction=Direction.INPUT
        )

        self.request = self.chip.request_lines(
            consumer="x728",
            config={PIN_POWER_LOSS: settings}
        )

    def update(self):
        value = self.request.get_value(PIN_POWER_LOSS)
        # X728: 0 = power lost
        self._state = (value == Value.INACTIVE)
        _LOGGER.warning("Čtu GPIO stav: %s", value)

    @property
    def is_on(self):
        return self._state
