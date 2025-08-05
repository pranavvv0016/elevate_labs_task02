import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys

file_path = 'superstore.csv'

try:
    df = pd.read_csv(file_path, encoding='ISO-8859-1', sep=',')
except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found.")
    print(f"Please make sure '{file_path}' is in the same folder as this script.")
    sys.exit()
except Exception as e:
    print(f"An error occurred while reading the file: {e}")
    sys.exit()

df['Order.Date'] = pd.to_datetime(df['Order.Date'])
df['Profit Margin'] = (df['Profit'] / df['Sales']) * 100

print("Data loaded and preprocessed successfully.")
print(f"Dataset contains {df.shape[0]} rows and {df.shape[1]} columns.")
print("\n--- High-Level Business Overview ---")

total_sales = df['Sales'].sum()
total_profit = df['Profit'].sum()
overall_profit_margin = (total_profit / total_sales) * 100

print(f"Total Sales: ${total_sales:,.2f}")
print(f"Total Profit: ${total_profit:,.2f}")
print(f"Overall Profit Margin: {overall_profit_margin:.2f}%")

sns.set_style('whitegrid')

print("\nGenerating Chart 1: Sales and Profit Over Time...")
df_time = df.set_index('Order.Date').resample('M')[['Sales', 'Profit']].sum().reset_index()

plt.figure(figsize=(14, 7))
plt.plot(df_time['Order.Date'], df_time['Sales'], label='Sales', color='royalblue')
plt.plot(df_time['Order.Date'], df_time['Profit'], label='Profit', color='seagreen', linestyle='--')
plt.title('Monthly Sales and Profit Over Time', fontsize=16)
plt.xlabel('Year')
plt.ylabel('Amount (USD)')
plt.legend()
plt.grid(True)
plt.savefig('sales_profit_over_time.png', bbox_inches='tight')
print("Chart 1 saved as sales_profit_over_time.png")

print("\nGenerating Chart 2: Profitability by State...")
state_profit = df.groupby('State')['Profit'].sum().sort_values()
colors = ['crimson' if x < 0 else 'forestgreen' for x in state_profit]

plt.figure(figsize=(12, 10))
state_profit.plot(kind='barh', color=colors)
plt.title('Total Profit by State', fontsize=16)
plt.xlabel('Total Profit (USD)')
plt.ylabel('State')
plt.savefig('profit_by_state.png', bbox_inches='tight')
print("Chart 2 saved as profit_by_state.png")

print("\nGenerating Chart 3: Sales by Product Category...")
category_sales = df.groupby('Category')['Sales'].sum().sort_values(ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(x=category_sales.index, y=category_sales.values, palette='viridis')
plt.title('Total Sales by Product Category', fontsize=16)
plt.xlabel('Category')
plt.ylabel('Total Sales (USD)')
plt.savefig('sales_by_category.png', bbox_inches='tight')
print("Chart 3 saved as sales_by_category.png")

print("\nGenerating Chart 4: Sub-Category Sales vs. Profit Margin...")
subcategory_performance = df.groupby('Sub.Category').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
subcategory_performance['Profit Margin'] = (subcategory_performance['Profit'] / subcategory_performance['Sales']) * 100

plt.figure(figsize=(14, 8))
sns.scatterplot(data=subcategory_performance, x='Sales', y='Profit Margin', size='Sales', hue='Profit Margin',
                sizes=(50, 2000), palette='coolwarm', legend=False)
plt.title('Sub-Category Performance: Sales vs. Profit Margin', fontsize=16)
plt.xlabel('Total Sales (USD)')
plt.ylabel('Profit Margin (%)')
plt.axhline(0, color='red', linestyle='--', linewidth=1)

for i in range(subcategory_performance.shape[0]):
    item = subcategory_performance.iloc[i]
    if item['Profit Margin'] < 0 or item['Sales'] > 250000:
        plt.text(item['Sales'], item['Profit Margin'] + 2, item['Sub.Category'], fontsize=9)

plt.savefig('subcategory_performance.png', bbox_inches='tight')
print("Chart 4 saved as subcategory_performance.png")

print("\nAll visualizations have been created and saved.")