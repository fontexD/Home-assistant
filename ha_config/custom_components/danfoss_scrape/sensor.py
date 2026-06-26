from __future__ import annotations

from datetime import timedelta
import logging
import re
import time
import urllib.parse
import urllib.request

import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA, SensorEntity
from homeassistant.const import (
    CONF_HOST,
    CONF_NAME,
    CONF_PASSWORD,
    CONF_SCAN_INTERVAL,
    CONF_USERNAME,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = "Danfoss Session Data"
DEFAULT_SCAN_INTERVAL = timedelta(seconds=60)
REQUEST_TIMEOUT = 35
MAX_ATTEMPTS = 3
RETRY_DELAY_SECONDS = 2

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
        vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): cv.time_period,
    }
)


def _parse_number(value: str | None) -> float | None:
    text = (value or "").strip()
    if not text:
        return None

    if "," in text and "." in text:
        if text.rfind(",") > text.rfind("."):
            text = text.replace(".", "").replace(",", ".")
        else:
            text = text.replace(",", "")
    elif "," in text:
        text = text.replace(",", ".")

    try:
        return float(text)
    except ValueError:
        return None


def _request_text(opener: urllib.request.OpenerDirector, url: str, data: bytes | None = None) -> str:
    last_exc: Exception | None = None

    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            return opener.open(url, data=data, timeout=REQUEST_TIMEOUT).read().decode("utf-8", "ignore")
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
            if attempt < MAX_ATTEMPTS:
                time.sleep(RETRY_DELAY_SECONDS * attempt)

    if last_exc is not None:
        raise last_exc

    return ""


def _extract_values(overview: str) -> tuple[float | None, float | None]:
    current_kw: float | None = None
    today_kwh: float | None = None

    cp_match = re.search(
        r"id=[\"']curr_power[\"'][^>]*>\s*([0-9][0-9\.,]*)\s*([kKmMwW]{1,2})?",
        overview,
    )
    pt_match = re.search(
        r"id=[\"']prod_today[\"'][^>]*>\s*([0-9][0-9\.,]*)\s*kWh",
        overview,
        re.IGNORECASE,
    )

    if cp_match:
        current_value = _parse_number(cp_match.group(1))
        unit = (cp_match.group(2) or "kW").lower()
        if current_value is not None:
            if unit == "w":
                current_value = current_value / 1000.0
            current_kw = round(current_value, 3)

    if pt_match:
        today_value = _parse_number(pt_match.group(1))
        if today_value is not None:
            today_kwh = round(today_value, 3)

    return current_kw, today_kwh


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    async_add_entities(
        [
            DanfossSessionSensor(
                host=config[CONF_HOST],
                username=config[CONF_USERNAME],
                password=config[CONF_PASSWORD],
                name=config[CONF_NAME],
                scan_interval=config[CONF_SCAN_INTERVAL],
            )
        ],
        True,
    )


class DanfossSessionSensor(SensorEntity):
    _attr_should_poll = True

    def __init__(
        self,
        host: str,
        username: str,
        password: str,
        name: str,
        scan_interval: timedelta,
    ) -> None:
        self._host = host
        self._username = username
        self._password = password
        self._scan_interval = scan_interval
        self._sid = ""

        self._attr_name = name
        self._attr_unique_id = "danfoss_session_data"
        self._attr_native_value = None
        self._attr_extra_state_attributes = {
            "current_kw": None,
            "today_kwh": None,
            "sid": "",
            "error": "",
        }

    @property
    def scan_interval(self) -> timedelta:
        return self._scan_interval

    async def async_update(self) -> None:
        data = await self.hass.async_add_executor_job(self._fetch_data)

        self._attr_native_value = data["current_kw"]
        self._attr_extra_state_attributes = {
            "current_kw": data["current_kw"],
            "today_kwh": data["today_kwh"],
            "sid": data["sid"],
            "error": data["error"],
        }

    def _fetch_data(self) -> dict:
        out = {
            "current_kw": self._attr_extra_state_attributes.get("current_kw"),
            "today_kwh": self._attr_extra_state_attributes.get("today_kwh"),
            "sid": self._sid,
            "error": "",
        }

        base = f"http://{self._host}"

        try:
            opener = urllib.request.build_opener()

            if self._sid:
                try:
                    overview = _request_text(opener, f"{base}/cgi-bin/overview.tcl?sid={self._sid}")
                    current_kw, today_kwh = _extract_values(overview)
                    if current_kw is not None or today_kwh is not None:
                        if current_kw is not None:
                            out["current_kw"] = current_kw
                        if today_kwh is not None:
                            out["today_kwh"] = today_kwh
                        out["sid"] = self._sid
                        return out
                except Exception:  # noqa: BLE001
                    # Cached sid likely expired; continue with login flow.
                    pass

            def _login(force_release: bool) -> str:
                if force_release:
                    _request_text(opener, f"{base}/cgi-bin/closed_for_now.tcl?useTheForce=1")

                payload = urllib.parse.urlencode(
                    {"user": self._username, "pw": self._password, "sid": ""}
                ).encode()
                login_html = _request_text(opener, f"{base}/cgi-bin/handle_login.tcl", data=payload)
                sid_match = re.search(r"sid=([0-9]+)", login_html)
                return sid_match.group(1) if sid_match else ""

            sid = _login(force_release=False)
            if not sid:
                sid = _login(force_release=True)

            self._sid = sid
            out["sid"] = sid
            if not sid:
                out["error"] = "no_sid"
                return out

            overview = _request_text(opener, f"{base}/cgi-bin/overview.tcl?sid={sid}")
            current_kw, today_kwh = _extract_values(overview)

            if current_kw is not None:
                out["current_kw"] = current_kw

            if today_kwh is not None:
                out["today_kwh"] = today_kwh

            if out["current_kw"] is None and out["today_kwh"] is None:
                out["error"] = "parse_failed"

        except Exception as exc:  # noqa: BLE001
            out["error"] = f"{exc.__class__.__name__}: {exc}"[:180]
            _LOGGER.warning("Danfoss scrape failed: %s", out["error"])

        return out
