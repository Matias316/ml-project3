from weatherbit.api import Api
import pandas as pd

API_KEY = "USER_YOUR_API"

# Configuring weather bit API
api = Api(API_KEY)
api.set_granularity('daily')

# Returns max and min temperatures for specific latitude, longitude and date
def retrieve_temps(row):
    history = api.get_history(lat=row['latitude'], lon=row['longitude'], start_date=row['start_date'].strftime("%Y-%m-%d"), end_date=row['end_date'].strftime("%Y-%m-%d") )
    temp_series = history.get_series(['max_temp','min_temp'])[0]
    max = temp_series.get('max_temp')
    min = temp_series.get('min_temp')
    return max, min

def obtain_temperatures(input_file, output_file, sample_size = 0):
    corona_df = pd.read_csv(input_file)

    # Normalize column names
    columns_mappings = {'Last_Update': 'last_update', 'Last Update': 'last_update', 'Lat': 'latitude', 'Latitude':'latitude', 'Long_':'longitude', 'Longitude':'longitude'}
    corona_df.rename(columns = columns_mappings, inplace = True)

    # Drop records with null values in key columns
    corona_df.dropna(subset=['last_update', 'latitude', 'longitude'], inplace=True)

    # If sample_size not provided use all records from input_file
    if (sample_size > 0):      
        corona_df = corona_df.sample(sample_size)

    # Convert to datetime
    corona_df['last_update'] = pd.to_datetime(corona_df['last_update'], infer_datetime_format=True)

    # Extract date and calculate EndDate
    corona_df['start_date'] = corona_df['last_update'].dt.date
    corona_df['end_date'] = corona_df['start_date'] + pd.DateOffset(1)

    corona_df[['max_temp','min_temp']] = corona_df.apply(lambda row: retrieve_temps(row), axis=1, result_type="expand")

    #Calculate average temperatures using max and min temperatures
    corona_df['avg_temp'] = corona_df[['max_temp', 'min_temp']].mean(axis=1).round(2)

    # Exporting as new CSV
    corona_df.to_csv(output_file, index=False)