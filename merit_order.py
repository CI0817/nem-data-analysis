"""
This script plots the theoretical electricity price based on supply and demand and fixed costs.
"""

# Get the demand data in Victoria
import nemosis
import pandas as pd

start_time = "2025/06/10 00:00:00"
end_time = "2025/06/20 23:55:00"
demand_table = "DISPATCHREGIONSUM" # the total demand of a region
raw_data_cache = "./raw_data_cache"

demand_data = nemosis.dynamic_data_compiler(
    start_time, end_time, demand_table, raw_data_cache,
    select_columns=['SETTLEMENTDATE', 'REGIONID', 'TOTALDEMAND'],
    filter_cols=['REGIONID'], filter_values=[['VIC1']])

# Convert the SETTLEMENTDATE to pd datetime object
demand_data['SETTLEMENTDATE'] = pd.to_datetime(demand_data['SETTLEMENTDATE'])

# Set datetime as index
demand_data.set_index('SETTLEMENTDATE', inplace=True)

# print(demand_data)

# Get the supply data
supply_table = "DISPATCHLOAD"
supply_data = nemosis.dynamic_data_compiler(
    start_time, end_time, supply_table, raw_data_cache,
    select_columns=['SETTLEMENTDATE','DUID','AVAILABILITY', 'INTERVENTION'],
    filter_cols=['INTERVENTION'], filter_values=[[0]])

# Select only the settlementdate, duid, and availability
supply_data = supply_data[['SETTLEMENTDATE', 'DUID', 'AVAILABILITY']]

# print(supply_data)

# Keep only the generators that produce something
supply_data = supply_data[supply_data['AVAILABILITY'] > 0]

# print(supply_data)

# Read the generator data from the given excel sheet
local_file = "./NEM Registration and Exemption List.xlsx"
gen_info = pd.read_excel(local_file, sheet_name="PU and Scheduled Loads")

# Get the Victorian generators
filtered_region = 'VIC1'
filtered_gen_info = gen_info[gen_info['Region'] == filtered_region]

# Get the list of DUIDs in Victoria
vic_duids = filtered_gen_info['DUID'].tolist()

# print(vic_duids)

# Get the supply data that is only from Victorian generators
supply_data = supply_data[supply_data['DUID'].isin(vic_duids)]

# print(supply_data)

# Get the fuel type and the duid, and join it with the supply data
fuel_type = filtered_gen_info[['DUID', 'Fuel Source - Primary']].set_index('DUID')
supply_data = supply_data.join(fuel_type, on='DUID')

# print(supply_data)

