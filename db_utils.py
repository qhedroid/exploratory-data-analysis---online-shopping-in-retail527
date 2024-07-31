import pandas as pd
from sqlalchemy import create_engine
import yaml

class RDSDatabaseConnector:
    def __init__(self, credentials):
        # Setting up the connection string for the database
        db_string = f"postgresql://{credentials['user']}:{credentials['password']}@{credentials['host']}:{credentials['port']}/{credentials['dbname']}"
        self.engine = create_engine(db_string)
        print("Connected to the database successfully!")

    def fetch_data(self):
        # Fetching data from the customer_activity table
        return pd.read_sql("SELECT * FROM customer_activity", self.engine)

    def save_data(self, data_frame, filename='customer_activity.csv'):
        # Saving the fetched data to a CSV file
        data_frame.to_csv(filename, index=False)
        print(f"Data saved to {filename}")

def load_credentials(file_path='credentials.yaml'):
    # Loading database credentials from a YAML file
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)['database_credentials']

if __name__ == "__main__":
    creds = load_credentials()
    db_connector = RDSDatabaseConnector(creds)
    data = db_connector.fetch_data()
    db_connector.save_data(data)