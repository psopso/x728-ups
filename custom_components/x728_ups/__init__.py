import RPi.GPIO as GPIO
import time

DOMAIN = "x728_ups"

def setup(hass, config):
    def handle_full_shutdown(call):
        # Puls na GPIO13 řekne desce X728, aby se za chvíli úplně vypla
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(13, GPIO.OUT)
        GPIO.output(13, GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(13, GPIO.LOW)
        # Následně pošleme příkaz k vypnutí samotného hostitele
        hass.services.call("hassio", "host_shutdown")

    hass.services.register(DOMAIN, "safe_shutdown", handle_full_shutdown)
    return True
    