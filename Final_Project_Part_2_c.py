import pandas as pd
import numpy as np

df=pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_1.csv")
print (df.head(10))

# Assuming df is your DataFrame
def missing_values_info(df):
    # Calculate the percentage of missing values for each attribute
    missing_percentage = df.isnull().mean() * 100

    # Identify the column type for each attribute
    column_types = df.dtypes

    # Create a DataFrame with the results
    missing_info = pd.DataFrame({
        'Missing Percentage': missing_percentage,
        'Column Type': column_types
    })

    return missing_info

print(missing_values_info(df))

outcome_counts = df ['Outcome'].value_counts()
print (outcome_counts)

launchsite_counts = df['LaunchSite'].value_counts()
print(launchsite_counts)

orbit_counts = df['Orbit'].value_counts()
print(orbit_counts)

landing_outcomes = df['Outcome'].value_counts()
print(landing_outcomes)

outcome_per_orbit = df.groupby(['Orbit', 'Outcome']).size().reset_index(name='Count')
print(outcome_per_orbit)


# Derive Landing_Class from Outcome
df['Landing_Class'] = df['Outcome'].apply(lambda x: 1 if x.startswith('True') else 0)

# Calculate the percentage of 1s in Landing_Class
count_1 = df['Landing_Class'].sum()
total_count = len(df['Landing_Class'])
percentage_1 = (count_1 / total_count) * 100

# Print the percentage of the occurrence of 1
print(f'The percentage of 1s in Landing_Class is: {percentage_1:.2f}%')

# Save the resulting DataFrame to a CSV file
df.to_csv('dataset_part_2.csv', index=False)