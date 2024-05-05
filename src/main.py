import os
import pandas as pd
import numpy as np

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

t_data.head()

c_data.head()

# Custom function to apply recategorization logic
def recategorize_transactions(row):
    if 'climb' in row['Description'] and row['Amount'] < -80:
        return 'gym'
    elif 'hos corp' in row['Description'] and row['Amount'] > -25:
        return 'restaurants'    
    elif 'new loan' in row['Description'] and row['Amount'] < -10000:
        return 'auto loan'    
    elif 'mortgage & rent' in row['Category'] and row['Amount'] < -37000:
        return 'transfer to vanguard'    
    elif 'hbo now' in row['Description']:
        return 'entertainment'
    elif 'robinhood' in row['Description']:
        return 'investments'       
    elif 'dividend' in row['Description']:
        return 'investments'   
    elif 'coinbase' in row['Description']:
        return 'investments'    
    elif 'alliant' in row['Description'] and row['Amount'] < -600:
        return 'rent'  
    elif 'airbnb' in row['Description']:
        return 'hotel'    
    elif 'walgreens' in row['Description']:
        return 'shopping'
    elif 'acme feed' in row['Description']:
        return 'restaurants'
    elif 'ach trans - select rwds pymt' in row['Description'] and row['Amount'] < -2792:
        return 'travel - Las Vegas climbing trip AirBNB + CC Payment'
    else:
        return row['Category']

# Apply the recategorization logic to the DataFrame
t_data['Category'] = t_data.apply(recategorize_transactions, axis=1)
c_data['Category'] = c_data.apply(recategorize_transactions, axis=1)

# Custom function to apply subscription labels based on description content
def label_subscriptions(row):
    if 'lucid' in row['Description']:
        return 'subscription - productivity'
    elif 'hbo' in row['Description'] or 'patreon' in row['Description'] or 'samharris' in row['Description'] or 'spotify' in row['Description']:
        return 'subscription - media'
    elif 'amazon prime' in row['Description']:
        return 'subscription - shopping'
    elif 'airbnb' in row['Description']:
        return 'travel hotel'
    elif 'climb' in row['Description'] and -50 > row['Amount'] > -150:
        return 'subscription - fitness'
    elif 'fahrenheit yoga' in row['Description']:
        return 'subscription - fitness'
    elif 'chase credit' in row['Description']:
        return 'chase credit card payment' 
    elif 'ach trans - select rwds pymt' in row['Description'] and row['Amount'] < -2792:
        return 'vegas vacation airbnb'
    else:
        return row['Labels']

# Apply the recategorization logic to the DataFrame
t_data['Labels'] = t_data.apply(label_subscriptions, axis=1)
c_data['Labels'] = c_data.apply(label_subscriptions, axis=1)

# Custom function to change trans type to match mint 
def chase_trans_type(row):
    if 'payment' in row['Type']:
        return 'credit'
    elif 'adjustment' in row['Type']:
        return 'credit'
    elif 'sale' in row['Type']:
        return 'debit'
    else:
        return row['Type']

# Apply the recategorization logic to the DataFrame
c_data['Type'] = c_data.apply(chase_trans_type, axis=1)


# Custom function to tag outliers in the dataset
def label_outliers(row):
    if  'auto' in row['Category'] and row['Amount'] < -2000:
        return 1
    elif 'buy' in row['Category'] and row['Amount'] < -10000:
        return 1
    elif 'transfer' in row['Category'] and row['Amount'] < -37000:
        return 1
    elif 'chest freezer' in row['Description'] and row['Amount'] < -500:
        return 1
    else:
        return 0

# Apply the recategorization logic to the DataFrame
t_data['outliers'] = t_data.apply(label_outliers, axis=1)
c_data['outliers'] = c_data.apply(label_outliers, axis=1)

