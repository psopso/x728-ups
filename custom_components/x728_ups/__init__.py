from homeassistant.core import HomeAssistant
from .const import DOMAIN
from .coordinator import X728Coordinator

PLATFORMS = ["sensor", "binary_sensor", "button"]

async def async_setup(hass: HomeAssistant, config: dict):
    coordinator = X728Coordinator(hass)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN]["coordinator"] = coordinator

    async def shutdown_service(call):
        await coordinator.shutdown_host()

    hass.services.async_register(
        DOMAIN,
        "shutdown_host",
        shutdown_service,
    )

    for platform in PLATFORMS:
        hass.async_create_task(
            hass.helpers.discovery.async_load_platform(
                platform, DOMAIN, {}, config
            )
        )

    return True
