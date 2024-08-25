import os
import pandas as pd
from standardize import standardize_dataframe  # Import the function
from classify import *  # Import the function
from generator import *  # Import the function


# Path relative to the script's location
# folder_path = os.path.join(os.path.dirname(__file__), 'data')
folder_path = 'data/sources'

# Initialize an empty list to store DataFrames
dataframes = []

# List all CSV files in the folder
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# Mappings from source columns to standard columns
file_mappings = {
    'amex.csv': {
        "Date": "Date", 
        "Description": "Description", 
        "Original Description": None, 
        "Amount": "Amount", 
        "Transaction Type": None, 
        "Category": None, 
        "Account Name": None, 
        "Labels": None, 
        "Notes": None
    },
    'alecu_save.csv': {
        "Date": "Date", 
        "Description": "Description", 
        "Original Description": None, 
        "Amount": "Credit", 
        "Transaction Type": "Type", 
        "Category": None, 
        "Account Name": None, 
        "Labels": None, 
        "Notes": None
    },
    'alecu_check.csv': {
        "Date": "Date", 
        "Description": "Description", 
        "Original Description": None, 
        "Amount": "Debit", 
        "Transaction Type": "Type", 
        "Category": None, 
        "Account Name": None, 
        "Labels": None, 
        "Notes": None
    },
    'chase.csv': {
        "Date": "Transaction Date", 
        "Description": "Description", 
        "Original Description": None, 
        "Amount": "Amount", 
        "Transaction Type": "Type", 
        "Category": "Category", 
        "Account Name": None, 
        "Labels": None, 
        "Notes": "Memo"
    },
    'mint.csv': {
        "Date": "Date", 
        "Description": "Description", 
        "Original Description": "Original Description", 
        "Amount": "Amount", 
        "Transaction Type": "Transaction Type", 
        "Category": "Category", 
        "Account Name": "Account Name", 
        "Labels": "Labels", 
        "Notes": "Notes"
    }
}

# Standardize and store each DataFrame
for file in csv_files:
    file_path = os.path.join(folder_path, file)
    df = pd.read_csv(file_path)
    
    # Get the mapping for the current file
    mappings = file_mappings.get(file, {})
    standardized_df = standardize_dataframe(df, file, mappings)
    
    dataframes.append(standardized_df)

# Combine all standardized DataFrames into one
standard_df = pd.concat(dataframes, ignore_index=True)

# Sort the final DataFrame by date
standard_df = standard_df.sort_values(by='Date')


# Recategorize
standard_df['Category'] = standard_df.apply(recategorize_transactions, axis=1)

# Label Subscriptions
standard_df['Labels'] = standard_df.apply(label_subscriptions, axis=1)

# Label Outliers
standard_df['outliers'] = standard_df.apply(label_outliers, axis=1)

# # Write final_df to a CSV file
# standard_df.to_csv('data/output/standard_df.csv', index=False)
# print("The DataFrame has been successfully written to 'standard_df.csv'.")

# Call the function to write the DataFrame to a CSV file
write_dataframe_to_csv(standard_df)

recent_month(standard_df)
