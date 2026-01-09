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

def idCleaner(id_columns, df):
    """
    Convert ID columns to integers
    """
    for col in id_columns:
        if col in df.columns:
            try:
                # Use Int64 dtype to handle any potential NaN values
                df[col] = df[col].astype('Int64')
                print(f"Converted {col} to integer")
            except Exception as e:
                print(f"Error converting {col} to integer: {e}")
    return df

def enrich_dateDuration(colA, colB, df):
    """
    Takes the two datetime input column names and the dataframe to create a new column days_borrowed which is the difference, in days, between colB and colA.
    
    Note:
    colA = checkout date (earlier)
    colB = return date (later)
    colB > colA for valid loans
    """
    df['days_borrowed'] = (df[colB] - df[colA]).dt.days

    # Conditional Filtering to be able to gauge erroneous loans.
    df['valid_loan_flag'] = df['days_borrowed'] >= 0
    
    # Drop invalid loans (where days_borrowed is negative)
    invalid_count = (~df['valid_loan_flag']).sum()
    if invalid_count > 0:
        print(f"Warning: Found {invalid_count} invalid loan(s) where return date is before checkout date. Removing these records.")
    
    df = df[df['valid_loan_flag']].copy()
    df.reset_index(drop=True, inplace=True)

    return df

if __name__ == '__main__':
    print('**************** Starting Clean ****************')

    # Instantiation - Using Windows paths
    filepath_input = 'C:/Users/Admin/Desktop/M5-20260106/sample-data/03_Library Systembook.csv'
    date_columns = ['Book checkout', 'Book Returned']
    id_columns_loans = ['Id', 'Customer ID']  # ID columns for loans data (corrected from 'Book ID' to 'Id')
    output_dir = 'C:/Users/Admin/Desktop/M5-20260106/output-data'

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    data = fileLoader(filepath=filepath_input)

    # Drop duplicates & NAs
    data = duplicateCleaner(data)
    data = naCleaner(data)

    # Converting date columns into datetime
    for col in date_columns:
        data = dateCleaner(col, data)
    
    # Enriching the dataset and removing invalid loans
    data = enrich_dateDuration(df=data, colA='Book checkout', colB='Book Returned')

    # Convert ID columns to integers AFTER all other operations
    data = idCleaner(id_columns_loans, data)

    print(data)
    print(f"\nData types:\n{data.dtypes}")

    # Cleaning the customer file
    filepath_input_2 = 'C:/Users/Admin/Desktop/M5-20260106/sample-data/03_Library SystemCustomers.csv'
    id_columns_customers = ['Customer ID']  # ID columns for customer data

    data2 = fileLoader(filepath=filepath_input_2)

    # Drop duplicates & NAs
    data2 = duplicateCleaner(data2)
    data2 = naCleaner(data2)

    # Convert ID columns to integers
    data2 = idCleaner(id_columns_customers, data2)

    print(data2)
    print(f"\nData types:\n{data2.dtypes}")
    print('**************** DATA CLEANED ****************')

    print('Writing cleaned data to CSV files...')

    # Write cleaned data to CSV
    data.to_csv(f'{output_dir}/cleaned_library_systembook.csv', index=False)
    data2.to_csv(f'{output_dir}/cleaned_customers.csv', index=False)
    
    print('**************** End ****************')