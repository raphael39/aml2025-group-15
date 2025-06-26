# Electricity Price Forecasting using Weather and Consumption Data

This repository contains utilities for working with electricity price data in the Netherlands. The project aims to forecast hourly prices using historical prices, demand and weather information.

## ENTSO-E API Client

`entsoe_client.py` implements a small client for the [ENTSO-E Transparency Platform](https://transparency.entsoe.eu/). It allows downloading historical day-ahead (spot) prices and the realised generation mix for the Netherlands.

### Usage

```python
from datetime import datetime
from entsoe_client import EntsoeClient

client = EntsoeClient("<YOUR_ENTSOE_TOKEN>")
start = datetime(2024, 1, 1)
end = datetime(2024, 1, 2)

prices = client.get_spot_prices(start, end)
mix = client.get_generation_mix(start, end)
```

Both methods return dictionaries keyed by `datetime`.
