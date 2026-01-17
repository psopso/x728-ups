from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .coordinator import X728Coordinator

PLATFORMS = ["sensor", "binary_sensor", "button"]


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up integration via YAML (optional)."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up x728 UPS from a config entry."""
    coordinator = X728Coordinator(hass)

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault("x728_ups", {})
    hass.data["x728_ups"][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(
        entry, PLATFORMS
    )
    if unload_ok:
        hass.data["x728_ups"].pop(entry.entry_id)

    return unload_ok
