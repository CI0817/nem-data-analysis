'''
This script visualise the price trough caused by solar during the day.
Focusing on data between 2025/01/01 and 2025/01/31 in Victoria.
'''

import nemosis
import pandas as pd
import matplotlib.pyplot as plt

# Download the data
start_time = "2025/01/01 00:00:00"
end_time = "2025/01/31 23:55:00"
table = "DISPATCHPRICE"
raw_data_cache = "./raw_data_cache"

price_data = nemosis.dynamic_data_compiler(start_time, end_time, table, raw_data_cache,
                                            select_columns=['SETTLEMENTDATE', 'REGIONID','RRP'],
                                            filter_cols=['REGIONID'], filter_values=[['VIC1']])

# Convert the datetime column to pd datatime object for easy extraction
price_data['SETTLEMENTDATE'] = pd.to_datetime(price_data['SETTLEMENTDATE'])

# Extract just the "Hour" (0 to 23) from the timestamp
price_data['HOUR'] = price_data['SETTLEMENTDATE'].dt.hour

# Group by hour and calculate the average price
average_price_by_hour = price_data.groupby('HOUR')['RRP'].mean()

# Visualise the average price by hour
plt.figure(figsize=(10,5))
average_price_by_hour.plot(kind="line", marker="o", color="orange", linewidth=2)

plt.axhline(0, color="red", linestyle="--", linewidth=1, label="Zero Price Floor")
plt.title("Average Spot Price by Hour in Victoria in January of 2025")
plt.ylabel("Price ($/MWh)")
plt.xlabel("Hour of Day (0-23)")
plt.grid(True)
plt.legend()

plt.show()

# print(price_data)
# print(average_price_by_hour)

