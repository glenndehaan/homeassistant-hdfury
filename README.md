# HDFury Integration for Home Assistant

This custom integration allows Home Assistant to monitor and control compatible [HDFury](https://www.hdfury.com/) devices such as Diva, Vertex2, and VRROOM over the local network.

## Features

* Setup via config flow (no YAML required)
* Select HDMI input ports via UI
* Reboot the HDFury device from Home Assistant
* Monitor device status (inputs, outputs, audio, EDID, eARC)
* Diagnostic information available in the entity state

## Supported Devices

Tested with the following HDFury devices:

* VRROOM

## Installation

### HACS (Recommended)

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

### Entity Overview

This integration will expose:

* **Sensors**: HDMI port state, audio output status, EDID info
* **Selects**: Input selection for HDMI TX ports
* **Buttons**: Reboot device

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

## License

MIT
