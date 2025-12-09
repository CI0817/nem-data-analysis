'''
This script analyses the generation mix and how it changes on average throughout the day.
'''

import nemosis
import pandas as pd

# Download the generation mix data from NEMOSIS
start_time = "2025/01/15 00:00:00"
end_time = "2025/01/15 23:55:00"
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
merged_data = pd.merge(scada_data, filtered_gen_info, on='DUID', , how='left') # left join to prevent losing scada data if no gen info
print(merged_data)

