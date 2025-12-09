'''
This script analyses the generation mix and how it changes on average throughout the day.
'''

import nemosis
import pandas as pd

# Download the generation mix data from NEMOSIS
start_time = "2025/01/15 00:00:00"
end_time = "2025/01/15 23:55:00"
table = "DISPATCH_UNIT_SCADA"
raw_data_cache = "./raw_data_cache"

scada_data = nemosis.dynamic_data_compiler(start_time, end_time, table, raw_data_cache,
                                            select_columns=['SETTLEMENTDATE', 'DUID', 'SCADAVALUE'])

# Convert the SCADA value to pd numerical value to filter out zeros
scada_data['SCADAVALUE'] = pd.to_numeric(scada_data['SCADAVALUE'])
# print(scada_data)
scada_data = scada_data[scada_data['SCADAVALUE'] > 0]
# print(scada_data)