# Define the categorize_categories function
def nws_categories(df):
    # Create a dictionary to map original categories to new values
    category_mapping = {
        'rent': 'need',
        'food': 'need',
        'food & drink': 'need',
        'restaurants': 'want',
        'cafe': 'want',
        'coffee': 'need',
        'coffee shops': 'want',
        'pharmacy': 'need',
        'groceries': 'need',
        'auto': 'need',
        'gas & fuel': 'need',
        'food & dining': 'want',
        'ride share': 'need',
        'parking': 'need',
        'rental car & taxi': 'need',
        'transportation': 'need',
        'hotel': 'want',
        'venmo': 'want',
        'travel': 'want',
        'entertainment': 'want',
        'amusement': 'want',
        'clothing': 'want',
        'dating': 'want',
        'transfer': 'need',
        'concert': 'want',
        'club': 'want',
        'movie': 'want',
        'Dentist': 'need',
        'Doctor': 'need',
        'Internet': 'need',
        'bills': 'need',
        'utilities': 'need',
        'Life Insurance': 'need',
        'bills & utilities': 'need',
        'Mobile Phone': 'need',
        'business services': 'need',
        'Loans': 'savings_debts',
        'alcohol & bars': 'want',
        'gift': 'need',
        'gym': 'need',
        'auto & transport': 'need',
        'music': 'need',
        'fast food': 'want',
        'sporting goods': 'want',
        'charity': 'want',
        'books': 'need',
        'electronics & software': 'want',
        'shopping': 'want',
        'investments': 'need',
        'paycheck': 'need',
        'personal care': 'want',
        'misc expenses': 'want',
        'fees & charges': 'need',
        'mortgage & rent': 'need',
        'venmo payment': 'want',
        'advertising': 'want',
        'podcast': 'want',
        'arts': 'want',
        'air travel': 'want',
        'kids': 'want',
        'newspapers & magazines': 'want',
        'federal tax': 'need',
        'home improvement': 'need',
        'books & supplies': 'want',
        'uncategorized': 'want',
        'movies & dvds': 'want',
        'health & fitness': 'need',
        'income': 'need',
        'doctor': 'health',
        'cash & atm': 'need',
        'office supplies': 'want',
        'spa & massage': 'want',
        'laundry': 'want',
        'auto insurance': 'need',
        'hair': 'want',
        'shipping': 'want',
        'service & parts': 'need',
        'bank fee': 'need',
        'home services': 'need',
        'finance charge': 'need',
        'atm fee': 'need',
        'life insurance': 'need',
        'dentist': 'health',
        'public transportation': 'need',
        'furnishings': 'want',
        'mobile phone': 'need',
        'home': 'need',
        'sports': 'want',
        'gifts & donation': 'want',
        'bitcoin investment': 'need',
        'gifts & donations': 'want',
        'television': 'entertainment',
        'vacation': 'travel',
        'therapy': 'health',
        'lawn & garden': 'need',
        'classes': 'need',
        'hca cafe': 'want',
        'credit card payments': 'need',
        'printing': 'want',
        'credit card payment': 'need',
        'home supplies': 'need',
        'kids activities': 'want',
        'education': 'need',
        'hobbies': 'want',
        'question?': 'want',
        'financial': 'need',
        'home phone': 'need',
        'auto payment	': 'need',
        'returned purchase': 'want',
        'tax advisor': 'need',
        'internet': 'need',
        'attorney fee': 'need',
        'legal': 'need',
        'personal': 'want',
        'health & wellness': 'need',
        'return': 'want',
        'gas': 'need', 
        'automotive': 'need', 
        'fees & adjustments': 'need', 
        'pets': 'want',
        'golf': 'want',
        'comedy club': 'want',
        'cpa fees': 'need',
        'buy': 'loans',
        'auto loan': 'loans',
        'endurance race': 'want',
        'late fee': 'need',
        'toys': 'want',
        'transfer for cash spending': 'want',
        'hair': 'want',
        'tuition': 'want',
    }

    # Create a new column 'Cat2' based on the mapping
    # Add NNWS (Needs/Wants/Savings) column and initialize it as null. First broad bucket to group transactions
    df['NWS'] = df['Category'].str.lower().map(category_mapping)

    return df

# Call the categorize_categories function with your 't_data' DataFrame
t_data = nws_categories(t_data)
c_data = nws_categories(c_data)


# # Filter and return all rows where 'Cat2' is NaN
# rows_with_nan_cat2 = result_data.loc[result_data['Cat2'].isna()]
# # Print or use the filtered DataFrame
# rows_with_nan_cat2

