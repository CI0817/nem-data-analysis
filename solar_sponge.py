'''
This script visualises the price trough caused by solar during the day.
It plots the RRP (Regional Reference Price) for a specified time range in Victoria.
'''

import nemosis
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot_price(start_time, end_time):
    # Download the price data
    table = "DISPATCHPRICE"
    raw_data_cache = "./raw_data_cache"

    # Fetch data using NEMOSIS
    price_data = nemosis.dynamic_data_compiler(start_time, end_time, table, raw_data_cache,
                                                select_columns=['SETTLEMENTDATE', 'REGIONID','RRP'],
                                                filter_cols=['REGIONID'], filter_values=[['VIC1']])

    # Convert the datetime column to pd datatime object
    price_data['SETTLEMENTDATE'] = pd.to_datetime(price_data['SETTLEMENTDATE'])

    # Create a plot
    plt.figure(figsize=(15, 6))

    # Plot the RRP against time
    plt.plot(price_data['SETTLEMENTDATE'], price_data['RRP'], color="orange", label="RRP (VIC1)")

    # Format the plot based on date range (Single day vs Multi-day)
    start_date_str = pd.Timestamp(start_time).strftime('%Y-%m-%d')
    end_date_str = pd.Timestamp(end_time).strftime('%Y-%m-%d')

    if start_date_str == end_date_str:
        plt.title(f"Electricity Price (RRP) for VIC1 on {start_date_str}")
        # Single Day: Tick every few hours, format as HH:MM
        plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    else:
        plt.title(f"Electricity Price (RRP) for VIC1 between {start_date_str} and {end_date_str}")
        # Multi-Day: Force ticks to be exactly once per Day
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.gcf().autofmt_xdate() # Rotate date labels

    # General styling
    plt.xlabel("Time")
    plt.ylabel("Price ($/MWh)")
    plt.xlim(pd.Timestamp(start_time), pd.Timestamp(end_time))
    plt.axhline(0, color="red", linestyle="--", linewidth=1, label="Zero Price")
    plt.grid(True, color='gray', alpha=0.3)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    start_time = "2025/06/10 00:00:00"
    end_time = "2025/06/20 23:55:00"
    plot_price(start_time, end_time)