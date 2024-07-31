import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data from a CSV file into a DataFrame
df = pd.read_csv('path_to_your_data.csv')

# Define a function to plot bar charts easily
def plot_bar(data, title, xlabel, ylabel):
    data.plot(kind='bar')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

# Define a function to plot pie charts easily
def plot_pie(data, title):
    data.plot(kind='pie', autopct='%1.1f%%')
    plt.title(title)
    plt.ylabel('')
    plt.show()

# Milestone 1: Familiarize with the data
print("Data Shape:", df.shape)
print("Data Columns:", df.columns)
print("Sample Data:\n", df.head())

# Task 1: Convert columns to the correct format
# Assuming 'month' is in string format and needs to be converted to categorical
df['month'] = pd.Categorical(df['month'], categories=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], ordered=True)

# Task 2: Create a class to get information from the DataFrame
class DataFrameInfo:
    def __init__(self, dataframe):
        self.df = dataframe
    
    def describe_columns(self):
        print("DataFrame Description:\n", self.df.describe(include='all'))
    
    def count_nulls(self):
        null_counts = self.df.isnull().sum()
        print("Null Value Counts:\n", null_counts)

# Create an instance of the class and use its methods
df_info = DataFrameInfo(df)
df_info.describe_columns()
df_info.count_nulls()

# Task 3: Remove/impute missing values in the data
df.fillna(df.median(), inplace=True)  # Simple imputation strategy

# Task 4: Perform transformations on skewed columns
skewed_cols = df.select_dtypes(include=['float64', 'int64']).skew().abs()
skewed_cols = skewed_cols[skewed_cols > 0.5].index
df[skewed_cols] = df[skewed_cols].apply(lambda x: np.log1p(x))

# Milestone 2: Determine software customer use to access the website
os_usage = df['operating_system'].value_counts(normalize=True) * 100
plot_bar(os_usage, 'Operating System Usage', 'Operating System', 'Percentage (%)')

device_usage = df['device_type'].value_counts(normalize=True) * 100
plot_pie(device_usage, 'Device Type Usage')

# Browser usage by device type
mobile_browsers = df[df['device_type'] == 'Mobile']['browser'].value_counts(normalize=True) * 100
desktop_browsers = df[df['device_type'] == 'Desktop']['browser'].value_counts(normalize=True) * 100

plt.figure(figsize=(14, 6))
plt.subplot(1, 2, 1)
plot_bar(mobile_browsers, 'Mobile Browser Usage', 'Browser', 'Percentage (%)')
plt.subplot(1, 2, 2)
plot_bar(desktop_browsers, 'Desktop Browser Usage', 'Browser', 'Percentage (%)')

# Milestone 3: Effective marketing
revenue_by_source = df.groupby('traffic_source')['revenue'].sum()
plot_bar(revenue_by_source, 'Revenue by Traffic Source', 'Traffic Source', 'Revenue ($)')

bounce_rate_by_source = df.groupby('traffic_source')['bounce_rate'].mean()
plot_bar(bounce_rate_by_source, 'Bounce Rate by Traffic Source', 'Traffic Source', 'Bounce Rate (%)')

# Milestone 4: Revenue analysis
revenue_by_region = df.groupby('region')['revenue'].sum()
plot_bar(revenue_by_region, 'Revenue by Region', 'Region', 'Revenue ($)')

customer_revenue = df.groupby('customer_type')['revenue'].sum()
plot_pie(customer_revenue, 'Revenue: New vs Returning Customers')

weekday_revenue = df.groupby('day_of_week')['revenue'].sum()
plot_bar(weekday_revenue, 'Revenue by Day of the Week', 'Day of Week', 'Revenue ($)')

month_revenue = df.groupby('month')['revenue'].sum()
plot_bar(month_revenue, 'Revenue by Month', 'Month', 'Revenue ($)')

traffic_type_revenue = df.groupby('traffic_type')['revenue'].sum()
plot_bar(traffic_type_revenue, 'Revenue by Traffic Type', 'Traffic Type', 'Revenue ($)')

