## Before starting, in terminal run 'pip install -r requirements.txt'

import pandas as pd
import os

# Function to output dataframe that can be manipulated via a filepath
def fileLoader(filepath):
    data = pd.read_csv(filepath)
    return data 

# Duplicate Dropping Function
def duplicateCleaner(df):
    return df.drop_duplicates().reset_index(drop=True)

# NA handler - future scope can handle errors more elegantly. 
def naCleaner(df):
    return df.dropna().reset_index(drop=True)

# Turning date columns into datetime
def dateCleaner(col, df):
    #date_errors = pd.DataFrame(columns=df.columns)  # Store rows with date errors

    # Strip any quotes from dates
    df[col] = df[col].str.replace('"', "", regex=True)

    try:
        df[col] = pd.to_datetime(df[col], dayfirst=True, errors='coerce')

    except Exception as e:
        print(f"Error while converting column {col} to datetime: {e}")

    # Identify rows with invalid dates
    error_flag = pd.to_datetime(df[col], dayfirst=True, errors='coerce').isna()
        
    # Move invalid rows to date_errors - Future feature
    #date_errors = df[error_flag]
        
    # Keep only valid rows in df
    df = df[~error_flag].copy()

    # Reset index for the cleaned DataFrame
    df.reset_index(drop=True, inplace=True)

    return df

def enrich_dateDuration(colA, colB, df):
    """
    Takes the two datetime input column names and the dataframe to create a new column date_delta which is the difference, in days, between colA and colB.
    
    Note:
    colB>colA
    """
    df['days_borrowed'] = (df[colB]-df[colA]).dt.days

    #Conditional Filtering to be able to gauge erroneous loans.
    df.loc[df['days_borrowed'] < 0, 'valid_loan_flag'] = False
    df.loc[df['days_borrowed'] >= 0, 'valid_loan_flag'] = True

    return df

if __name__ == '__main__':
    print('**************** Starting Clean ****************')

    # Instantiation - Using Docker volume paths
    filepath_input = '/data/03_Library Systembook.csv'
    date_columns = ['Book checkout', 'Book Returned']
    output_dir = '/output'

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    data = fileLoader(filepath=filepath_input)

    # Drop duplicates & NAs
    data = duplicateCleaner(data)
    data = naCleaner(data)

    # Converting date columns into datetime
    for col in date_columns:
        data = dateCleaner(col, data)
    
    # Enriching the dataset
    data = enrich_dateDuration(df=data, colA='Book Returned', colB='Book checkout')

    print(data)

    # Cleaning the customer file
    filepath_input_2 = '/data/03_Library SystemCustomers.csv'

    data2 = fileLoader(filepath=filepath_input_2)

    # Drop duplicates & NAs
    data2 = duplicateCleaner(data2)
    data2 = naCleaner(data2)

    print(data2)
    print('**************** DATA CLEANED ****************')

    print('Writing cleaned data to CSV files...')

    # Write cleaned data to CSV
    data.to_csv(f'{output_dir}/cleaned_library_systembook.csv', index=False)
    data2.to_csv(f'{output_dir}/cleaned_customers.csv', index=False)
    
    print('**************** End ****************')