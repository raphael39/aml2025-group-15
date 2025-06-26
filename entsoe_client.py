import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from typing import Dict, Any


ENTSOE_BASE_URL = "https://web-api.tp.entsoe.eu/api"


class EntsoeClient:
    """Simple client for the ENTSO-E Transparency Platform."""

    def __init__(self, api_key: str, base_url: str = ENTSOE_BASE_URL) -> None:
        self.api_key = api_key
        self.base_url = base_url

    def _request(self, params: Dict[str, Any]) -> ET.Element:
        params = {**params, "securityToken": self.api_key}
        url = f"{self.base_url}?{urllib.parse.urlencode(params)}"
        with urllib.request.urlopen(url) as response:
            data = response.read()
        return ET.fromstring(data)

    def _parse_spot_prices(self, root: ET.Element) -> Dict[datetime, float]:
        """Parse spot (day-ahead) prices from the XML response."""
        prices: Dict[datetime, float] = {}
        for ts in root.findall(".//TimeSeries"):
            period = ts.find("Period")
            if period is None:
                continue
            ti = period.find("timeInterval")
            if ti is None:
                continue
            start_str = ti.findtext("start")
            if start_str is None:
                continue
            start = datetime.strptime(start_str, "%Y-%m-%dT%H:%MZ")
            for point in period.findall("Point"):
                pos_text = point.findtext("position")
                if pos_text is None:
                    continue
                pos = int(pos_text)
                price_el = point.find("price.amount") or point.find("priceAmount")
                if price_el is None:
                    # Fallback: first child after position
                    for child in point:
                        if child.tag != "position":
                            price_el = child
                            break
                if price_el is None or price_el.text is None:
                    continue
                price = float(price_el.text)
                ts_time = start + timedelta(hours=pos - 1)
                prices[ts_time] = price
        return prices

    def get_spot_prices(self, start: datetime, end: datetime, domain: str = "10YNL----------L") -> Dict[datetime, float]:
        """Retrieve day-ahead market (spot) prices for the given time range."""
        params = {
            "documentType": "A44",
            "in_Domain": domain,
            "out_Domain": domain,
            "periodStart": start.strftime("%Y%m%d%H%M"),
            "periodEnd": end.strftime("%Y%m%d%H%M"),
        }
        root = self._request(params)
        return self._parse_spot_prices(root)

    def _parse_generation_mix(self, root: ET.Element) -> Dict[str, Dict[datetime, float]]:
        mix: Dict[str, Dict[datetime, float]] = {}
        for ts in root.findall(".//TimeSeries"):
            psr_type = ts.findtext("MktPSRType/psrType")
            if psr_type is None:
                continue
            period = ts.find("Period")
            if period is None:
                continue
            ti = period.find("timeInterval")
            if ti is None:
                continue
            start_str = ti.findtext("start")
            if start_str is None:
                continue
            start = datetime.strptime(start_str, "%Y-%m-%dT%H:%MZ")
            for point in period.findall("Point"):
                pos_text = point.findtext("position")
                if pos_text is None:
                    continue
                pos = int(pos_text)
                qty_el = point.find("quantity")
                if qty_el is None:
                    for child in point:
                        if child.tag != "position":
                            qty_el = child
                            break
                if qty_el is None or qty_el.text is None:
                    continue
                qty = float(qty_el.text)
                ts_time = start + timedelta(hours=pos - 1)
                mix.setdefault(psr_type, {})[ts_time] = qty
        return mix

    def get_generation_mix(self, start: datetime, end: datetime, domain: str = "10YNL----------L") -> Dict[str, Dict[datetime, float]]:
        params = {
            "documentType": "A75",
            "processType": "A16",
            "in_Domain": domain,
            "periodStart": start.strftime("%Y%m%d%H%M"),
            "periodEnd": end.strftime("%Y%m%d%H%M"),
        }
        root = self._request(params)
        return self._parse_generation_mix(root)
