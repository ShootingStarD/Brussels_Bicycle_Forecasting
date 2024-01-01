import datetime as dt
from typing import List

import pandas as pd
import requests

from .constants import BIKE_API_BASE_URL

API_REQUEST_DATE_FORMAT = "%Y%m%d"
import pandera as pa
from pandera.typing import DataFrame, Series

"""
Fetch the measures of the bikes accross devices from the Brussels Mobility Bike Counts API
"""


class BikeMeasuresSingleDeviceRawSchema(pa.SchemaModel):
    """
    Raw Schema of a dataframe containing measures for a single device in a timespan.

    This Schema is for the raw data, not yet preprocessed
    """

    date: Series[str]
    time_gap: Series[int]
    count: Series[int]
    average_speed: Series[int]


class BikeMeasuresMultipleDevicesRawSchema(pa.SchemaModel):
    """
    Raw Schema of a dataframe containing measures for a multiple devices in a timespan.

    This Schema is for the raw data, not yet preprocessed
    """

    date: Series[str]
    time_gap: Series[int]
    count: Series[int]
    average_speed: Series[int]
    device: Series[str]


@pa.check_output(BikeMeasuresSingleDeviceRawSchema)
def get_bike_counts_for_one_device(
    device: str,
    start_date: dt.date,
    end_date: dt.date,
) -> DataFrame[BikeMeasuresSingleDeviceRawSchema]:
    """
    Retrieve the counts and speeds of bikes for one device in a specific time range.

    Parameters
    ----------
    device : str
        the device of which to query the metrics
    start_date : dt.date
        the data at which we want to start retrieving measures
    end_date : dt.date
        the date at which we want to end retrieving measures

    Returns
    -------
    pd.DataFrame
        dataframe with counts and speeds of vehicle every 15 minutes in the specified time range

    Raises
    ------
    response.raise_for_status
        if the data was not accessed
    """
    url = f"{BIKE_API_BASE_URL}?request=history&featureID={device}&startDate={start_date.strftime(API_REQUEST_DATE_FORMAT)}&endDate={end_date.strftime(API_REQUEST_DATE_FORMAT)}"
    response = requests.get(url)

    if not response.status_code == 200:
        raise response.raise_for_status()
    json_bike_counts = response.json()["data"]
    bike_counts_df = pd.json_normalize(json_bike_counts)
    bike_counts_df = bike_counts_df.rename(columns={"count_date": "date"})
    return bike_counts_df


@pa.check_output(BikeMeasuresMultipleDevicesRawSchema)
def get_bike_counts_accross_devices(
    devices: List[str],
    start_date: dt.date,
    end_date: dt.date,
) -> DataFrame[BikeMeasuresMultipleDevicesRawSchema]:

    bike_measures_list = []
    for device in devices:
        bikes_measures_one_device = get_bike_counts_for_one_device(
            device, start_date, end_date
        )
        bikes_measures_one_device["device"] = device
        bike_measures_list.append(bikes_measures_one_device)
    bike_measures_accross_devices_df = pd.concat(bike_measures_list)
    return bike_measures_accross_devices_df
