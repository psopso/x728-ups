from pathlib import Path

SERVICE_FILE = Path("/etc/systemd/system/x728-gpio-handler.service")

def is_installed() -> bool:
    return SERVICE_FILE.exists()
