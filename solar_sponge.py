'''
This script visualise the price trough caused by solar during the day.
Focusing on data between 2025/01/01 and 2025/01/31 in Victoria.
'''

import nemosis
import pandas as pd
import matplotlib.pyplot as plt

# Download the data
start_time = "2025/01/01 00:00:00"
end_time = "2025/10/31 23:55:00"
table = "DISPATCHPRICE"
raw_data_cache = "./raw_data_cache"

price_data = nemosis.dynamic_data_compiler(start_time, end_time, table, raw_data_cache,
                                            select_columns=['SETTLEMENTDATE', 'REGIONID','RRP'],
                                            filter_cols=['REGIONID'], filter_values=[['VIC1']])

# Convert the datetime column to pd datatime object for easy extraction
price_data['SETTLEMENTDATE'] = pd.to_datetime(price_data['SETTLEMENTDATE'])

# Extract the 'HOUR' and 'MONTH' from the 'SETTLEMENTDATE'
price_data['HOUR'] = price_data['SETTLEMENTDATE'].dt.hour
price_data['MONTH'] = price_data['SETTLEMENTDATE'].dt.month

# Create plot with 10 subplots for the 10 months
fig, axes = plt.subplots(5, 2, figsize=(12, 15), sharex=True, sharey=True)
axes = axes.flatten() # flatten the axes for easier looping

for i, month in enumerate(range(1,11)):
    # Get the current month price data
    monthly_data = price_data[price_data['MONTH']==month]

    # Calculate the average price by hour for that month
    avg_price = monthly_data.groupby('HOUR')['RRP'].mean()

    # Plot the result on a specific subplot
    ax = axes[i]
    avg_price.plot(kind='line', marker='o', ax=ax)

    # Style the plot
    ax.set_title(f"Month {month}")
    ax.axhline(0, color='red', linestyle='--', linewidth=1)
    ax.grid(True)

fig.supylabel("Price ($/MWh)")
fig.supxlabel("Hour of Day (0-23)")
fig.suptitle("Average Spot Price by Month in Victoria between Jan and Oct 2025")

# plt.tight_layout()
plt.show()

# print(price_data)
# print(average_price_by_hour)

