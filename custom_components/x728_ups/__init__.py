from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .coordinator import X728Coordinator

import logging
_LOGGER = logging.getLogger(__name__)
#_LOGGER.info("Pokus")

PLATFORMS = ["sensor", "binary_sensor", "button"]

_LOGGER.info("Startuji X728Coordinator")

#async def async_setup(hass: HomeAssistant, config: dict) -> bool:
#    """Set up integration via YAML (optional)."""
#    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up x728 UPS from a config entry."""
    _LOGGER.info("Debug1")
    coordinator = X728Coordinator(hass)
    _LOGGER.info("Debug2")
    await coordinator.async_config_entry_first_refresh()
    _LOGGER.info("Debug3")
    hass.data.setdefault("x728_ups", {})
    _LOGGER.info("Debug4")
    hass.data["x728_ups"][entry.entry_id] = coordinator

    _LOGGER.info("Pred forward")
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    _LOGGER.info("Po forward")
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(
        entry, PLATFORMS
    )
    if unload_ok:
        hass.data["x728_ups"].pop(entry.entry_id)

    return unload_ok