# Define the categorize_categories function
def categorize_categories(df):
    # Create a dictionary to map original categories to new values
    category_mapping = {
        'food': 'food',
        'food & drink': 'food',
        'restaurants': 'food',
        'cafe': 'food',
        'coffee': 'food',
        'coffee shops': 'food',
        'pharmacy': 'food',
        'groceries': 'food',
        'auto': 'auto',
        'gas & fuel': 'auto',
        'food & dining': 'auto',
        'ride share': 'auto',
        'parking': 'auto',
        'rental car & taxi': 'auto',
        'transportation': 'auto',
        'hotel': 'discretionary',
        'venmo': 'discretionary',
        'travel': 'discretionary',
        'entertainment': 'discretionary',
        'amusement': 'discretionary',
        'clothing': 'discretionary',
        'dating': 'discretionary',
        'transfer': 'transfer',
        'concert': 'discretionary',
        'club': 'discretionary',
        'movie': 'discretionary',
        'Dentist': 'utilities',
        'Doctor': 'utilities',
        'Internet': 'utilities',
        'bills': 'utilities',
        'utilities': 'utilities',
        'Life Insurance': 'utilities',
        'bills & utilities': 'utilities',
        'Mobile Phone': 'utilities',
        'business services': 'utilities',
        'Loans': 'loans',
        'alcohol & bars': 'discretionary',
        'gift': 'discretionary',
        'gym': 'investment',
        'auto & transport': 'auto',
        'music': 'discretionary',
        'fast food': 'food',
        'sporting goods': 'discretionary',
        'charity': 'discretionary',
        'books': 'investment',
        'electronics & software': 'discretionary',
        'shopping': 'discretionary',
        'investments': 'investment',
        'paycheck': 'income',
        'personal care': 'discretionary',
        'misc expenses': 'discretionary',
        'fees & charges': 'bills',
        'mortgage & rent': 'bills',
        'venmo payment': 'bills',
        'advertising': 'discretionary',
        'podcast': 'entertainment',
        'arts': 'discretionary',
        'air travel': 'travel',
        'kids': 'discretionary',
        'newspapers & magazines': 'entertainment',
        'federal tax': 'bills',
        'home improvement': 'utilities',
        'books & supplies': 'investment',
        'uncategorized': 'uncategorized',
        'movies & dvds': 'entertainment',
        'health & fitness': 'investment',
        'income': 'discretionary',
        'doctor': 'health',
        'cash & atm': 'bills',
        'office supplies': 'discretionary',
        'spa & massage': 'discretionary',
        'laundry': 'discretionary',
        'auto insurance': 'auto',
        'hair': 'discretionary',
        'shipping': 'discretionary',
        'service & parts': 'auto',
        'bank fee': 'bills',
        'home services': 'utilities',
        'finance charge': 'bills',
        'atm fee': 'bills',
        'life insurance': 'bills',
        'dentist': 'health',
        'public transportation': 'auto',
        'furnishings': 'discretionary',
        'mobile phone': 'bills',
        'home': 'utilities',
        'sports': 'discretionary',
        'gifts & donation': 'discretionary',
        'bitcoin investment': 'investment',
        'gifts & donations': 'discretionary',
        'television': 'entertainment',
        'vacation': 'travel',
        'therapy': 'health',
        'lawn & garden': 'utilities',
        'classes': 'investment',
        'hca cafe': 'food',
        'credit card payments': 'bills',
        'printing': 'discretionary',
        'credit card payment': 'bills',
        'home supplies': 'utilities',
        'kids activities': 'discretionary',
        'education': 'investment',
        'hobbies': 'discretionary',
        'question?': 'uncategorized',
        'financial': 'investment',
        'home phone': 'utilities',
        'auto payment	': 'auto',
        'returned purchase': 'discretionary',
        'tax advisor': 'bills',
        'internet': 'bills',
        'fees & adjustments': 'bills',
        'attorney fee': 'bills',
        'legal': 'bills',
        'return': 'discretionary',
        'gas': 'auto', 
        'automotive': 'auto', 
        'pets': 'discretionary',
        'golf': 'discretionary',
        'comedy club': 'discretionary',
        'personal': 'discretionary',
        'health & wellness': 'investment',
        'cpa fees': 'bills',
        'buy': 'loans',
        'auto loan': 'loans',
        'endurance race': 'discretionary',
        'late fee': 'bills',
        'toys': 'discretionary',
        'transfer for cash spending': 'discretionary',
        'hair': 'discretionary',
        'tuition': 'discretionary',
    }

    # Create a new column 'Cat2' based on the mapping
    df['Cat2'] = df['Category'].str.lower().map(category_mapping)

    return df

# Call the categorize_categories function with your 't_data' DataFrame
t_data = categorize_categories(t_data)
c_data = categorize_categories(c_data)



t_data.rename(columns = {'Date':'Transaction_Date'}, inplace = True)

t_data = t_data.loc[:,['Transaction_Date','Post_Date','Year','Month','Account_Name','Transaction_Type','Amount','NWS','Category','Cat2','Description','Labels','outliers','Notes']]

c_data.rename(columns = {'Type':'Transaction_Type','Memo':'Notes'}, inplace = True)

c_data = c_data.loc[:,['Transaction_Date','Post_Date','Year','Month','Account_Name','Transaction_Type','Amount','NWS','Category','Cat2','Description','Labels','outliers','Notes']]



# Write the DataFrame to a new CSV file
t_data.to_csv('data/output/clean.csv', index=False)
c_data.to_csv('data/output/chase.csv', index=False)



