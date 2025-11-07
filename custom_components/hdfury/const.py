"""Constants for HDFury Integration."""

DOMAIN = "hdfury"

SELECT_PORT_LIST = [
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
    "autosw": lambda client, value: client.set_auto_switch_inputs(value),
    "htpcmode0": lambda client, value: client.set_htpc_mode_rx0(value),
    "htpcmode1": lambda client, value: client.set_htpc_mode_rx1(value),
    "htpcmode2": lambda client, value: client.set_htpc_mode_rx2(value),
    "htpcmode3": lambda client, value: client.set_htpc_mode_rx3(value),
    "mutetx0": lambda client, value: client.set_mute_tx0_audio(value),
    "mutetx1": lambda client, value: client.set_mute_tx1_audio(value),
    "oled": lambda client, value: client.set_oled(value),
    "iractive": lambda client, value: client.set_ir_active(value),
    "relay": lambda client, value: client.set_relay(value),
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
