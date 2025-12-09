'''
This script visualise the price trough caused by solar during the day.
Focusing on data between 2025/01/01 and 2025/10/31 in Victoria.
'''

import nemosis
import pandas as pd
import matplotlib.pyplot as plt
import math

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

def plot_average_price_by_months(months, data):
    """
    Plots average RRP by hour for the specified list of months.
    """
    num_plots = len(months)
    
    # distinct logic for single vs multiple plots
    if num_plots == 1:
        fig, axes = plt.subplots(1, 1, figsize=(10, 5))
        axes = [axes] # Make it a list so we can loop over it identically
    else:
        cols = 2
        rows = math.ceil(num_plots / cols)
        # Adjust figure height based on rows
        fig, axes = plt.subplots(rows, cols, figsize=(12, 3 * rows), sharex=True, sharey=True)
        axes = axes.flatten()

    for i, month in enumerate(months):
        ax = axes[i]
        
        # Filter and Group
        monthly_data = data[data['MONTH'] == month]
        avg_price = monthly_data.groupby('HOUR')['RRP'].mean()
        
        # Plot
        avg_price.plot(kind="line", marker="o", color="orange", ax=ax)
        
        # Styling
        ax.set_title(f"Month {month}")
        ax.axhline(0, color="red", linestyle="--", linewidth=1)
        ax.set_xlabel("")
        ax.grid(True)

    # Hide any unused subplots (e.g. if you plot 3 months in a 2x2 grid)
    for j in range(i + 1, len(axes)):
        axes[j].axis('off')

    # Global Labels
    fig.supylabel("Price ($/MWh)")
    fig.supxlabel("Hour of Day (0-23)")
    fig.suptitle(f"Average Spot Price in Victoria (Months: {months})")
    
    plt.show()

plot_average_price_by_months([6], price_data)

# plot_average_price_by_months([1, 3, 5], price_data)

# plot_average_price_by_months(range(1, 11), price_data)