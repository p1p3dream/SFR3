import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = 'path_to_your_json_file'  # Replace with your file path
df = pd.read_json(file_path)

# Convert UNIX timestamp columns to datetime
df['payment_date'] = pd.to_datetime(df['payment_date'], unit='ms')
df['lease_start_date'] = pd.to_datetime(df['lease_start_date'], unit='ms')
df['lease_end_date'] = pd.to_datetime(df['lease_end_date'], unit='ms')

# Analysis 1: Rent Collection Efficiency
# Adding a column for the month and year of payment
df['payment_month_year'] = df['payment_date'].dt.to_period('M')

# Calculating the late payment frequency by month
late_payments_by_month = df.groupby('payment_month_year')['late_payment'].sum()

# Visualization 1: Late Payment Trends Over Time
plt.figure(figsize=(12, 6))
late_payments_by_month.plot(kind='line', color='blue', marker='o')
plt.title('Late Payment Trends Over Time')
plt.xlabel('Month and Year')
plt.ylabel('Number of Late Payments')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()

# Analysis 2: Insights from Tenant Screening Data
# Scatter plot of Screening Score vs Late Payments
plt.figure(figsize=(12, 6))
sns.scatterplot(data=df, x='screening_score', y='late_payment', alpha=0.6)
plt.title('Screening Score vs Late Payment')
plt.xlabel('Screening Score')
plt.ylabel('Late Payment (1 for Late, 0 for On-Time)')
plt.grid(True)
plt.tight_layout()

# Analysis 3: Lease Signing Trends
# Counting the number of leases started each month
df['lease_start_month_year'] = df['lease_start_date'].dt.to_period('M')
lease_starts_by_month = df.groupby('lease_start_month_year').size()

# Visualization 2: Lease Signing Trends Over Time
plt.figure(figsize=(12, 6))
lease_starts_by_month.plot(kind='bar', color='green')
plt.title('Lease Signing Trends Over Time')
plt.xlabel('Month and Year')
plt.ylabel('Number of Lease Starts')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()

plt.show()
