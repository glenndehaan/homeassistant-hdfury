"""Helpers for HDFury Integration."""

import asyncio
import json
import logging

from aiohttp import ClientError

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

_LOGGER = logging.getLogger(__name__)


async def fetch_json(hass: HomeAssistant, url: str):
    """Fetch JSON data from an HDFury device."""

    _LOGGER.debug("HTTP Request: %s", url)
    session = async_get_clientsession(hass)

    try:
        async with session.get(url, timeout=10) as resp:
            if resp.status != 200:
                _LOGGER.error("Non-200 response from %s: %s", url, resp.status)
                return {}

            text = await resp.text()
            _LOGGER.debug("HTTP Body from %s: %s", url, text)

            try:
                return json.loads(text)
            except json.JSONDecodeError as err:
                _LOGGER.error("Invalid JSON from %s: %s", url, err)
                return {}

    except asyncio.TimeoutError:
        _LOGGER.warning("Timeout while fetching %s", url)
    except ClientError as err:
        _LOGGER.warning("Client error while fetching %s: %s", url, err)
    except Exception as err:
        _LOGGER.exception("Unexpected error fetching %s: %s", url, err)

    return {}


def get_base_url(host: str):
    """Return HDFury Device Base URL."""

    return f"http://{host}"


def get_brd_url(host: str):
    """Return HDFury Device Board URL."""

    return f"{get_base_url(host)}/ssi/brdinfo.ssi"


def get_conf_url(host: str):
    """Return HDFury Device Configuration URL."""

    return f"{get_base_url(host)}/ssi/confpage.ssi"


def get_info_url(host: str):
    """Return HDFury Device Info URL."""

    return f"{get_base_url(host)}/ssi/infopage.ssi"


def get_cmd_url(host: str, cmd: str, option: str = ""):
    """Return HDFury Command URL."""

    return f"{get_base_url(host)}/cmd?{cmd}={option}"
