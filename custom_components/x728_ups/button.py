from homeassistant.components.button import ButtonEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([X728ShutdownButton(coordinator, entry.entry_id), X728InstallOsHandlerButton(coordinator, entry.entry_id)])

class X728ShutdownButton(CoordinatorEntity, ButtonEntity):
    _attr_name = "X728 Shutdown Host"
    _attr_icon = "mdi:power"

    def __init__(self, coordinator, entry_id):
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry_id}_shutdown"

    async def async_press(self):
        await self.coordinator.shutdown_host()

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "x728_ups")},
            "name": "Suptronics X728 UPS",
        }

    @property
    def available(self):
        # dostupnost buttonu závisí na GPIO
        return self.coordinator.data.get("power_loss") is not None

class X728InstallOsHandlerButton(CoordinatorEntity, ButtonEntity):
    _attr_name = "Install X728 OS Button Handler"

    def __init__(self, coordinator, entry_id):
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry_id}_install"

    async def async_press(self):
        from .os_helper.installer import install
        from .os_helper.notifier import notify_restart_required

        await self.hass.async_add_executor_job(install)
        notify_restart_required(self.hass)

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "x728_ups")},
            "name": "Suptronics X728 UPS",
        }

