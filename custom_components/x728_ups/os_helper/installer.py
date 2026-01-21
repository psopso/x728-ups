import subprocess
from pathlib import Path

def install():
    subprocess.run(
        ["cp", "/config/custom_components/x728_ups/os_helper/x728-gpio-handler.sh",
         "/usr/local/bin/x728-gpio-handler.sh"],
        check=True
    )
    subprocess.run(["chmod", "+x", "/usr/local/bin/x728-gpio-handler.sh"], check=True)

    subprocess.run(
        ["cp",
         "/config/custom_components/x728_ups/os_helper/x728-gpio-handler.service",
         "/etc/systemd/system/"],
        check=True
    )

    subprocess.run(["systemctl", "daemon-reexec"], check=True)
    subprocess.run(["systemctl", "enable", "x728-gpio-handler"], check=True)
