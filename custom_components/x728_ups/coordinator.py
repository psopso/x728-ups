from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.core import HomeAssistant
import gpiod
from gpiod.line import Direction, Value
from smbus2 import SMBus
from .const import *

class X728Coordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant):
        super().__init__(
            hass,
            logger=None,
            name=DOMAIN,
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
        )

        # I2C
        self.bus = SMBus(I2C_BUS)

        # GPIO
        self.chip = gpiod.Chip(GPIO_CHIP)

        self.power_loss_req = self.chip.request_lines(
            consumer="x728_power",
            config={
                PIN_POWER_LOSS: gpiod.LineSettings(
                    direction=Direction.INPUT
                )
            }
        )

        self.shutdown_req = self.chip.request_lines(
            consumer="x728_shutdown",
            config={
                PIN_SHUTDOWN: gpiod.LineSettings(
                    direction=Direction.OUTPUT,
                    output_value=Value.INACTIVE,
                )
            }
        )

    async def _async_update_data(self):
        # GPIO
        power_loss_val = self.power_loss_req.get_value(PIN_POWER_LOSS)
        power_loss = (power_loss_val == Value.INACTIVE)

        # I2C voltage
        raw_v = self.bus.read_word_data(I2C_ADDR, REG_VOLTAGE)
        raw_v = ((raw_v >> 8) | (raw_v << 8)) & 0xFFFF
        voltage = round(raw_v * 1.25 / 1000, 2)

        # I2C capacity
        raw_c = self.bus.read_word_data(I2C_ADDR, REG_CAPACITY)
        raw_c = ((raw_c >> 8) | (raw_c << 8)) & 0xFFFF
        capacity = round(raw_c / 256, 1)

        return {
            "power_loss": power_loss,
            "voltage": voltage,
            "capacity": capacity,
        }

    async def shutdown_host(self):
        # pulz pro X728 (cca 2 s)
        self.shutdown_req.set_value(PIN_SHUTDOWN, Value.ACTIVE)
        await self.hass.async_add_executor_job(lambda: __import__("time").sleep(2))
        self.shutdown_req.set_value(PIN_SHUTDOWN, Value.INACTIVE)
