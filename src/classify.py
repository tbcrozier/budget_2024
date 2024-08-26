import pandas as pd

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
    elif 'chase credit' in row['Description']:
        return 'chase credit card payment' 
    elif 'ach trans - select rwds pymt' in row['Description'] and row['Amount'] < -2792:
        return 'vegas vacation airbnb'
    elif 'ach trans - select rwds pymt' in row['Description'] and row['Amount'] < -2792:
        return 'travel - Las Vegas climbing trip AirBNB + CC Payment'
    else:
        return row['Category']
    

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
    elif 'chatgpt' in row['Description']:
        return 'subscription - chatgpt'
    else:
        return row['Labels']


# # Custom function to change trans type to match mint 
# def chase_trans_type(row):
#     if 'payment' in row['Type']:
#         return 'credit'
#     elif 'adjustment' in row['Type']:
#         return 'credit'
#     elif 'sale' in row['Type']:
#         return 'debit'
#     else:
#         return row['Type']



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
