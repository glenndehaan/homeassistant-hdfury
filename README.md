# HDFury Integration for Home Assistant

This custom integration allows Home Assistant to monitor and control compatible [HDFury](https://www.hdfury.com/) devices such as Diva, Vertex2, and VRROOM over the local network.

## Features

* Setup via config flow (no YAML required)
* Select HDMI input ports via UI
* Customize input labels through the UI
* Reboot the HDFury device from Home Assistant
* Monitor device status (inputs, outputs, audio, EDID, eARC)
* Diagnostic information available in the entity state

## Supported Devices

Tested with the following HDFury devices:

* VRROOM
* Diva

## Installation

### HACS (Recommended)

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=glenndehaan&repository=homeassistant-hdfury)

1. Ensure HACS is installed. If not, follow the [HACS installation guide](https://hacs.xyz/docs/use/download/download/).
2. Go to **HACS → Integrations**
3. Search for "HDFury" and install the integration.
4. Restart Home Assistant
5. Go to **Settings → Devices & Services** and add **HDFury**

### Manual

1. Clone this repository or download it as a ZIP.
2. Copy the `custom_components/hdfury` folder to your Home Assistant configuration at `/config/custom_components/hdfury`.
3. Restart Home Assistant.
4. Add HDFury via the UI (Settings → Devices & Services).

## Configuration

This integration uses a **UI config flow** — no YAML setup is needed.
Just enter the IP address of your HDFury device when prompted.

### Custom Input Labels

You can personalize the labels for HDMI inputs shown in Home Assistant.

To do this:
1. Go to **Settings → Devices & Services**
2. Click your **HDFury device**
3. Click the **Configure** button
4. Enter custom names for the HDMI inputs (e.g., "Apple TV", "PS5", etc.)

These labels will be reflected in the HDMI input select entity.

### Entity Overview

This integration will expose:

* **Sensors**: HDMI port state, audio output status, EDID info
* **Selects**: Input selection for HDMI TX ports (with custom labels)
* **Buttons**: Reboot device, Issue Hotplug
* **Switches**: Auto Switch Input, HTPC Modes, Audio Mutes, OLED Display, Infrared and Relay.

Each device is identified using its serial number and MAC address to ensure uniqueness across multiple HDFury units.

## Troubleshooting

* Ensure the HDFury device is on the same local network and its API is accessible.
* Validate access to `http://<device_ip>/ssi/infopage.ssi` from a browser.
* Enable debug logging for troubleshooting:

```yaml
logger:
  default: info
  logs:
    custom_components.hdfury: debug
```

## Contributions

Issues and pull requests are welcome. Please open an issue to report bugs or request features.

## Screenshots

### Device Overview

![Device Overview](screenshots/device_overview.png)

### Options

![Options](screenshots/options.png)

## License

MIT
