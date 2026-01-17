from homeassistant.core import HomeAssistant
from homeassistant.helpers import service
from .const import DOMAIN, PIN_SHUTDOWN, GPIO_CHIP
import gpiod
import asyncio

import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict):
    async def shutdown_host(call):
        chip = gpiod.Chip(GPIO_CHIP)
        line = chip.get_line(PIN_SHUTDOWN)
        line.request(
            consumer="x728",
            type=gpiod.LINE_REQ_DIR_OUT
        )
        line.set_value(1)
        await asyncio.sleep(2)
        line.set_value(0)
        line.release()

    hass.services.async_register(
        DOMAIN,
        "shutdown_host",
        shutdown_host
    )

    return True
