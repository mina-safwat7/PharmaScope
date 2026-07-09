import pandas as pd
from faker import Faker
import random
from datetime import timedelta
import uuid

fake = Faker()  

drugs_df = pd.read_csv(r"E:\Python\Depi\medicines_data_updated.csv\medicines_data_updated.csv")  

categories = ["Antibiotic", "Antifungal", "Antiviral", "Painkiller", "Vitamin"]
drugs_by_category = {cat: drugs_df[drugs_df['Category'] == cat]['Drugname'].tolist() 
                     for cat in categories}

age_distribution = {
    (0, 18): 0.15,
    (19, 40): 0.25,
    (41, 65): 0.35,
    (66, 90): 0.25
}
age_ranges = list(age_distribution.keys())
weights = list(age_distribution.values())

drug_categories_by_age = {
    (0, 18): ["Vitamin", "Antibiotic", "Painkiller"],
    (19, 40): ["Vitamin", "Painkiller", "Antibiotic", "Antiviral"],
    (41, 65): ["Painkiller", "Antiviral", "Antibiotic"],
    (66, 90): ["Painkiller", "Antiviral", "Vitamin"]
}

num_patients = 10000
patients = []

for pid in range(1, num_patients + 1):
    age_range = random.choices(age_ranges, weights=weights, k=1)[0]
    age = random.randint(age_range[0], age_range[1])
    
    city = fake.city()
    state = fake.state()
    
    drug_cat = random.choice(drug_categories_by_age[age_range])
    
    drug_name = random.choice(drugs_by_category.get(drug_cat, ["Unknown Drug"]))
    
    drug_row = drugs_df[drugs_df['Drugname'] == drug_name].iloc[0] if drug_name in drugs_df['Drugname'].values else pd.Series({
        'Price': None, 'Form': None, 'Company': None, 'Category': drug_cat
    })
    
    start_date = fake.date_between(start_date='-1y', end_date='today')
    duration_days = random.randint(3, 30)
    end_date = start_date + timedelta(days=duration_days)
    
    freq_per_day = random.randint(1, 3)
    quantity = freq_per_day * duration_days
    
    patient = {
        "Patient_ID": str(uuid.uuid4()),
        "Name": fake.name(),
        "Age": age,
        "City": city,
        "State": state,
        "Drugname": drug_name,
        "Price": drug_row.get('Price', None),
        "Form": drug_row.get('Form', None),
        "Company": drug_row.get('Company', None),
        "Category": drug_row.get('Category', drug_cat),
        "Start_Date": start_date,
        "End_Date": end_date,
        "Frequency_per_day": freq_per_day,
        "Quantity": quantity
    }
    
    patients.append(patient)

df = pd.DataFrame(patients)
df.to_csv("patients_with_city_state.csv", index=False)
