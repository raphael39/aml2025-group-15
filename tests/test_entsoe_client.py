import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from datetime import datetime
import xml.etree.ElementTree as ET
from entsoe_client import EntsoeClient


def test_parse_spot_prices():
    xml_content = """
    <Publication_MarketDocument>
      <TimeSeries>
        <Period>
          <timeInterval>
            <start>2024-01-01T00:00Z</start>
            <end>2024-01-01T02:00Z</end>
          </timeInterval>
          <resolution>PT60M</resolution>
          <Point>
            <position>1</position>
            <price.amount>100</price.amount>
          </Point>
          <Point>
            <position>2</position>
            <price.amount>110</price.amount>
          </Point>
        </Period>
      </TimeSeries>
    </Publication_MarketDocument>
    """
    root = ET.fromstring(xml_content)
    client = EntsoeClient("token")
    prices = client._parse_spot_prices(root)
    assert prices[datetime(2024, 1, 1, 0)] == 100.0
    assert prices[datetime(2024, 1, 1, 1)] == 110.0


def test_parse_generation_mix():
    xml_content = """
    <Publication_MarketDocument>
      <TimeSeries>
        <MktPSRType>
          <psrType>B16</psrType>
        </MktPSRType>
        <Period>
          <timeInterval>
            <start>2024-01-01T00:00Z</start>
            <end>2024-01-01T02:00Z</end>
          </timeInterval>
          <resolution>PT60M</resolution>
          <Point>
            <position>1</position>
            <quantity>50</quantity>
          </Point>
          <Point>
            <position>2</position>
            <quantity>60</quantity>
          </Point>
        </Period>
      </TimeSeries>
    </Publication_MarketDocument>
    """
    root = ET.fromstring(xml_content)
    client = EntsoeClient("token")
    mix = client._parse_generation_mix(root)
    assert mix["B16"][datetime(2024, 1, 1, 0)] == 50.0
    assert mix["B16"][datetime(2024, 1, 1, 1)] == 60.0
