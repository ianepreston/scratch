import datetime as dt
import json
import logging
import os
import random
from typing import Dict, List
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import azure.functions as func


def get_pool_prices() -> List[Dict[str, str]]:
    """Get the last two day's pool prices from AESO."""
    logging.info("Attempting to retrieve pool price data.")
    aeso_api = os.getenv("AESOAPI")
    start_dt = f"{dt.date.today() - dt.timedelta(days=10)}"
    end_dt = f"{dt.date.today()}"
    header = {"X-API-Key": aeso_api}
    base_url = "https://api.aeso.ca/report/v1.1/price/poolPrice"
    parameters = {"startDate": start_dt, "endDate": end_dt}
    query_string = urlencode(parameters)
    full_url = f"{base_url}?{query_string}"
    request = Request(url=full_url, headers=header)
    stdresult = urlopen(request)
    raw_data = stdresult.read()
    encoding = stdresult.info().get_content_charset("utf8")
    result_dict = json.loads(raw_data.decode(encoding))["return"]["Pool Price Report"]
    logging.info(f"Retrieved {len(result_dict)} records.")
    return result_dict

def clean_pool_price(raw_pool: Dict[str, str]) -> Dict:
    """Clean up a pool price entry."""
    return {
        "timestamp": raw_pool["begin_datetime_mpt"],
        "pool_price": raw_pool["pool_price"],
        "forecast_pool_price": raw_pool["forecast_pool_price"]
    }

def noisy_forecast(clean_pool: Dict[str, str]):
    """Add some noise to forecasts so I can be sure they change.

    I don't want every record to change, but I do want some change so I can see
    how that will work.
    """
    # probability that I actually add noise, let's say I add it to 10% of records
    cutoff = 0.1
    if random.random() < cutoff:
        base_fcst = float(clean_pool["forecast_pool_price"])
        scale_factor = random.uniform(0.9, 1.1)
        noisy_forecast = base_fcst * scale_factor
        clean_pool["forecast_pool_price"] = f"{noisy_forecast:.2f}"
    return clean_pool

def process_prices() -> List[Dict[str, str]]:
    """Get pool prices with some noise in the forecast in the format I want."""
    return [
        noisy_forecast(clean_pool_price(pool_price)) for pool_price in get_pool_prices()
    ]

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    result_dict = process_prices()
    return func.HttpResponse(json.dumps(result_dict))
