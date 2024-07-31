import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import yaml

class RDSDatabaseConnector:
    def __init__(self, credentials):
        # Set up the connection string for the database
        db_string = f"postgresql://{credentials['user']}:{credentials['password']}@{credentials['host']}:{credentials['port']}/{credentials['dbname']}"
        self.engine = create_engine(db_string)
        print("Connected to the database successfully!")

    def fetch_data(self):
        # Fetch data from the customer_activity table
        return pd.read_sql("SELECT * FROM customer_activity", self.engine)

    def save_data(self, data_frame, filename='customer_activity.csv'):
        # Save the fetched data to a CSV file
        data_frame.to_csv(filename, index=False)
        print(f"Data saved to {filename}")

class DataFrameTransform:
    def __init__(self, dataframe):
        self.df = dataframe

    def count_null_values(self):
        # Returns a count of NULL values for each column
        return self.df.isnull().sum()

    def drop_columns(self, threshold=0.4):
        # Drops columns with missing values exceeding the threshold percentage
        initial_cols = len(self.df.columns)
        self.df.dropna(thresh=len(self.df) * (1 - threshold), axis=1, inplace=True)
        final_cols = len(self.df.columns)
        print(f"Dropped {initial_cols - final_cols} columns due to high null values.")

    def impute_with_median_mean(self, strategy='median'):
        # Imputes missing values using median or mean for numerical columns
        numerical_cols = self.df.select_dtypes(include=['float64', 'int64']).columns
        if strategy == 'median':
            for column in numerical_cols:
                self.df[column].fillna(self.df[column].median(), inplace=True)
        else:
            for column in numerical_cols:
                self.df[column].fillna(self.df[column].mean(), inplace=True)
        print(f"Missing values imputed with the {strategy}.")

class Plotter:
    def __init__(self, dataframe):
        self.df = dataframe

    def plot_null_values(self):
        # Generates a bar plot of the count of NULL values in each column
        null_data = self.df.isnull().sum()
        null_data = null_data[null_data > 0]
        null_data.sort_values(inplace=True)
        null_data.plot.bar(color='red')
        plt.title('Null Values Count per Column')
        plt.xlabel('Columns')
        plt.ylabel('Null Counts')
        plt.xticks(rotation=45)
        plt.show()

def load_credentials(file_path='credentials.yaml'):
    # Load database credentials from a YAML file
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

if __name__ == "__main__":
    creds = load_credentials()
    db_connector = RDSDatabaseConnector(creds)
    data = db_connector.fetch_data()

    # Initializing classes for transformation and plotting
    transformer = DataFrameTransform(data)
    plotter = Plotter(data)

    # Visualizing initial null values
    plotter.plot_null_values()

    # Data transformation steps
    transformer.drop_columns()
    transformer.impute_with_median_mean()

    # Re-check null values and visualize again
    print(transformer.count_null_values())
    plotter.plot_null_values()