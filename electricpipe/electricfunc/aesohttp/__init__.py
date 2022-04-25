import datetime as dt
import json
import logging
import os
import random
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import azure.functions as func
import sqlalchemy


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
        "pool_time_stamp": dt.datetime.fromisoformat(raw_pool["begin_datetime_mpt"]),
        "pool_price": raw_pool["pool_price"],
        "forecast_pool_price": raw_pool["forecast_pool_price"],
        "insert_time_stamp": dt.datetime.now(),
    }


def noisy_forecast(clean_pool: Dict[str, str]):
    """Add some noise to forecasts so I can be sure they change.

    I don't want every record to change, but I do want some change so I can see
    how that will work.
    """
    # probability that I actually add noise, let's say I add it to 1% of records
    cutoff = 0.01
    if random.random() < cutoff and clean_pool["forecast_pool_price"] != "":
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


class MSDatabase:
    """Helper class to access the SQL server database."""

    _meta = sqlalchemy.MetaData()

    @property
    def engine(self) -> sqlalchemy.engine.Engine:
        """Get a connection to the mssql database."""
        sqlip = os.getenv("SQLIP")
        sa_pass = os.getenv("SA_PASSWORD")
        connection_url = sqlalchemy.engine.URL.create(
            "mssql+pyodbc",
            username="sa",
            password=sa_pass,
            host=sqlip,
            port=1433,
            database="electric",
            query={"driver": "ODBC Driver 17 for SQL Server"},
        )
        return sqlalchemy.create_engine(connection_url)

    @property
    def metadata(self) -> sqlalchemy.schema.MetaData:
        return self.__class__._meta

    def get_table(self, table_str: str) -> sqlalchemy.Table:
        return sqlalchemy.Table(table_str, self.metadata, autoload_with=self.engine)


def floatmapper(instr: str) -> Optional[float]:
    """Convert a string to float."""
    try:
        return float(instr)
    except:
        return None


def stage_sql() -> None:
    """Stage the latest AESO query to the database."""
    db = MSDatabase()
    engine = db.engine
    poolstage = db.get_table("poolstage")
    prices = process_prices()
    for price in prices:
        for col in ["forecast_pool_price", "pool_price"]:
            price[col] = floatmapper(price[col])
    with engine.connect() as conn:
        conn.execute("truncate table poolstage;")
        _ = conn.execute(sqlalchemy.insert(poolstage), prices)
    logging.info(f"Staged {len(prices):,.0f} records")


def update_pool() -> Tuple[int, int]:
    db = MSDatabase()
    stage_tbl = db.get_table("poolstage")
    pool_tbl = db.get_table("poolprice")
    stage_key = stage_tbl.c.pool_time_stamp
    pool_key = pool_tbl.c.pool_time_stamp
    update_stmt = (
        pool_tbl.update()
        .values(forecast_pool_price=stage_tbl.c.forecast_pool_price, update_time_stamp=stage_tbl.c.insert_time_stamp)
        .where(stage_key == pool_key)
        .where(stage_tbl.c.forecast_pool_price != pool_tbl.c.forecast_pool_price)
    )

    insert_select = sqlalchemy.select(
        [
            stage_key,
            stage_tbl.c.pool_price,
            stage_tbl.c.forecast_pool_price,
            stage_tbl.c.insert_time_stamp,
            stage_tbl.c.insert_time_stamp.label("update_time_stamp"),
        ]
    ).where(stage_key.notin_(sqlalchemy.select([pool_key])))
    insert_cols = ["pool_time_stamp", "pool_price", "forecast_pool_price", "insert_time_stamp", "update_time_stamp"]
    insert_stmt = pool_tbl.insert().from_select(insert_cols, insert_select)
    with db.engine.connect() as conn:
        update_r = conn.execute(update_stmt)
        insert_r = conn.execute(insert_stmt)
        logging.info(f"Updated {update_r.rowcount} rows")
        logging.info(f"Inserted {insert_r.rowcount} rows")
        return update_r.rowcount, insert_r.rowcount



def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")
    # result_dict = process_prices()
    # return func.HttpResponse(json.dumps(result_dict))
    stage_sql()
    updates, inserts = update_pool()
    return func.HttpResponse(f"Inserted {inserts} rows and updated {updates} rows.")
