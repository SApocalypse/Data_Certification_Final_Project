import csv
import sqlite3
import pandas as pd
import requests

# URL of the CSV file
csv_url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_2/data/Spacex.csv"
csv_filename = "Spacex.csv"

# Download the CSV file
response = requests.get(csv_url)
with open(csv_filename, 'wb') as file:
    file.write(response.content)

# Connect to SQLite database
con = sqlite3.connect("my_data1.db")
cur = con.cursor()

# Load the CSV data into a pandas DataFrame
df = pd.read_csv(csv_filename)

# Save the DataFrame to the SQLite database as the table SPACEXTBL
df.to_sql("SPACEXTBL", con, if_exists='replace', index=False, method="multi")

# Drop SPACEXTABLE if it exists to avoid errors
cur.execute("DROP TABLE IF EXISTS SPACEXTABLE")

# Create the new table SPACEXTABLE with non-null Date entries
cur.execute("""
CREATE TABLE SPACEXTABLE AS 
SELECT * FROM SPACEXTBL 
WHERE Date IS NOT NULL
""")
con.commit()

# Verify the contents of SPACEXTABLE
result = cur.execute("SELECT * FROM SPACEXTABLE LIMIT 5").fetchall()
for row in result:
    print(row)

# Query to get the unique names of all rows under 'Launch_Site'
unique_launch_sites = cur.execute("SELECT DISTINCT Launch_Site FROM SPACEXTABLE").fetchall()

# Print the unique launch sites
print("Unique Launch Sites:")
for site in unique_launch_sites:
    print(site[0])

# Query to get the first 5 records where the launch site begins with 'CCA'
cca_launch_sites = cur.execute("SELECT * FROM SPACEXTABLE WHERE Launch_Site LIKE 'CCA%' LIMIT 5").fetchall()

# Print the first 5 records where the launch site begins with 'CCA'
print("First 5 records where Launch Site begins with 'CCA':")
for record in cca_launch_sites:
    print(record)

# Query to sum all values under 'PAYLOAD_MASS__KG_' that are labeled as 'NASA (CRS)' under 'Customer'
total_payload_mass_nasa_crs = cur.execute("SELECT SUM(PAYLOAD_MASS__KG_) AS Total_Payload_Mass FROM SPACEXTABLE WHERE Customer = 'NASA (CRS)'").fetchone()

# Print the total payload mass for 'NASA (CRS)'
print("Total Payload Mass for 'NASA (CRS)':", total_payload_mass_nasa_crs[0])

# Query to get the average values from 'PAYLOAD_MASS__KG_' for all rows with 'F9 v1.1' under 'Booster_Version'
average_payload_mass_f9v1_1 = cur.execute("SELECT AVG(PAYLOAD_MASS__KG_) AS Average_Payload_Mass FROM SPACEXTABLE WHERE Booster_Version = 'F9 v1.1'").fetchone()

# Print the average payload mass for 'F9 v1.1'
print("Average Payload Mass for 'F9 v1.1':", average_payload_mass_f9v1_1[0])

# Query to identify the minimum value from 'Date' with 'Landing_Outcome' starting with 'Success'
earliest_successful_landing_date = cur.execute("SELECT MIN(Date) AS Earliest_Successful_Landing_Date FROM SPACEXTABLE WHERE Landing_Outcome LIKE 'Success%'").fetchone()

# Print the earliest successful landing date
print("Earliest Successful Landing Date:", earliest_successful_landing_date[0])

# Query to identify all unique values under 'Booster_Version' with 'PAYLOAD_MASS__KG_' between 4000 and 6000
# and 'Landing_Outcome' labeled as 'Success (drone ship)'
unique_booster_versions = cur.execute("""
SELECT DISTINCT Booster_Version
FROM SPACEXTABLE
WHERE PAYLOAD_MASS__KG_ BETWEEN 4000 AND 6000
  AND Landing_Outcome = 'Success (drone ship)'
""").fetchall()

# Print the unique booster versions
print("Unique Booster Versions with PAYLOAD_MASS_KG between 4000 and 6000 and Landing_Outcome 'Success (drone ship)':")
for booster in unique_booster_versions:
    print(booster[0])

# Query to count total number of entries starting with 'Success' and 'Failure' under 'Landing_Outcome'
landing_outcome_counts = cur.execute("""
SELECT 
    SUM(CASE WHEN Landing_Outcome LIKE 'Success%' THEN 1 ELSE 0 END) AS Total_Success,
    SUM(CASE WHEN Landing_Outcome LIKE 'Failure%' THEN 1 ELSE 0 END) AS Total_Failure
FROM SPACEXTABLE
""").fetchone()

# Print the counts of 'Success' and 'Failure' landing outcomes
print("Total 'Success' Landing Outcomes:", landing_outcome_counts[0])
print("Total 'Failure' Landing Outcomes:", landing_outcome_counts[1])

# Query to identify the maximum value from 'PAYLOAD_MASS__KG_' for each unique value in 'Booster_Version'
# and display the values in descending order
max_payload_per_booster = cur.execute("""
SELECT Booster_Version, MAX(PAYLOAD_MASS__KG_) AS Max_Payload_Mass
FROM SPACEXTABLE
GROUP BY Booster_Version
ORDER BY Max_Payload_Mass DESC
""").fetchall()

# Print the maximum payload mass for each booster version
print("Maximum Payload Mass for each Booster Version (in descending order):")
for record in max_payload_per_booster:
    print(f"Booster Version: {record[0]}, Max Payload Mass: {record[1]}")

    # Query to display the name of the month (derived from 'Date') for all rows with 'Failure (drone ship)'
    # under 'Landing_Outcome', including 'Booster_Version' and 'Launch_Site', and limit to year 2015
failure_drone_ship_2015 = cur.execute("""
 SELECT 
     STRFTIME('%m', Date) AS Month,
     Booster_Version,
     Launch_Site
 FROM SPACEXTABLE
 WHERE Landing_Outcome = 'Failure (drone ship)'
   AND STRFTIME('%Y', Date) = '2015'
 """).fetchall()

# Print the results
print("Failures (drone ship) in 2015:")
for record in failure_drone_ship_2015:
    print(f"Month: {record[0]}, Booster Version: {record[1]}, Launch Site: {record[2]}")

# Query to count and rank in descending order all unique values under 'Landing_Outcome'
# between '2010-06-04' and '2017-03-20'
landing_outcome_rank = cur.execute("""
SELECT 
    Landing_Outcome, 
    COUNT(*) AS Outcome_Count
FROM SPACEXTABLE
WHERE Date BETWEEN '2010-06-04' AND '2017-03-20'
GROUP BY Landing_Outcome
ORDER BY Outcome_Count DESC
""").fetchall()

# Print the counts and ranks of 'Landing_Outcome'
print("Counts and Ranks of Landing Outcomes between 2010-06-04 and 2017-03-20:")
for record in landing_outcome_rank:
    print(f"Landing Outcome: {record[0]}, Count: {record[1]}")

# Close the connection
con.close()


