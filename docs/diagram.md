Tlačítko X728

┌───────────────┐

│   STISK       │

└───────┬───────┘

&nbsp;       │

&nbsp;       ▼

+-------------------------------+

| X728 kontroluje GPIO12 (BOOT) |

+-------------------------------+

&nbsp;       │

&nbsp;       ├── GPIO12 = 0

&nbsp;       │      │

&nbsp;       │      └─► NIC SE NEDĚJE

&nbsp;       │          GPIO5 = 0

&nbsp;       │

&nbsp;       └── GPIO12 = 1

&nbsp;              │

&nbsp;              ▼

&nbsp;     po uvolnění tlačítka

&nbsp;              │

&nbsp;              ▼

&nbsp;       krátký impuls na GPIO5

&nbsp;              │

&nbsp;              ▼

&nbsp;     Raspberry Pi vyhodnotí délku

&nbsp;       │              │

&nbsp;       │              └─ dlouhý impuls → shutdown

&nbsp;       └─ krátký impuls → reboot



