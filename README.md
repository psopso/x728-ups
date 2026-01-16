# Suptronics X728 UPS Integration for Home Assistant

This custom component provides native support for the **Suptronics X728 UPS"** (Uninterruptible Power Supply) expansion board. It allows Home Assistant to monitor battery health and manage safe shutdowns during power outages.

## Usage

### What you need

* **Raspberry Pi** (3B+/4/5) with Home Assistant OS.
* **Suptronics X728 Board** (Compatible with versions 1.2, 1.3, 2.0, 2.1, 2.3, 2.5).
* **I2C enabled** on your Home Assistant OS host.


### GPIO & I2C Pinout

Function | Pin (v1.2 - v1.3) | Pin (v2.0 - v2.5) | Note
---------|------------------|-------------------|-----
**I2C SDA** | GPIO 2 | GPIO 2 | Data
**I2C SCL** | GPIO 3 | GPIO 3 | Clock
**AC Power Loss** | GPIO 6 | GPIO 6 | High = AC OK
**Low Battery** | GPIO 26 | GPIO 26 | High = Low Bat
**Shutdown Signal** | GPIO 18 | GPIO 5 | Button/Signal
**Full Power Off** | GPIO 13 | GPIO 12 | Hardware Cut-off

## Installation

### 1. Enabling I2C in HAOS

I2C is disabled by default in Home Assistant OS. To enable it:
1. Install **Advanced SSH & Web Terminal** add-on.
2. Disable **Protection Mode** in the add-on settings.
3. Run the following command in the terminal:
   ``bash
   curl -OSL https://github.com/adamoutler/HassOSConfigurator/raw/main/enable_i2c.sh
   chmod +x enable_i2c.sh
   ./enable_i2c.sh
   ``\
4. **Reboot your host twice.**

### 2. Manual Installation
1. Create a directory `custom_components/x728_ups/`  in your HA config folder.
2. Copy all files (`__init__.py`, `sensor.py`, `binary_sensor.py`, `manifest.json`) into that folder.
3. Restart Home Assistant.


## Configuration

Add the following to your `configuration.yaml`:

```yaml
# X728 UPS Sensors (Voltage and Percentage)
sensor:
  - platform: x728_ups

# X728 UPS Status (AC Power and Low Battery)
binary_sensor:
  - platform: x728_ups
```J

## Automations

### Recommended Safe Shutdown

This automation ensures that Home Assistant shuts down gracefully when the battery voltage reaches a critical level (3.0V - 3.1V), preventing database and SD card corruption.

```yaml
alias: "System: UPS Safe Shutdown"
trigger:
  - platform: numeric_state
    entity_id: sensor.x728_battery_voltage
    below: 3.1
condition:
  - condition: state
    entity_id: binary_sensor.x728_ac_power_status
    state: "off"
action:
  - service: notify.persistent_notification
    data:
      title: "UPS Alert"
      message: "Battery critical! Initiating safe shutdown."
  - service: hassio.host_shutdown
```J

## Troubleshooting

* **No sensors appearing**: Check your Home Assistant logs for `ModuleNotFoundError: No module named 'smbus2' `.
* **I2C errors**: Verify I2C is active by running `ls /dev/i2c*` in the terminal. You should see `/dev/i2c-1`.
* **Incorrect Voltage**: Ensure no other HAT is conflicting with the I2C pins (GPIO 2 & 3).
