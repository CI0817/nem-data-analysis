'''
This script analyses the generation mix and how it changes on average throughout the day.
'''

import nemosis
import pandas as pd
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates


def plot_duck_curve(start_time, end_time):
    # Download the generation mix data from NEMOSIS
    scada_table = "DISPATCH_UNIT_SCADA"
    raw_data_cache = "./raw_data_cache"

    scada_data = nemosis.dynamic_data_compiler(start_time, end_time, scada_table, raw_data_cache,
                                                select_columns=['SETTLEMENTDATE', 'DUID', 'SCADAVALUE'])

    # Convert the SCADA value to pd numerical value to filter out zeros
    scada_data['SCADAVALUE'] = pd.to_numeric(scada_data['SCADAVALUE'])
    # print(scada_data)
    scada_data = scada_data[scada_data['SCADAVALUE'] > 0]
    # print(scada_data)

    # Read the generator data from the xlsx file downloaded from AEMO
    # The file can be downloaded via this link: https://aemo.com.au/-/media/files/electricity/nem/participant_information/nem-registration-and-exemption-list.xlsx
    local_file = "./NEM Registration and Exemption List.xlsx"
    gen_info = pd.read_excel(local_file, sheet_name="PU and Scheduled Loads")
    # print(gen_info)

    # Filter the generation data to only have DUID, Fuel Type, and Region
    filtered_gen_info = gen_info[['DUID', 'Fuel Source - Primary', 'Region']]
    # print(filtered_gen_info)

    # Merge the generation data with the scada data
    merged_data = pd.merge(scada_data, filtered_gen_info, on='DUID', how='left') # left join to prevent losing scada data if no gen info
    # print(merged_data)

    # Create a plot
    plt.figure(figsize=(15, 6))

    # Filter the target region
    target_region = "VIC1"
    region_data = merged_data[merged_data['Region'] == target_region]
    # print(region_data)

    # Group the data by fuel type and sum the SCADA value ordering by time
    fuel_mix = region_data.pivot_table(index='SETTLEMENTDATE', 
                                        columns='Fuel Source - Primary', 
                                        values='SCADAVALUE', 
                                        aggfunc='sum').fillna(0)
    # print(fuel_mix)

    # Smooth out the data by resampling to 30min
    fuel_mix = fuel_mix.resample('30min').mean()

    # Get the list of fuel types
    existing_fuels = fuel_mix.columns.tolist()
    # print(existing_fuels)

    # Add fuel type random colors
    colors = cm.rainbow(np.linspace(0, 1, len(existing_fuels)))

    # Create a stackplot
    plt.stackplot(fuel_mix.index, fuel_mix.values.T, labels=existing_fuels, colors=colors)

    # Format the plot
    start_date_str = pd.Timestamp(start_time).strftime('%Y-%m-%d')
    end_date_str = pd.Timestamp(end_time).strftime('%Y-%m-%d')
    if start_date_str == end_date_str:
        plt.title(f"Generation Mix for {target_region} on {start_date_str}")
        # Single Day: Tick every few hours, format as HH:MM
        plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    else:
        plt.title(f"Generation Mix for {target_region} between {start_date_str} and {end_date_str}")
        # Multi-Day: Force ticks to be exactly once per Day, change the interval to be less frequent if needed
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=2))
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.gcf().autofmt_xdate() # Rotate date labels
    plt.xlabel("Time")
    plt.xlim(pd.Timestamp(start_time),pd.Timestamp(end_time))
    plt.ylabel("Generation (MW)")
    # plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.legend(bbox_to_anchor=(1,1), title='Fuel Type', loc='upper left')
    plt.subplots_adjust(right=0.8)
    plt.show()

if __name__ == "__main__":
    start_time = "2025/06/01 00:00:00"
    end_time = "2025/06/30 23:55:00"
    plot_duck_curve(start_time, end_time)