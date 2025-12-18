"""
This script plots the theoretical electricity price based on supply and demand and fixed costs.
"""

# Get the demand data in Victoria
import nemosis
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def get_demand(start_time, end_time, raw_data_cache):
    demand_table = "DISPATCHREGIONSUM" # the total demand of a region
    demand_data = nemosis.dynamic_data_compiler(
        start_time, end_time, demand_table, raw_data_cache,
        select_columns=['SETTLEMENTDATE', 'REGIONID', 'TOTALDEMAND'],
        filter_cols=['REGIONID'], filter_values=[['VIC1']])
      
    # Convert the SETTLEMENTDATE to pd datetime object
    demand_data['SETTLEMENTDATE'] = pd.to_datetime(demand_data['SETTLEMENTDATE'])

    # Set datetime as index
    demand_data.set_index('SETTLEMENTDATE', inplace=True)

    return demand_data

def get_supply(start_time, end_time, raw_data_cache):
    supply_table = "DISPATCHLOAD"
    supply_data = nemosis.dynamic_data_compiler(
        start_time, end_time, supply_table, raw_data_cache,
        select_columns=['SETTLEMENTDATE','DUID','AVAILABILITY', 'INTERVENTION'],
        filter_cols=['INTERVENTION'], filter_values=[[0]])

    # Select only the settlementdate, duid, and availability
    supply_data = supply_data[['SETTLEMENTDATE', 'DUID', 'AVAILABILITY']]
    
    # Keep only the generators that produce something
    supply_data = supply_data[supply_data['AVAILABILITY'] > 0]

    # Read the generator data from the given excel sheet
    local_file = "./NEM Registration and Exemption List.xlsx"
    gen_info = pd.read_excel(local_file, sheet_name="PU and Scheduled Loads")

    # Get the Victorian generators
    filtered_region = 'VIC1'
    filtered_gen_info = gen_info[gen_info['Region'] == filtered_region]

    # Get the list of DUIDs in Victoria
    vic_duids = filtered_gen_info['DUID'].tolist()

    # Get the supply data that is only from Victorian generators
    supply_data = supply_data[supply_data['DUID'].isin(vic_duids)]

    # Get the fuel type and the duid, and join it with the supply data
    fuel_type = filtered_gen_info[['DUID', 'Fuel Source - Primary']].set_index('DUID')
    supply_data = supply_data.join(fuel_type, on='DUID')

    # Merge the supply available by fuel type
    supply_merged = supply_data.groupby(['SETTLEMENTDATE', 'Fuel Source - Primary'])['AVAILABILITY'].sum().unstack(fill_value=0)

    return supply_merged

def get_merit_order():
    # Define the cost dictionary of each fuel type
    # These numbers are quite arbitrary and fixed; in reality, these prices are dynamics and update every 5 mins or so.
    # It's too complicated to model them dynamically for now.
    merit_order = {
        # Renewables
        'Solar': 0,
        'Wind': 0,
        'Hydro': 45,
        # Storage
        'Battery Storage': 90,
        # Fossils
        'Fossil': 20,
        'Brown Coal': 20,
        'Black Coal': 55,
        'Natural Gas': 300,
        'Liquid Fuel': 500
    }

    return merit_order

def calculate_price(demand, supply, merit_order):
    # Align data timestamps
    common_index = demand.index.intersection(supply.index)
    demand = demand.loc[common_index]
    supply = supply.loc[common_index]

    # Identify which fuels from our merit order exist in the actual data
    available_fuels = [f for f in merit_order.keys() if f in supply.columns]

    # Sort them by price (cheapest first)
    sorted_stack = sorted(available_fuels, key=lambda x: merit_order[x])
    
    simulated_prices = []
    
    for timestamp in common_index:
        current_demand = demand.loc[timestamp, 'TOTALDEMAND']
        cumulative_supply = 0
        cleared_price = 15000 # Default to market cap price if we run out of supply
        
        # Stack the generators
        for fuel in sorted_stack:
            fuel_avail = supply.loc[timestamp, fuel]
            cumulative_supply += fuel_avail
            
            # If we have enough power to meet demand, this fuel sets the price
            if cumulative_supply >= current_demand:
                cleared_price = merit_order[fuel]
                break
        
        simulated_prices.append(cleared_price)
        
    return pd.DataFrame({'Simulated_Price': simulated_prices}, index=common_index)

def plot_price(data, start_time, end_time):
    # Create a plot
    plt.figure(figsize=(15, 6))

    # Plot the simulated price
    plt.plot(data.index, data['Simulated_Price'], color="orange", label="Simulated Price")

    # Format the plot
    plt.title("Simulated Electricity Price")
    plt.xlabel("Time")
    plt.ylabel("Price ($/MWh)")
    plt.xlim(pd.Timestamp(start_time), pd.Timestamp(end_time))
    plt.axhline(0, color="red", linestyle="--", linewidth=1, label="Zero Price")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

    plt.show()

if __name__ == "__main__":
    start_time = "2025/06/10 00:00:00"
    end_time = "2025/06/20 23:55:00"
    raw_data_cache = "./raw_data_cache"
    demand_data = get_demand(start_time, end_time, raw_data_cache)
    supply_data = get_supply(start_time, end_time, raw_data_cache)
    merit_order = get_merit_order()
    price_data = calculate_price(demand_data, supply_data, merit_order)
    plot_price(price_data, start_time, end_time)