\# Functionality Overview



This document describes how the \*\*Suptronics X728 UPS Home Assistant integration\*\*

works internally, what data it uses, and how it behaves in different scenarios.



The integration is intentionally designed to separate \*\*critical control logic\*\*

from \*\*diagnostic functionality\*\*, ensuring reliability even in degraded states.



---



\## Architecture Overview



The integration communicates with the X728 UPS board using two independent

interfaces:



\- \*\*GPIO\*\* – critical control and power state signals

\- \*\*I2C\*\* – battery diagnostics (voltage and capacity)



These subsystems are handled independently so that failure of I2C does not

prevent safe system operation.



---



\## GPIO – Power Control and State Detection



GPIO is considered \*\*mandatory and always active\*\*.



\### Power Loss Detection



The X728 board signals loss of external power using a GPIO input:



\- \*\*GPIO pin:\*\* 6

\- \*\*Direction:\*\* Input

\- \*\*Logic level interpretation:\*\*

&nbsp; - ACTIVE → External power present

&nbsp; - INACTIVE → Running on battery



This state is exposed in Home Assistant as:



\- \*\*Binary Sensor: `X728 Power Loss`\*\*

&nbsp; - `ON` → External power lost

&nbsp; - `OFF` → External power present



This binary sensor can be used for:

\- Automations

\- Notifications

\- Conditional logic (e.g. delayed shutdown)



---



\### Host Shutdown Trigger



The X728 board supports host shutdown using a short GPIO pulse:



\- \*\*GPIO pin:\*\* 26

\- \*\*Direction:\*\* Output

\- \*\*Pulse length:\*\* approximately 2 seconds



The integration exposes this as:



\- \*\*Button entity:\*\* `X728 Shutdown Host`

\- \*\*Service:\*\* `x728\_ups.shutdown\_host`



When triggered:

1\. GPIO output is set ACTIVE

2\. Pulse is held for ~2 seconds

3\. GPIO output is set INACTIVE

4\. X728 initiates host shutdown



⚠️ The integration does \*\*not\*\* shut down the operating system directly.

It only signals the X728 board, which then handles the shutdown process.



---



\## I2C – Battery Diagnostics



I2C is used only for \*\*battery monitoring\*\* and is optional.



\- \*\*Bus:\*\* I2C-1

\- \*\*Device address:\*\* `0x36`



\### Battery Voltage



\- \*\*Register:\*\* `0x02`

\- Converted to volts

\- Exposed as:

&nbsp; - \*\*Sensor:\*\* `X728 Battery Voltage`



\### Battery Capacity



\- \*\*Register:\*\* `0x04`

\- Converted to percentage

\- Exposed as:

&nbsp; - \*\*Sensor:\*\* `X728 Battery Capacity`



---



\### Behavior When I2C Fails



If I2C communication fails due to:

\- Disabled I2C

\- Missing battery

\- Hardware error

\- Bus conflict



Then:

\- Voltage and capacity sensors return `None`

\- No exception propagates to Home Assistant

\- GPIO functionality remains fully operational



This ensures that:

\- Power loss detection continues to work

\- Shutdown functionality remains available

\- The integration remains stable



---



\## Data Update Model



The integration uses Home Assistant’s `DataUpdateCoordinator`:



\- \*\*Update interval:\*\* 10 seconds

\- Single centralized data refresh

\- All entities read from the same data snapshot



Benefits:

\- No duplicate GPIO or I2C reads

\- Consistent state across entities

\- Minimal system load



---



\## Design Rationale



| Aspect | Design Choice |

|------|--------------|

| GPIO | Always available, critical |

| I2C | Optional, diagnostic only |

| Failure handling | Graceful degradation |

| Shutdown | Hardware-triggered |

| Updates | Centralized coordinator |



---



\## Summary



\- GPIO ensures reliable power state detection and shutdown signaling

\- I2C provides battery diagnostics without affecting core functionality

\- The integration remains operational even with partial hardware failure

\- Designed for stability and predictable behavior



This makes the integration suitable for unattended systems and long-term use.



