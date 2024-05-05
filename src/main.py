import os
import pandas as pd  # import matplotlib.pyplot as plt
import numpy as np  # numpy to to update the 'Amount' column based on the 'Transaction_Type'


os.getcwd() 

# Read the data file into a DataFrame
t_data_file_path = 'data/sources/transactions.csv'
c_data_file_path = 'data/sources/Chase8461_Activity20220106_20240108.CSV'

t_data = pd.read_csv(t_data_file_path)
c_data = pd.read_csv(c_data_file_path)

# Replace spaces with underscores in column names
t_data.columns = t_data.columns.str.replace(' ', '_')
c_data.columns = c_data.columns.str.replace(' ', '_')

# Convert all text data in the DataFrame to lowercase (done to help w matching rules)
t_data_text_columns = ['Description', 'Original_Description', 'Transaction_Type', 'Category', 'Account_Name', 'Notes']
t_data[t_data_text_columns] = t_data[t_data_text_columns].apply(lambda x: x.astype(str).str.lower())

c_data_text_columns = ['Description','Category','Type','Memo']
c_data[c_data_text_columns] = c_data[c_data_text_columns].apply(lambda x: x.astype(str).str.lower())

# Convert 'Date' column to datetime type with explicit format
t_data['Date'] = pd.to_datetime(t_data['Date'], format='%m/%d/%Y')
t_data['Post_Date'] = pd.to_datetime(t_data['Date'], format='%m/%d/%Y')
c_data['Transaction_Date'] = pd.to_datetime(c_data['Transaction_Date'], format='%m/%d/%Y')
c_data['Post_Date'] = pd.to_datetime(c_data['Post_Date'], format='%m/%d/%Y')

# Extract year and month from the 'Date' column
t_data['Year'] = t_data['Date'].dt.year
t_data['Month'] = t_data['Date'].dt.month
c_data['Year'] = c_data['Transaction_Date'].dt.year
c_data['Month'] = c_data['Transaction_Date'].dt.month

# Strip whitespace from all string columns
t_data = t_data.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

# Perform a string replace operation on the "ColumnName" column
t_data['Original_Description'] = t_data['Original_Description'].str.replace('pos purch - ', ' ')
t_data['Description'] = t_data['Original_Description'].str.replace('pos purch - ', ' ')

# # Verify the updated data type of the 'Date' column
# print("Data type of 'Date' column after conversion:", t_data['Date'].dtype)
# print("Data type of 'Date' column after conversion:", c_data['Transaction_Date'].dtype)
# print("Data type of 'Date' column after conversion:", c_data['Post_Date'].dtype)

# Add Label2 to capture more granular categories
c_data['Labels'] = ''
c_data['Account_Name'] = 'Chase - Credit Card'
c_data['Memo'] = ''

# Strip whitespace from all string columns
c_data = c_data.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

# Remove commas from the some text columns to help avoid loading issues in looker (if used)
t_data['Notes'] = t_data['Notes'].str.replace(',', '')
t_data['Description'] = t_data['Description'].str.replace(',', '')
# t_data['Original_Description'] = t_data['Original_Description'].str.replace(',', '')
t_data.drop(columns=['Original_Description'])

# Assuming t_data is your DataFrame
t_data['Amount'] = np.where(t_data['Transaction_Type'] == 'debit', -t_data['Amount'], t_data['Amount'])

print(t_data.head())
c_data.head()



