import sys

import requests
from bs4 import BeautifulSoup
import re
import unicodedata
import pandas as pd


def date_time(table_cells):
    """
    This function returns the data and time from the HTML  table cell
    Input: the  element of a table data cell extracts extra row
    """
    return [data_time.strip() for data_time in list(table_cells.strings)][0:2]


def booster_version(table_cells):
    """
    This function returns the booster version from the HTML  table cell
    Input: the  element of a table data cell extracts extra row
    """
    out = ''.join([booster_version for i, booster_version in enumerate(table_cells.strings) if i % 2 == 0][0:-1])
    return out


def landing_status(table_cells):
    """
    This function returns the landing status from the HTML table cell
    Input: the  element of a table data cell extracts extra row
    """
    out = [i for i in table_cells.strings][0]
    return out


def get_mass(table_cells):
    mass = unicodedata.normalize("NFKD", table_cells.text).strip()
    if mass:
        mass.find("kg")
        new_mass = mass[0:mass.find("kg") + 2]
    else:
        new_mass = 0
    return new_mass


def extract_column_from_header(row):
    """
    This function returns the landing status from the HTML table cell
    Input: the  element of a table data cell extracts extra row
    """
    if (row.br):
        row.br.extract()
    if row.a:
        row.a.extract()
    if row.sup:
        row.sup.extract()

    colunm_name = ' '.join(row.contents)

    # Filter the digit and empty names
    if not (colunm_name.strip().isdigit()):
        colunm_name = colunm_name.strip()
        return colunm_name

static_url = "https://en.wikipedia.org/w/index.php?title=List_of_Falcon_9_and_Falcon_Heavy_launches&oldid=1027686922"

import requests
from bs4 import BeautifulSoup

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

# Now you can work with the BeautifulSoup object 'soup' to parse and extract data from the HTML
# For example, you can find all tables in the HTML
tables = soup.find_all('table')

# Print the number of tables found
print(f"Number of tables found: {len(tables)}")

# Example: Print the title of the Wikipedia page
title = soup.title
print(f"Title of the page: {title}")

# Find all table column names and store them in a list
table_column_names = []
for table in soup.find_all('table'):
    # Find all <th> elements within the <table>
    headers = table.find_all('th')
    column_names = [header.text.strip() for header in headers]
    table_column_names.append(column_names)

# Print the list of table column names
print("List of Table Column Names:")
for i, column_names in enumerate(table_column_names, start=1):
    print(f"Table {i} Column Names:")
    for name in column_names:
        print(name)
    print()


# Initialize an empty set to store unique column names
column_names = set()

# Find all tables in the HTML starting from the third table
tables = soup.find_all('table')[2:]  # Starting from index 2 (third table)

# Find column names in each table and store them in the set
for table in tables:
    # Find all <th> elements within the <table>
    headers = table.find_all('th')
    for header in headers:
        column_name = header.text.strip()
        # Check conditions: no duplicates, no numbered columns, and no 'Launch_dict'
        if column_name not in column_names and not column_name.isdigit() and 'Launch_dict' not in column_name:
            column_names.add(column_name)

# Convert set to sorted list for consistent output order
column_names = sorted(column_names)

# Print the list of filtered column names
print("List of filtered column names:")
for name in column_names:
    print(name)

# Define the desired columns
desired_columns = ['Flight No', 'Launch Site', 'Payload', 'Payload mass', 'Orbit',
                   'Customer', 'Launch outcome', 'Version Booster', 'Booster landing',
                   'Date', 'Time']

# Initialize an empty dictionary
launch_dict = {col: [] for col in desired_columns}

# Find all tables in the HTML starting from the third table
tables = soup.find_all('table')[2:]  # Starting from index 2 (third table)

# Extract data from each table row and populate the dictionary
for table in tables:
    rows = table.find_all('tr')
    for row in rows:
        columns = row.find_all(['th', 'td'])
        if columns:
            # Extract column names and data
            column_names = [col.text.strip() for col in columns if col.text.strip()]
            if 'Flight No' in column_names:
                # Populate dictionary based on desired columns
                for col in desired_columns:
                    if col in column_names:
                        index = column_names.index(col)
                        launch_dict[col].append(columns[index].text.strip())

# Print the dictionary (for demonstration purposes)
print("Launch Dictionary:")
print(launch_dict)

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
        if columns:
            # Extract column data
            flight_no = columns[0].text.strip()
            launch_site = columns[1].text.strip()
            payload = columns[2].text.strip()
            payload_mass = columns[3].text.strip()
            orbit = columns[4].text.strip()
            customer = columns[5].text.strip()
            launch_outcome = columns[6].text.strip()
            version_booster = columns[7].text.strip()
            booster_landing = columns[8].text.strip()
            date_time_utc = columns[9].text.strip()

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

# Print the dictionary (for demonstration purposes)
print("Launch Dictionary:")
print(launch_dict)