"""
Pre-process count speed bike data from Brussels Mobility.
"""
import datetime as dt
from typing import Optional, Union

import pandas as pd
import pandera as pa
from pandera.typing import DataFrame, Series

from brussels_bike_forecasting.data_fetching.fetch_bikes_measures import (
    BikeMeasuresMultipleDevicesRawSchema,
    BikeMeasuresSingleDeviceRawSchema,
)


class BikeMeasuresSchema(pa.SchemaModel):
    """
    Schema of a dataframe containing bikes measures for one or multiple devices in a timespan.

    This Schema is for preprocessed data
    """

    timestamp: Series[dt.datetime]
    count: Series[int]
    average_speed: Series[int]
    hour: Series[pa.Int32]
    minute: Series[pa.Int32]
    device: Optional[Series[str]]


def format_bike_metrics(
    bike_dataframe: Union[
        BikeMeasuresSingleDeviceRawSchema, BikeMeasuresMultipleDevicesRawSchema
    ]
) -> DataFrame[BikeMeasuresSchema]:
    """
    Preprocess a bike metrics dataframe to make it ready to be analyzed in plots.


    Parameters
    ----------
    bike_dataframe : Union[BikeMeasuresSingleDeviceRawSchema, BikeMeasuresMultipleDevicesRawSchema]
        either a dataframe containing metrics for a single or multiple devices sensoring bikes metrics

    Returns
    -------
    pd.DataFrame
        preprocess dataframe
    """

    bike_dataframe = bike_dataframe.copy()
    bikes_dates = bike_dataframe[BikeMeasuresSingleDeviceRawSchema.date]
    bikes_timegap = bike_dataframe[BikeMeasuresSingleDeviceRawSchema.time_gap]
    bikes_minutes = bikes_timegap.astype(int) * 15
    bikes_timestamp = pd.to_datetime(bikes_dates, format="%Y/%m/%d")
    bike_dataframe["timestamp"] = bikes_timestamp + pd.to_timedelta(
        bikes_minutes, unit="m"
    )
    bike_dataframe = bike_dataframe.drop(
        columns=[
            BikeMeasuresSingleDeviceRawSchema.date,
            BikeMeasuresSingleDeviceRawSchema.time_gap,
        ]
    )
    bike_dataframe["hour"] = bike_dataframe["timestamp"].dt.hour
    bike_dataframe["day_week"] = bike_dataframe["timestamp"].dt.day_of_week
    bike_dataframe["minute"] = bike_dataframe["timestamp"].dt.minute
    return bike_dataframe
