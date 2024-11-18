
# Athletic Sales Analysis
# Assignment for analyzing sales data to gain insights.

import pandas as pd

# Load the data
data_2020 = pd.read_csv('athletic_sales_2020.csv')
data_2021 = pd.read_csv('athletic_sales_2021.csv')

# Combine the data
combined_data = pd.concat([data_2020, data_2021], ignore_index=True)

# Convert 'invoice_date' to datetime
combined_data['invoice_date'] = pd.to_datetime(combined_data['invoice_date'], errors='coerce')

# Determine which region sold the most products
region_product_sales = combined_data.groupby(['region', 'state', 'city']).agg(
    Total_Units_Sold=('units_sold', 'sum')
).sort_values(by='Total_Units_Sold', ascending=False).reset_index()

# Determine which region had the most sales
region_total_sales = combined_data.groupby(['region', 'state', 'city']).agg(
    Total_Sales=('total_sales', 'sum')
).sort_values(by='Total_Sales', ascending=False).reset_index()

# Create a pivot table with 'invoice_date' as the index and 'total_sales' as values
sales_by_date_pivot = combined_data.pivot_table(
    index='invoice_date',
    values='total_sales',
    aggfunc='sum'
).rename(columns={'total_sales': 'Total_Sales'})

# Resample to daily bins for total sales
daily_sales = sales_by_date_pivot.resample('D').sum()

# Filter for women's athletic footwear
womens_footwear_data = combined_data[combined_data['product'] == "Women's Athletic Footwear"]
womens_footwear_sales_pivot = womens_footwear_data.pivot_table(
    index='invoice_date',
    values='total_sales',
    aggfunc='sum'
)

# Resample to daily bins for women's athletic footwear sales
daily_womens_footwear_sales = womens_footwear_sales_pivot.resample('D').sum()

# Sort the daily sales data for the top 10 days
top_10_days_womens_sales = daily_womens_footwear_sales.sort_values(by='total_sales', ascending=False).head(10)

# Resample to weekly bins for women's athletic footwear sales
weekly_womens_footwear_sales = womens_footwear_sales_pivot.resample('W').sum()

# Sort the weekly sales data for the top 10 weeks
top_10_weeks_womens_sales = weekly_womens_footwear_sales.sort_values(by='total_sales', ascending=False).head(10)

# Save the results to CSV files for submission
region_product_sales.to_csv('region_product_sales.csv', index=False)
region_total_sales.to_csv('region_total_sales.csv', index=False)
top_10_days_womens_sales.to_csv('top_10_days_womens_sales.csv', index=True)
top_10_weeks_womens_sales.to_csv('top_10_weeks_womens_sales.csv', index=True)
