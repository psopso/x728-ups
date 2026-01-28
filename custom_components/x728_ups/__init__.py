from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .coordinator import X728Coordinator
import logging

_LOGGER = logging.getLogger(__name__)
PLATFORMS = ["sensor", "binary_sensor"]

_LOGGER.info("Startuji X728 UPS Integration")

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """YAML setup (nepovinné)."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Setup z config entry."""
    _LOGGER.debug("X728: async_setup_entry start")
    coordinator = X728Coordinator(hass)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault("x728_ups", {})[entry.entry_id] = coordinator

    _LOGGER.debug("X728: Forwarding platforms")
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    _LOGGER.debug("X728: async_setup_entry done")
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data["x728_ups"].pop(entry.entry_id)
    return unload_ok
