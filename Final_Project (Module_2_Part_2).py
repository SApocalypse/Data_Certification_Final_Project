import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import io


# Function to fetch data from the given URL
def fetch_data(url):
    response = requests.get(url)
    response.raise_for_status()  # Ensure we raise an error for bad status codes
    return pd.read_csv(io.BytesIO(response.content))


# Main function to execute the data fetching and display
def main():
    URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv"
    df = fetch_data(URL)

    # Save a copy of the CSV file locally
    df.to_csv('dataset_part_2_copy.csv', index=False)
    print("CSV file saved as 'dataset_part_2_copy.csv'")

    print(df.head(5))

    # Plotting with seaborn catplot
    sns.set(style="whitegrid")
    cat_plot = sns.catplot(x="FlightNumber", y="LaunchSite", hue="Class", data=df, height=6, aspect=2, kind="strip")
    plt.title("Flight Number vs Launch Site")
    plt.show()

     # Plotting with seaborn catplot
    sns.set(style="whitegrid")
    cat_plot = sns.catplot(x="PayloadMass", y="LaunchSite", hue="Class", data=df, height=6, aspect=2, kind="strip")
    cat_plot.set_axis_labels("Payload Mass (kg)", "Launch Site")
    plt.title("PayLoad vs Launch Site")
    plt.show()

    # Group by 'Orbit' and calculate the average of 'Class'
    grouped_df = df.groupby('Orbit')['Class'].mean().reset_index()

    # Rename the columns for clarity
    grouped_df.columns = ['Orbit', 'Average Class']

    print(grouped_df)

    # Plotting with seaborn catplot
    sns.set(style="whitegrid")
    cat_plot = sns.catplot(x="FlightNumber", y="Orbit", hue="Class", data=df, height=6, aspect=2, kind="strip")
    cat_plot.set_axis_labels("Flight Number", "Orbit")
    plt.title("Flight Number and Orbit Type")
    plt.show()

    # Plotting with seaborn catplot
    sns.set(style="whitegrid")
    cat_plot = sns.catplot(x="PayloadMass", y="Orbit", hue="Class", data=df, height=6, aspect=2, kind="strip")
    cat_plot.set_axis_labels("Pay Load Mass (kg)", "Orbit")
    plt.title("Pay Load Mass (kg) and Orbit Type")
    plt.show()

    # Extract 'Year' from 'Date' column
    df['Year'] = pd.to_datetime(df['Date']).dt.year

    # Group by 'Year' and calculate the average of 'Class'
    grouped_df = df.groupby('Year')['Class'].mean().reset_index()

    # Rename the columns for clarity
    grouped_df.columns = ['Year', 'Success Rate']

    print(grouped_df)

    # Plotting the results
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=grouped_df, x='Year', y='Success Rate', marker='o')
    plt.xlabel('Year')
    plt.ylabel('Success Rate')
    plt.title('Success Rate Over Years')
    plt.grid(True)
    plt.savefig('Success_Rate_Over_Years.png')
    print("Plot saved as 'Success_Rate_Over_Years.png'")
    plt.show()

    features = df[
        ['FlightNumber', 'PayloadMass', 'Orbit', 'LaunchSite', 'Flights', 'GridFins', 'Reused', 'Legs', 'LandingPad',
         'Block', 'ReusedCount', 'Serial']]
    features.head()

    # Convert 'Date' column to datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # Convert 'Date' column to timestamps (seconds since the epoch)
    df['Date'] = df['Date'].astype('int64') // 10 ** 9

    # Apply one-hot encoding to the specified columns
    features_one_hot = pd.get_dummies(df, columns=['Orbit', 'LaunchSite', 'LandingPad', 'Serial', 'Outcome', 'BoosterVersion', 'GridFins', 'Reused', 'Legs'])

    # Cast all columns to 'float64'
    features_one_hot = features_one_hot.astype('float64')

    # Save the resulting DataFrame to a new CSV file
    features_one_hot.to_csv('dataset_part_3.csv', index=False)
    print("CSV file saved as 'dataset_part_3.csv'")
    
    # Display the result
    print("DataFrame with One-Hot Encoding Applied and All Columns Cast to float64:")
    print(features_one_hot.head(5))

# Run the main function
if __name__ == "__main__":
    main()

