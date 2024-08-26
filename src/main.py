import os
import pandas as pd
from standardize import *  # Import the function
from classify import *  # Import the function
from output import *  # Import the function


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
        "Category": None, 
        "Account Name": None, 
        "Transaction Type": None, 
        "Credit": None, 
        "Debit": None, 
        "Labels": None, 
        "Notes": None,
        "Balance": None
    },
    'alecu_save.csv': {
        "Date": "Date", 
        "Description": "Description", 
        "Original Description": None, 
        "Amount": None, 
        "Category": None, 
        "Account Name": None, 
        "Transaction Type": "Type", 
        "Credit": "Credit", 
        "Debit": "Debit", 
        "Labels": None, 
        "Notes": None,
        "Balance": "Balance"
    },
    'alecu_check.csv': {
        "Date": "Date", 
        "Description": "Description", 
        "Original Description": None, 
        "Amount": None, 
        "Category": None, 
        "Account Name": None, 
        "Transaction Type": "Type", 
        "Credit": "Credit", 
        "Debit": "Debit", 
        "Labels": None, 
        "Notes": None,
        "Balance": "Balance"
    },
    'chase.csv': {
        "Date": "Transaction Date", 
        "Description": "Description", 
        "Original Description": None, 
        "Amount": "Amount", 
        "Category": "Category", 
        "Account Name": None, 
        "Transaction Type": "Type", 
        "Credit": None, 
        "Debit": None, 
        "Labels": None, 
        "Notes": "Memo",
        "Balance": None
    }
    # ,
    # 'mint.csv': {
    #     "Date": "Date", 
    #     "Description": "Description", 
    #     "Original Description": "Original Description", 
    #     "Amount": "Amount", 
    #     "Category": "Category", 
    #     "Account Name": "Account Name", 
    #     "Transaction Type": "Transaction Type", 
    #     "Credit": None, 
    #     "Debit": None, 
    #     "Labels": "Labels", 
    #     "Notes": "Notes",
    #     "Balance": None,
    # }
}

# Standardize and store each DataFrame
for file in csv_files:
    file_path = os.path.join(folder_path, file)
    df = pd.read_csv(file_path)
    
    # Get the mapping for the current file
    mappings = file_mappings.get(file, {})
    standardized_df = standardize_dataframe(df, file, mappings)
    
    dataframes.append(standardized_df)


# Drop all-NA columns in each DataFrame before concatenation
cleaned_dataframes = [df.dropna(axis=1, how='all') for df in dataframes]

# Now concatenate the cleaned DataFrames
standard_df = pd.concat(cleaned_dataframes, ignore_index=True)

# # Combine all standardized DataFrames into one
# standard_df = pd.concat(dataframes, ignore_index=True)

# Sort the final DataFrame by date
standard_df = standard_df.sort_values(by='Date')


# Recategorize
standard_df['Category'] = standard_df.apply(recategorize_transactions, axis=1)

# Label Subscriptions
standard_df['Labels'] = standard_df.apply(label_subscriptions, axis=1)

# Label Outliers
standard_df['outliers'] = standard_df.apply(label_outliers, axis=1)

# Reshuffle the columns
standard_df = reshuffle_df(standard_df)

# Call the function to write the DataFrame to a CSV file
write_dataframe_to_csv(standard_df)
recent_month(standard_df)




