import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd

# Static URL
static_url = "https://en.wikipedia.org/w/index.php?title=List_of_Falcon_9_and_Falcon_Heavy_launches&oldid=1027686922"

# Fetch HTML content using requests
try:
    response = requests.get(static_url)
    response.raise_for_status()  # Raise an HTTPError for bad responses
    html_content = response.text
except requests.exceptions.RequestException as e:
    print(f"Error fetching HTML content: {e}")
    exit(1)

# Create BeautifulSoup object
soup = BeautifulSoup(html_content, 'html.parser')

# Initialize launch_dict with empty lists for each desired column
launch_dict = {
    'Flight No': [],
    'Launch Site': [],
    'Payload': [],
    'Payload mass': [],
    'Orbit': [],
    'Customer': [],
    'Launch outcome': [],
    'Version Booster': [],
    'Booster landing': [],
    'Date': [],
    'Time': []
}

# Find tables 3 through 15 in the HTML
tables = soup.find_all('table')[2:15]  # Tables 3 to 15

# Iterate through tables and extract data
for table in tables:
    rows = table.find_all('tr')[1:]  # Skip header row
    for row in rows:
        columns = row.find_all(['th', 'td'])

        # Check if the row contains a single <td> with colspan="9"
        if len(columns) == 1 and 'colspan' in columns[0].attrs and columns[0]['colspan'] == '9':
            print(f"Skipping row with colspan: {columns[0].text.strip()}")
            continue

        if len(columns) >= 10:  # Ensure there are enough columns in the row
            # Extract column data
            flight_no = columns[0].text.strip()
            launch_site = columns[3].text.strip()
            payload = columns[4].text.strip()
            payload_mass = columns[5].text.strip()
            orbit = columns[6].text.strip()
            customer = columns[7].text.strip()
            launch_outcome = columns[8].text.strip()
            version_booster = columns[2].text.strip()
            booster_landing = columns[9].text.strip()
            date_time_utc = columns[1].text.strip()

            # Split date and time (UTC)
            if date_time_utc:
                try:
                    date_utc, time_utc = date_time_utc.split(' ')
                    # Format date as YYYY-MM-DD
                    date_obj = datetime.strptime(date_utc, '%d %B %Y').date()
                    date_str = date_obj.strftime('%Y-%m-%d')
                    launch_dict['Date'].append(date_str)
                    launch_dict['Time'].append(time_utc)
                except ValueError:
                    launch_dict['Date'].append(None)
                    launch_dict['Time'].append(None)

            # Append data to launch_dict
            launch_dict['Flight No'].append(flight_no)
            launch_dict['Launch Site'].append(launch_site)
            launch_dict['Payload'].append(payload)
            launch_dict['Payload mass'].append(payload_mass)
            launch_dict['Orbit'].append(orbit)
            launch_dict['Customer'].append(customer)
            launch_dict['Launch outcome'].append(launch_outcome)
            launch_dict['Version Booster'].append(version_booster)
            launch_dict['Booster landing'].append(booster_landing)
        else:
            print(f"Skipping row with insufficient columns: {[col.text.strip() for col in columns]}")

# Print the dictionary (for demonstration purposes)
print("Launch Dictionary:")
print(launch_dict)

# Create DataFrame from launch_dict
df = pd.DataFrame(launch_dict)

# Export DataFrame to CSV
csv_filename = 'spacex_web_scraped.csv'
df.to_csv(csv_filename, index=False)

print(f"DataFrame exported to {csv_filename}")
