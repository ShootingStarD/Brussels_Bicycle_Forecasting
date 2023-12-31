import pandas as pd
from brussels_bike_forecasting.data_fetching.data_fetching import get_sensor_devices_dataframe

from brussels_bike_forecasting.data_fetching.data_fetching import get_sensor_devices_json


def test_get_sensor_devices_json():
    json_response = get_sensor_devices_json()
    
    assert isinstance(json_response,list)


def test_get_sensor_devices_dataframe():
    df_response = get_sensor_devices_dataframe()
    assert isinstance(df_response, pd.DataFrame)
