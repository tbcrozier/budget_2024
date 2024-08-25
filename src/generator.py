import pandas as pd
import os

def write_dataframe_to_csv(df):
    """
    Writes the given DataFrame to a CSV file at the specified file path.
    
    Parameters:
    df (pandas.DataFrame): The DataFrame to write to a CSV file.
    file_path (str): The path (including filename) where the CSV file will be saved.
    """

    file_path = 'data/output/standard_df.csv'

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # Write the DataFrame to the specified CSV file
    df.to_csv(file_path, index=False)
    
    print(f"The DataFrame has been successfully written to '{file_path}'.")


def recent_month(df):
    """
    Writes the given DataFrame to a CSV file at the specified file path.
    
    Parameters:
    df (pandas.DataFrame): The DataFrame to write to a CSV file.
    file_path (str): The path (including filename) where the CSV file will be saved.
    """

    file_path = 'data/output/recent_month.csv'

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Ensure the Date column is in datetime format (if not already done)
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Extract the most recent month (last month's transactions)
    most_recent_month = df['Date'].dt.to_period('M').max()

    # Filter the DataFrame for transactions in the most recent month and sort by Date
    last_month_transactions = df[df['Date'].dt.to_period('M') == most_recent_month].sort_values(by='Date')

    # Write the DataFrame to the specified CSV file
    last_month_transactions.to_csv(file_path, index=False)
    
    print(f"The DataFrame has been successfully written to '{file_path}'.")
