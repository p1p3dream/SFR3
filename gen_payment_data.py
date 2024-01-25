import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

pd.set_option('display.max_rows', None)

# Initialize Faker and Random Seed
fake = Faker()
random.seed(0)

# Function to calculate the probability of late payment based on screening score
def late_payment_probability(screening_score):
    #higher screening scores lead to lower probability of late payment
    return max(0, 1 - (screening_score - 300) / 550)

# Function to create monthly payment records for a single tenant
def create_monthly_payments():
    tenant_name = fake.name()
    rent_amount = round(random.uniform(500.0, 3000.0), 2)
    screening_score = random.randint(300, 850)
    
    # Generate a random lease start date on the first day of a month within the past 2 years
    lease_start_date = fake.date_between_dates(date_start=datetime(2019, 1, 1), date_end=datetime.today().replace(day=1))
    
    lease_end_date = lease_start_date + timedelta(days=365)

    payments = []
    payment_date = lease_start_date
    while payment_date <= lease_end_date:
        # Calculate the probability of late payment based on screening score
        probability = late_payment_probability(screening_score)
        
        # Ensure late_payment is False 90% of the time
        late_payment = random.choices([True, False], weights=[probability, 9 - probability])[0]
        
        payments.append({
            'tenant_name': tenant_name,
            'rent_amount': rent_amount,
            'payment_date': payment_date,
            'screening_score': screening_score,
            'lease_start_date': lease_start_date,
            'lease_end_date': lease_end_date,
            'late_payment': late_payment
        })
        payment_date += timedelta(days=30)  # Approximation of a month

    return payments

# Generate dataset
num_tenants = 1000
data = []
for _ in range(num_tenants):
    data.extend(create_monthly_payments())
df = pd.DataFrame(data)
df
