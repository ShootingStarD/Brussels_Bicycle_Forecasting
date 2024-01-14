import datetime as dt

from brussels_bike_forecasting.data_fetching.fetch_bikes_measures import (
    get_bike_counts_for_one_device,
)
from brussels_bike_forecasting.data_preprocessing.bikes_formatting import (
    BikeMeasuresSchema,
    format_bike_metrics,
)


def test_preprocessing_bikes_measures():
    device = "CB2105"
    start_date = dt.date(year=2022, month=1, day=1)
    end_date = dt.date(year=2022, month=1, day=31)
    bike_raw_df = get_bike_counts_for_one_device(device, start_date, end_date)

    bike_preprocessed_df = format_bike_metrics(bike_raw_df)
    BikeMeasuresSchema.validate(bike_preprocessed_df)


# TODO hypothesis test
