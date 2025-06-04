DOMAIN = "hdfury"
PLATFORMS = ["button", "select", "sensor"]

CONF_HOST = "host"

SELECT_MAP = {
    "portseltx0": ("Port Selector TX0", "mdi:hdmi-port"),
    "portseltx1": ("Port Selector TX1", "mdi:hdmi-port"),
}

SENSOR_MAP = {
    "RX0": ("Input RX0", "mdi:video-input-hdmi", "diagnostic"),
    "RX1": ("Input RX1", "mdi:video-input-hdmi", "diagnostic"),
    "TX0": ("Output TX0", "mdi:cable-data", "diagnostic"),
    "TX1": ("Output TX1", "mdi:cable-data", "diagnostic"),
    "AUD0": ("Audio TX0", "mdi:audio-input-rca", "diagnostic"),
    "AUD1": ("Audio TX1", "mdi:audio-input-rca", "diagnostic"),
    "AUDOUT": ("Audio Output", "mdi:television-speaker", "diagnostic"),
    "SINK0": ("EDID TX0", "mdi:television", "diagnostic"),
    "EDIDA0": ("EDID TXA0", "mdi:format-list-text", "diagnostic"),
    "SINK1": ("EDID TX1", "mdi:television", "diagnostic"),
    "EDIDA1": ("EDID TXA1", "mdi:format-list-text", "diagnostic"),
    "SINK2": ("EDID AUD", "mdi:audio-video", "diagnostic"),
    "EDIDA2": ("EDID AUDA", "mdi:format-list-text", "diagnostic"),
    "EARCRX": ("eARC/ARC Status", "mdi:audio-video", "diagnostic"),
}

INPUT_OPTIONS = {
    "0": "Input 0",
    "1": "Input 1",
    "2": "Input 2",
    "3": "Input 3",
    "4": "Copy TX"
}

INPUT_LABELS = {
    "Input 0": "Input 0",
    "Input 1": "Input 1",
    "Input 2": "Input 2",
    "Input 3": "Input 3"
}
