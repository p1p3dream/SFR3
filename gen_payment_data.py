import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

# Initialize Faker and Random Seed
fake = Faker()
random.seed(0)

# Function to create a single tenant record
def create_tenant_record():
    tenant_name = fake.name()
    rent_amount = round(random.uniform(500.0, 3000.0), 2)
    payment_date = fake.date_between(start_date='-2y', end_date='today')
    screening_score = random.randint(300, 850)
    lease_start_date = payment_date - timedelta(days=random.randint(1, 5))
    lease_end_date = lease_start_date + timedelta(days=365)
    late_payment_count = 0
    for _ in range(12):  # Assuming monthly payments
        payment_date = fake.date_between(start_date=lease_start_date, end_date=lease_end_date)
        if payment_date.day > 5:  # Payment is late if after the 5th of the month
            late_payment_count += 1

    return {
        'tenant_name': tenant_name,
        'rent_amount': rent_amount,
        'payment_date': payment_date,
        'screening_score': screening_score,
        'lease_start_date': lease_start_date,
        'lease_end_date': lease_end_date,
        'late_payment_count': late_payment_count
    }

# Generate dataset
num_records = 10000  # Number of records you want to generate
data = [create_tenant_record() for _ in range(num_records)]
df = pd.DataFrame(data)

df.sort_values(by='tenant_name', ascending=True)
