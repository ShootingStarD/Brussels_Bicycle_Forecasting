import datetime as dt

from brussels_bike_forecasting.data_fetching.fetch_bikes_measures import (
    get_bike_counts_accross_devices,
    get_bike_counts_for_one_device,
)


def test_get_bike_counts_for_one_device():
    """
    Checks that the function `get_bike_counts_for_one_device` executes without errors in a simple case
    """
    device = "CB2105"
    start_date = dt.date(year=2022, month=1, day=1)
    end_date = dt.date(year=2023, month=1, day=1)
    get_bike_counts_for_one_device(device, start_date, end_date)


def test_get_bike_counts_accross_devices():
    """
    Checks that the function `get_bike_counts_accross_devices` executes without errors in a simple case
    """
    devices = ["CB2105", "CAT17"]
    start_date = dt.date(year=2022, month=1, day=1)
    end_date = dt.date(year=2023, month=1, day=1)
    get_bike_counts_accross_devices(devices, start_date, end_date)
