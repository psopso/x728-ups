from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.core import HomeAssistant
import gpiod
from gpiod.line import Direction, Value
from smbus2 import SMBus
from .const import *
import logging
import time

_LOGGER = logging.getLogger(__name__)

class X728Coordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant):
        super().__init__(
            hass,
            logger=_LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
        )

        # I2C
        self.bus = SMBus(I2C_BUS)

        # GPIO
        self.chip = gpiod.Chip(GPIO_CHIP)

        self.ext_button = self.chip.request_lines(
            consumer="x728_ext_button",
            config={PIN_EXT_BUTTON: gpiod.LineSettings(direction=Direction.INPUT)}
        )

        self.power_loss_req = self.chip.request_lines(
            consumer="x728_power",
            config={PIN_POWER_LOSS: gpiod.LineSettings(direction=Direction.INPUT)}
        )

        self.shutdown_req = self.chip.request_lines(
            consumer="x728_shutdown",
            config={PIN_SHUTDOWN: gpiod.LineSettings(
                direction=Direction.OUTPUT,
                output_value=Value.INACTIVE
            )}
        )

    async def _async_update_data(self):
        data = {}

        # --- GPIO ---
        try:
            power_loss_val = self.power_loss_req.get_value(PIN_POWER_LOSS)
            data["power_loss"] = (power_loss_val != Value.INACTIVE)
        except Exception as err:
            _LOGGER.error("GPIO read failed: %s", err)
            data["power_loss"] = None

        # --- I2C ---
        try:
            raw_v = self.bus.read_word_data(I2C_ADDR, REG_VOLTAGE)
            raw_v = ((raw_v >> 8) | (raw_v << 8)) & 0xFFFF
            #data["voltage"] = round(raw_v * 1.25 / 1000, 2)
            data["voltage"] = raw_v


            raw_c = self.bus.read_word_data(I2C_ADDR, REG_CAPACITY)
            raw_c = ((raw_c >> 8) | (raw_c << 8)) & 0xFFFF
            data["capacity"] = round(raw_c / 256, 1)
        except OSError as err:
            _LOGGER.warning("I2C read failed: %s", err)
            data["voltage"] = None
            data["capacity"] = None

        return data

    async def shutdown_host(self):
        await hass.services.async_call(
            "homeassistant",
            "shutdown",
            blocking=True,
    )
