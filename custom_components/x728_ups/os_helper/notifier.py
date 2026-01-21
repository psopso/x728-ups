from homeassistant.components.persistent_notification import create

def notify_restart_required(hass):
    create(
        hass,
        title="X728 UPS",
        message=(
            "OS-level GPIO handler installed.\n\n"
            "A full Home Assistant OS restart is required."
        ),
        notification_id="x728_os_restart",
    )
