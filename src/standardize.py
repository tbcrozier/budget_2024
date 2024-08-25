import pandas as pd

# Define the standard columns
standard_columns = ["Date", "Description", "Original Description", "Amount", 
                    "Transaction Type", "Category", "Account Name", "Labels", "Notes"]


# Function to standardize each DataFrame
def standardize_dataframe(df, source, mappings):
    df_standardized = pd.DataFrame(columns=standard_columns)

    # Replace spaces with underscores in column names
    df_standardized.columns = df_standardized.columns.str.replace(' ', '_')

    for col, mapped_col in mappings.items():
        if mapped_col in df.columns:
            df_standardized[col] = df[mapped_col]
    df_standardized['Source'] = source
    
    # Convert Date column to datetime format, handle different formats
    df_standardized['Date'] = pd.to_datetime(df_standardized['Date'], errors='coerce')
    df_standardized['Month-Year'] = df_standardized['Date'].dt.to_period('M')

    # Convert all dates to the same format (YYYY-MM-DD)
    df_standardized['Date'] = df_standardized['Date'].dt.strftime('%Y-%m-%d')

    # Convert all text data in the DataFrame to lowercase (done to help w match rules)
    df_std_txt_col = ['Description', 'Original_Description', 'Transaction_Type', 'Category', 'Account_Name', 'Notes']
    df_standardized[df_std_txt_col] = df_standardized[df_std_txt_col].apply(lambda x: x.astype(str).str.lower())
    # Strip whitespace from all string columns
    df_standardized = df_standardized.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    df_standardized = df_standardized.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

    # Add Label2 to capture more granular categories
    df_standardized['Labels'] = ''
    df_standardized['Memo'] = ''
    
    return df_standardized
