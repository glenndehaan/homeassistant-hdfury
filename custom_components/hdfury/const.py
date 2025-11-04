"""Constants for HDFury Integration."""

DOMAIN = "hdfury"
PLATFORMS = ["button", "select", "sensor", "switch"]

CONF_HOST = "host"

SELECT_MAP = {
    "portseltx0": "Port Selector TX0",
    "portseltx1": "Port Selector TX1",
}

SENSOR_MAP = {
    "RX0": ("Input RX0", "diagnostic"),
    "RX1": ("Input RX1", "diagnostic"),
    "TX0": ("Output TX0", "diagnostic"),
    "TX1": ("Output TX1", "diagnostic"),
    "AUD0": ("Audio TX0", "diagnostic"),
    "AUD1": ("Audio TX1", "diagnostic"),
    "AUDOUT": ("Audio Output", "diagnostic"),
    "SINK0": ("EDID TX0", "diagnostic"),
    "EDIDA0": ("EDID TXA0", "diagnostic"),
    "SINK1": ("EDID TX1", "diagnostic"),
    "EDIDA1": ("EDID TXA1", "diagnostic"),
    "SINK2": ("EDID AUD", "diagnostic"),
    "EDIDA2": ("EDID AUDA", "diagnostic"),
    "EARCRX": ("eARC/ARC Status", "diagnostic"),
}

SWITCH_MAP = {
    "autosw": ("Auto Switch Inputs", "autosw", "configuration"),
    "htpcmode0": ("HTPC Mode RX0", "htpcmode0", "configuration"),
    "htpcmode1": ("HTPC Mode RX1", "htpcmode1", "configuration"),
    "htpcmode2": ("HTPC Mode RX2", "htpcmode2", "configuration"),
    "htpcmode3": ("HTPC Mode RX3", "htpcmode3", "configuration"),
    "mutetx0": ("Mute TX0 Audio", "mutetx0audio", "configuration"),
    "mutetx1": ("Mute TX1 Audio", "mutetx1audio", "configuration"),
    "oled": ("OLED Display", "oled", "configuration"),
    "iractive": ("Infrared", "iractive", "configuration"),
    "relay": ("Relay", "relay", "configuration"),
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
