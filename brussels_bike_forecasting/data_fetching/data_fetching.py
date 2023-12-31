from pathlib import Path
import pandas as pd
import requests
from typing import Dict, List
import argparse
def get_sensor_devices_json()->List[Dict]:
    """
    Get a list of all bike sensors from Brussels Mobility Bike API.

    Returns
    -------
    List[Dict]
        the list of all bikes sensors from Brussels Mobility Bike API.

    Raises
    ------
    response.raise_for_status
        _description_
    """
    DEVICE_REQUEST = "https://data.mobility.brussels/bike/api/counts/?request=devices"

    response = requests.get(DEVICE_REQUEST)
    if not response.status_code == 200:
        raise response.raise_for_status()
    return response.json()["features"]        

def get_sensor_devices_dataframe()->pd.DataFrame:
    """
    Get a dataframe with most important informations of the sensor devices
    
    Having a dataframe of those devices will allow easy plotting as well as querying bikes counts from all those devices

    Returns
    -------
    pd.DataFrame
        dataframe with all important static informations of bike counts sensors.
    """
    json_devices = get_sensor_devices_json()
    devices_df = pd.json_normalize(json_devices)
    DEVICES_IMPORTANT_COLUMNS = [
        "properties.device_name",
        "geometry.type",
        "geometry.coordinates",
        "properties.road_en",
        'properties.lane_schema',
        'properties.basic_schema',
        'properties.detailed_schema', 
        'properties.picture_1',
        'properties.picture_2'
    ]
    devices_df = devices_df[DEVICES_IMPORTANT_COLUMNS]
    devices_df.columns = [column.split(".")[1] for column in devices_df.columns]
    return devices_df
    
def sensor_devices_to_parquet(path:Path):
    """
    Load and save sensors devices in a parquet file
    """
    get_sensor_devices_dataframe().to_parquet()
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Save the devices data from Brussels Mobility Bike API into a parquet file.')
    parser.add_argument(
        'output_file', 
        type=str, 
        help='Path of the parquet file'
    )
    args = parser.parse_args()
    path = Path(args.output_file)
    if path.exists():
        raise FileExistsError(f"File already exists at path {path.absolute()}")
    get_sensor_devices_dataframe().to_parquet(path)