import folium
import pandas as pd
import requests
import io
from folium.features import DivIcon
from folium.plugins import MarkerCluster
import numpy as np

# Function to fetch data from the given URL
def fetch_data(url):
    response = requests.get(url)
    response.raise_for_status()  # Ensure we raise an error for bad status codes
    return pd.read_csv(io.BytesIO(response.content))

# Main function to execute the data fetching and display
def main():
    URL = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_geo.csv'
    df = fetch_data(URL)

    # Save a copy of the CSV file locally
    df.to_csv('spacex_launch_geo.csv', index=False)
    print("CSV file saved as 'spacex_launch_geo.csv'")

    print(df.head(5))

    # Start location is NASA Johnson Space Center
    nasa_coordinate = [29.559684888503615, -95.0830971930759]
    site_map = folium.Map(location=nasa_coordinate, zoom_start=5)

    # Create a marker cluster
    marker_cluster = MarkerCluster().add_to(site_map)

    # Iterate through each row in the dataframe and create a Marker
    for index, row in df.iterrows():
        lat = row['Lat'] + np.random.uniform(-0.001, 0.001)  # Add a small random offset to lat
        long = row['Long'] + np.random.uniform(-0.001, 0.001)  # Add a small random offset to long
        flight_number = row['Flight Number']
        flight_class = row['class']

        # Determine the marker color based on the class
        color = 'green' if flight_class == 1 else 'red'

        # Create a marker at the given coordinate with a popup showing the flight number
        marker = folium.Marker(
            location=[lat, long],
            popup=folium.Popup(flight_number, parse_html=True),
            icon=DivIcon(
                icon_size=(10, 10),  # Make the icon size smaller
                icon_anchor=(-3, -3),  # Adjust anchor to move text closer to the GPS location
                html=f'<div style="font-size: 10px; color:{color};"><b>{flight_number}</b></div>',
            )
        )

        # Add the marker to the marker cluster
        marker_cluster.add_child(marker)

    # Save the map to an HTML file
    site_map.save("spacex_launch_sites_map.html")
    print("Map saved as 'spacex_launch_sites_map.html'")

if __name__ == "__main__":
    main()
