"""Live FX via Frankfurter API (cached). Amounts convert through USD."""

from __future__ import annotations

import time
from decimal import Decimal
from typing import Callable

import httpx

from app.config import settings

RatesMap = dict[str, Decimal]
FetchFn = Callable[[str], tuple[str, RatesMap]]

_cache: dict[str, tuple[float, str, RatesMap]] = {}


class FxError(Exception):
    pass


def _default_fetch(base: str) -> tuple[str, RatesMap]:
    url = f"{settings.fx_api_base.rstrip('/')}/latest"
    try:
        response = httpx.get(
            url,
            params={"from": base},
            timeout=settings.fx_timeout_seconds,
        )
        response.raise_for_status()
        payload = response.json()
    except httpx.HTTPError as exc:
        raise FxError(f"FX provider unavailable: {exc}") from exc

    rates_raw = payload.get("rates") or {}
    as_of = str(payload.get("date") or "")
    rates: RatesMap = {base.upper(): Decimal("1")}
    for code, value in rates_raw.items():
        rates[str(code).upper()] = Decimal(str(value))
    return as_of, rates


def get_rates_vs_base(
    base: str = "USD",
    *,
    fetch: FetchFn | None = None,
) -> tuple[str, RatesMap]:
    """
    Return (as_of_date, rates) where rates[C] = units of C per 1 unit of base.
    Cached in-process for fx_cache_seconds.
    """
    base = base.upper()
    now = time.time()
    cached = _cache.get(base)
    if cached and now - cached[0] < settings.fx_cache_seconds:
        return cached[1], cached[2]

    fetch_fn = fetch or _default_fetch
    as_of, rates = fetch_fn(base)
    _cache[base] = (now, as_of, rates)
    return as_of, rates


def clear_fx_cache() -> None:
    _cache.clear()


def convert_amount(
    amount: Decimal,
    from_currency: str,
    to_currency: str,
    rates_vs_usd: RatesMap,
) -> Decimal:
    """
    Convert using USD-cross rates.
    rates_vs_usd[C] = units of C per 1 USD.
    """
    from_c = from_currency.upper()
    to_c = to_currency.upper()
    if from_c == to_c:
        return amount.quantize(Decimal("0.01"))

    def to_usd(value: Decimal, code: str) -> Decimal:
        if code == "USD":
            return value
        rate = rates_vs_usd.get(code)
        if rate is None or rate == 0:
            raise FxError(f"Missing FX rate for {code}")
        return value / rate

    def from_usd(value_usd: Decimal, code: str) -> Decimal:
        if code == "USD":
            return value_usd
        rate = rates_vs_usd.get(code)
        if rate is None or rate == 0:
            raise FxError(f"Missing FX rate for {code}")
        return value_usd * rate

    usd = to_usd(amount, from_c)
    return from_usd(usd, to_c).quantize(Decimal("0.01"))
