import os
import pandas as pd

# Path relative to the script's location
# folder_path = os.path.join(os.path.dirname(__file__), 'data')
folder_path = 'data/sources'


# Initialize an empty list to store DataFrames
dataframes = []

# List all CSV files in the folder
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# Define the standard columns
standard_columns = ["Date", "Description", "Original Description", "Amount", 
                    "Transaction Type", "Category", "Account Name", "Labels", "Notes"]

# Function to standardize each DataFrame
def standardize_dataframe(df, source, mappings):
    df_standardized = pd.DataFrame(columns=standard_columns)
    for col, mapped_col in mappings.items():
        if mapped_col in df.columns:
            df_standardized[col] = df[mapped_col]
    df_standardized['Source'] = source
    
    # Convert Date column to datetime format, handle different formats
    df_standardized['Date'] = pd.to_datetime(df_standardized['Date'], errors='coerce')
    
    # Convert all dates to the same format (YYYY-MM-DD)
    df_standardized['Date'] = df_standardized['Date'].dt.strftime('%Y-%m-%d')
    
    return df_standardized

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

# Write final_df to a CSV file
standard_df.to_csv('data/output/standard_df.csv', index=False)

print("The DataFrame has been successfully written to 'standard_df.csv'.")
