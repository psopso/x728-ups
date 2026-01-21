# X728 Button and GPIO Behavior (Detailed Explanation)

## Summary
On the **Suptronics X728 UPS board**, the shutdown signal on **GPIO5 (pin 29)** is **not generated simply by pressing the button**.

GPIO5 becomes active **only if the X728 detects that the operating system on Raspberry Pi is running**.  
This information is provided via **GPIO12 (pin 32)**.

---

## GPIO Roles

### GPIO12 – BOOT Signal
- Direction: **output from Raspberry Pi**
- Logic HIGH (3.3 V) means:
  **"The operating system is running and ready."**
- If GPIO12 is NOT HIGH:
  - The X728 **ignores the button**
  - GPIO5 remains permanently LOW

### GPIO5 – SHUTDOWN Signal
- Direction: **output from X728**
- A **short pulse** is generated after the button is released
- The pulse is evaluated by software:
  - short pulse → reboot
  - long pulse → shutdown

---

## Manufacturer Script (Conceptual Overview)

Suptronics provides a reference script which:

1. Exports GPIO12
2. Sets GPIO12 to HIGH
3. Monitors GPIO5
4. Measures pulse duration
5. Executes:
   - reboot
   - or poweroff

Without this (or equivalent logic),
**GPIO5 will never generate a pulse.**

---

## Button Press Behavior

### Case A – GPIO12 = LOW (OS not running / not initialized)
- Button press:
  - no pulse generated
  - GPIO5 stays LOW
- Multimeter shows constant 0 V
- This behavior is **intentional and correct**

### Case B – GPIO12 = HIGH (OS running)
- Button press:
  - after release, a pulse appears on GPIO5
  - pulse width ≈ 200–600 ms
- Pulse is very short
- Multimeter usually does **not detect it**
- Oscilloscope or logic analyzer required

---

## Design Rationale

This mechanism prevents:
- false shutdown during boot
- unintended power-off if OS is frozen
- undefined GPIO behavior after power-up

X728 logic:
> "Do not trust the button until the OS confirms it is ready."

---

## Hardware Test Without OS

For raw hardware testing:

1. Connect:
   - GPIO12 → 3.3 V (pin 1)
2. Attach:
   - oscilloscope / logic analyzer to GPIO5
3. Press the button

➡️ A pulse will appear  
➡️ A multimeter will likely still miss it

---

## Implications for Home Assistant and Custom Integrations

- The integration **must actively drive GPIO12**
- Without this:
  - the X728 button appears non-functional
  - but the hardware is operating correctly
- GPIO5 is **pulse-based**, not a static state

---
