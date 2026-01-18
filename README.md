> [!IMPORTANT]
> **WORK IN PROGRESS / EXPERIMENTAL**
>
> This integration is currently under active development. It is **not finished** and may not work as expected.
> Published primarily for easier installation via HACS on my personal setup. Use at your own risk.

# Suptronics X728 UPS – Home Assistant Integration

Custom Home Assistant integration for the **Suptronics X728 UPS HAT**.
The integration provides battery monitoring via **I2C** and power / shutdown
control via **GPIO** using modern Home Assistant architecture
(`DataUpdateCoordinator`, config entries, UI setup).

---

## Features

- Battery voltage sensor
- Battery capacity sensor
- Power loss binary sensor
- Shutdown button for host system
- GPIO access via `gpiod`
- I2C access via `smbus2`
- Fully UI-configurable (config flow)
- Graceful handling of missing I2C (GPIO still works)

---

## Requirements

- Home Assistant OS / Supervised
- Raspberry Pi (or compatible SBC)
- Suptronics X728 UPS HAT
- Enabled I2C interface
- Linux GPIO character device (`/dev/gpiochip*`)

---

## Installation

### Manual installation

1. Copy the `x728_ups` directory into:

   ```
   /config/custom_components/x728_ups
   ```

2. Restart Home Assistant.

3. Go to:
   **Settings → Devices & Services → Add Integration**
   and select **Suptronics X728 UPS**.

---

## Configuration

No YAML configuration is required.

All setup is done through the Home Assistant UI using a config entry.
The integration will automatically create:

- Sensors
- Binary sensor
- Button
- Device entry

---

## Entities

### Sensors

- **X728 Battery Voltage** (V)
- **X728 Battery Capacity** (%)

### Binary Sensor

- **X728 Power Loss**
  - `on` = external power lost
  - `off` = external power present

### Button

- **X728 Shutdown Host**
  - Sends a shutdown pulse to the X728 board

---

## GPIO & I2C Details

### GPIO

- Power loss input pin
- Shutdown output pin

Accessed using the Linux GPIO character device:
```
/dev/gpiochip0
```

### I2C

- Battery monitoring via I2C
- Default bus: `1`
- Default address: `0x36`

If I2C communication fails, the integration will:
- Log a warning
- Continue operating GPIO-based entities

---

## Logging & Debugging

To enable debug logging, add the following to `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.x728_ups: debug
```

Restart Home Assistant after changing logging settings.

---

## Architecture

- Uses `DataUpdateCoordinator` for centralized polling
- All entities are implemented as `CoordinatorEntity`
- No polling in individual entities
- Clean unload / reload support

---

## Known Limitations

- Designed for Home Assistant OS / Supervised
- Requires access to `/dev/gpiochip*`
- Not tested on container-only installations

---

## License

MIT License

---

## Disclaimer

This integration is not affiliated with Suptronics.
Use at your own risk.
