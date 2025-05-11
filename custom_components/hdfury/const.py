DOMAIN = "hdfury"
PLATFORMS = ["select", "sensor"]

CONF_HOST = "host"

SELECT_MAP = {
    "portseltx0": ("Port Selector TX0", "mdi:hdmi-port"),
}

SENSOR_MAP = {
    "portseltx0": ("Port Selector TX0", "mdi:hdmi-port"),
    "portseltx1": ("Port Selector TX1", "mdi:hdmi-port"),
    "RX0": ("Input RX0", "mdi:video-input-hdmi"),
    "RX1": ("Input RX1", "mdi:video-input-hdmi"),
    "TX0": ("Output TX0", "mdi:cable-data"),
    "TX1": ("Output TX1", "mdi:cable-data"),
    "AUD0": ("Audio TX0", "mdi:audio-input-rca"),
    "AUD1": ("Audio TX1", "mdi:audio-input-rca"),
    "AUDOUT": ("Audio Output", "mdi:television-speaker"),
    "SINK0": ("EDID TX0", "mdi:television"),
    "EDIDA0": ("EDID TXA0", "mdi:format-list-text"),
    "SINK1": ("EDID TX1", "mdi:television"),
    "EDIDA1": ("EDID TXA1", "mdi:format-list-text"),
    "SINK2": ("EDID AUD", "mdi:audio-video"),
    "EDIDA2": ("EDID AUDA", "mdi:format-list-text"),
    "EARCRX": ("eARC/ARC Status", "mdi:audio-video"),
}

DIAGNOSTIC_KEYS = {
    "RX0",
    "RX1",
    "TX0",
    "TX1",
    "AUD0",
    "AUD1",
    "AUDOUT",
    "SINK0",
    "SINK1",
    "SINK2",
    "EDIDA0",
    "EDIDA1",
    "EDIDA2",
    "EARCRX",
}
