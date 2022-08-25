from weatherbit_calculation import obtain_temperatures

corona_input_file = 'datasets/Corona.csv'
corona_output_file = 'datasets/Corona_with_temperatures.csv'

# Obtain temperatures for initial dataset
obtain_temperatures(corona_input_file, corona_output_file)

corona_input_file = 'datasets/Corona_2021_01_20.csv'
corona_input_file = 'datasets/Corona_2021_01_20_with_temperatures.csv'

# Obtain temperatures for second dataset for comparisons
obtain_temperatures(corona_input_file, corona_output_file, sample_size = 250)
