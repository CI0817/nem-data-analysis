"""
This script plots the theoretical electricity price based on supply and demand and fixed costs.
"""

# Get the demand data in Victoria
import nemosis
import pandas as pd

start_time = "2025/06/10 00:00:00"
end_time = "2025/06/20 23:55:00"
table = "DISPATCHREGIONSUM" # the total demand of a region
raw_data_cache = "./raw_data_cache"

demand_data = nemosis.dynamic_data_compiler(
    start_time, end_time, table, raw_data_cache,
    select_columns=['SETTLEMENTDATE', 'REGIONID', 'TOTALDEMAND'],
    filter_cols=['REGIONID'], filter_values=[['VIC1']])

# Convert the SETTLEMENTDATE to pd datetime object
demand_data['SETTLEMENTDATE'] = pd.to_datetime(demand_data['SETTLEMENTDATE'])

# Set datetime as index
demand_data.set_index('SETTLEMENTDATE', inplace=True)

print(demand_data)
