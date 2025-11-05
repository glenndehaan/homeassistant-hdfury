"""Constants for HDFury Integration."""

DOMAIN = "hdfury"

SELECT_LIST = [
    "portseltx0",
    "portseltx1",
]

SENSOR_LIST = [
    "RX0",
    "RX1",
    "TX0",
    "TX1",
    "AUD0",
    "AUD1",
    "AUDOUT",
    "SINK0",
    "EDIDA0",
    "SINK1",
    "EDIDA1",
    "SINK2",
    "EDIDA2",
    "EARCRX",
]

SWITCH_MAP = {
    "autosw": "autosw",
    "htpcmode0": "htpcmode0",
    "htpcmode1": "htpcmode1",
    "htpcmode2": "htpcmode2",
    "htpcmode3": "htpcmode3",
    "mutetx0": "mutetx0audio",
    "mutetx1": "mutetx1audio",
    "oled": "oled",
    "iractive": "iractive",
    "relay": "relay",
}

INPUT_OPTIONS = {
    "0": "Input 0",
    "1": "Input 1",
    "2": "Input 2",
    "3": "Input 3",
    "4": "Copy TX",
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
    "Input 3": "Input 3",
}
