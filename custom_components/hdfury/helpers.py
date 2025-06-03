import json
import logging

import aiohttp

_LOGGER = logging.getLogger(__name__)

async def fetch_json(url):
    """Fetch Helper for HDFury Device."""

    _LOGGER.debug("HTTP Request: %s", url)
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    text = await resp.text()
                    return json.loads(text)
                _LOGGER.error("Non-200 response: %s", resp.status)
    except Exception as e:
        _LOGGER.error("Error fetching %s: %s", url, e)
    return {}

def get_base_url(host):
    """Return HDFury Device Base URL."""

    return f"http://{host}"

def get_brd_url(host):
    """Return HDFury Device Board URL."""

    return f"{get_base_url(host)}/ssi/brdinfo.ssi"

def get_conf_url(host):
    """Return HDFury Device Configuration URL."""

    return f"{get_base_url(host)}/ssi/confpage.ssi"

def get_info_url(host):
    """Return HDFury Device Info URL."""

    return f"{get_base_url(host)}/ssi/infopage.ssi"

def get_cmd_insel_url(host, option):
    """Return HDFury Device Port Select URL."""

    return f"{get_base_url(host)}/cmd?insel={option}"

def get_cmd_rst_url(host):
    """Return HDFury Device Restart URL."""

    return f"{get_base_url(host)}/cmd?reboot="
