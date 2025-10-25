DOMAIN = "hdfury"
PLATFORMS = ["button", "select", "sensor", "switch"]

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

SWITCH_MAP = {
    "autosw": ("Auto Switch Inputs", "autosw", "mdi:import", "configuration"),
    "htpcmode0": ("HTPC Mode RX0", "htpcmode0", "mdi:desktop-classic", "configuration"),
    "htpcmode1": ("HTPC Mode RX1", "htpcmode1", "mdi:desktop-classic", "configuration"),
    "htpcmode2": ("HTPC Mode RX2", "htpcmode2", "mdi:desktop-classic", "configuration"),
    "htpcmode3": ("HTPC Mode RX3", "htpcmode3", "mdi:desktop-classic", "configuration"),
    "mutetx0": ("Mute TX0 Audio", "mutetx0audio", "mdi:volume-mute", "configuration"),
    "mutetx1": ("Mute TX1 Audio", "mutetx1audio", "mdi:volume-mute", "configuration"),
    "oled": ("OLED Display", "oled", "mdi:cellphone-information", "configuration"),
    "iractive": ("Infrared", "iractive", "mdi:remote", "configuration"),
    "relay": ("Relay", "relay", "mdi:electric-switch", "configuration"),
}

INPUT_OPTIONS = {
    "0": "Input 0",
    "1": "Input 1",
    "2": "Input 2",
    "3": "Input 3",
    "4": "Copy TX"
}

OPMODE_OPTIONS = {
    "0": "Mode 0 - Splitter TX0/TX1 FRL5 VRR",
    "1": "Mode 1 - Splitter TX0/TX1 UPSCALE FRL5",
    "2": "Mode 2 - Matrix TMDS",
    "3": "Mode 3 - Matrix FRL->TMDS",
    "4": "Mode 4 - Matrix DOWNSCALE",
    "5": "Mode 5 - Matrix RX0:FRL5 + RX1-3:TMDS",
}

INPUT_LABELS = {
    "Input 0": "Input 0",
    "Input 1": "Input 1",
    "Input 2": "Input 2",
    "Input 3": "Input 3"
}
