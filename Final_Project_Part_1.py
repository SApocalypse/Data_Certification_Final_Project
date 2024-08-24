import requests
import pandas as pd
import numpy as np
import datetime

pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)

# Initialize lists for storing data
BoosterVersion = []
LaunchSite = []
Longitude = []
Latitude = []
PayloadMass = []
Orbit = []
Block = []
ReusedCount = []
Serial = []
Outcome = []
Flights = []
GridFins = []
Reused = []
Legs = []
LandingPad = []

def getBoosterVersion(data):
    for x in data['rocket']:
        if x:
            response = requests.get(f"https://api.spacexdata.com/v4/rockets/{x}").json()
            BoosterVersion.append(response['name'])

def getLaunchSite(data):
    for x in data['launchpad']:
        if x:
            response = requests.get(f"https://api.spacexdata.com/v4/launchpads/{x}").json()
            Longitude.append(response['longitude'])
            Latitude.append(response['latitude'])
            LaunchSite.append(response['name'])

def getPayloadData(data):
    for load in data['payloads']:
        if load:
            response = requests.get(f"https://api.spacexdata.com/v4/payloads/{load}").json()
            PayloadMass.append(response['mass_kg'])
            Orbit.append(response['orbit'])

def getCoreData(data):
    for core in data['cores']:
        if core['core'] is not None:
            response = requests.get(f"https://api.spacexdata.com/v4/cores/{core['core']}").json()
            Block.append(response.get('block'))
            ReusedCount.append(response.get('reuse_count'))
            Serial.append(response.get('serial'))
        else:
            Block.append(None)
            ReusedCount.append(None)
            Serial.append(None)
        Outcome.append(f"{core['landing_success']} {core['landing_type']}")
        Flights.append(core['flight'])
        GridFins.append(core['gridfins'])
        Reused.append(core['reused'])
        Legs.append(core['legs'])
        LandingPad.append(core['landpad'])

# URL for the static JSON file
static_json_url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/API_call_spacex_api.json'

# Fetching the data from the static JSON URL
try:
    response = requests.get(static_json_url)
    response.raise_for_status()  # Raise an HTTPError for bad responses
    data_json = response.json()
except requests.exceptions.RequestException as e:
    print(f"Error fetching data: {e}")
    exit(1)

# Normalize JSON data into a flat DataFrame
try:
    data = pd.json_normalize(data_json)
except Exception as e:
    print(f"Error normalizing JSON: {e}")
    exit(1)

# Select the desired columns
try:
    data = data[['rocket', 'payloads', 'launchpad', 'cores', 'flight_number', 'date_utc']]
except KeyError as e:
    print(f"Error selecting columns: {e}")
    exit(1)

# Filter rows with a single core and a single payload
try:
    data = data[data['cores'].map(len) == 1]
    data = data[data['payloads'].map(len) == 1]
except Exception as e:
    print(f"Error filtering rows: {e}")
    exit(1)

# Extract the single value in the lists for 'cores' and 'payloads'
try:
    data['cores'] = data['cores'].map(lambda x: x[0])
    data['payloads'] = data['payloads'].map(lambda x: x[0])
except Exception as e:
    print(f"Error mapping lists: {e}")
    exit(1)

# Convert 'date_utc' to datetime and extract the date
try:
    data['date'] = pd.to_datetime(data['date_utc']).dt.date
except Exception as e:
    print(f"Error converting date: {e}")
    exit(1)

# Filter the DataFrame by date
try:
    data = data[data['date'] <= datetime.date(2020, 11, 13)]
except Exception as e:
    print(f"Error filtering by date: {e}")
    exit(1)

# Fetch additional data from SpaceX API and update the DataFrame
getBoosterVersion(data)
getLaunchSite(data)
getPayloadData(data)
getCoreData(data)

# Add the new columns to the DataFrame
data['BoosterVersion'] = BoosterVersion
data['LaunchSite'] = LaunchSite
data['Longitude'] = Longitude
data['Latitude'] = Latitude
data['PayloadMass'] = PayloadMass
data['Orbit'] = Orbit
data['Block'] = Block
data['ReusedCount'] = ReusedCount
data['Serial'] = Serial
data['Outcome'] = Outcome
data['Flights'] = Flights
data['GridFins'] = GridFins
data['Reused'] = Reused
data['Legs'] = Legs
data['LandingPad'] = LandingPad

# Filter rows with 'Falcon 9' in BoosterVersion
data = data[data['BoosterVersion'] == 'Falcon 9']

# Reset flight numbers starting from 1
data['flight_number'] = range(1, len(data) + 1)

# Calculate the average of PayloadMass
average_payload_mass = data['PayloadMass'].mean()

# Replace NaN values in PayloadMass with the calculated average
data['PayloadMass'].fillna(average_payload_mass, inplace=True)

# Export the DataFrame to CSV
data.to_csv('dataset_part_1.csv', index=False)

# Final check of the resulting DataFrame
print("Final DataFrame:")
print(data.head())
