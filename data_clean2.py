iimport pandas as pd
import numpy as np

# Read the Customer CSV file
df_customers = pd.read_csv('C:/Users/Admin/Desktop/M5-20260106/sample-data/03_Library SystemCustomers.csv')

def clean_customer_data(df):
    # Convert Customer ID to integer (before removing other missing values)
    # First, remove rows where Customer ID is missing
    df = df.dropna(subset=['Customer ID'])
    df['Customer ID'] = df['Customer ID'].astype(int)
    print("Customer ID converted to integer")
    
    # Remove rows with missing values in any column
    df_cleaned = df.dropna()
    print(f"\nAfter removing all missing values: {df_cleaned.shape}")
    
    # Standardize column names (capitalize first letter, replace spaces with _)
    df_cleaned.columns = df_cleaned.columns.str.replace(' ', '_').str.title()
    print(f"New column names: {list(df_cleaned.columns)}")
    
    # Display summary
    print("\n--- Customer Data Cleaning Summary ---")
    print(f"Original rows: {len(df)}")
    print(f"Rows removed (missing values): {len(df) - len(df_cleaned)}")
    print(f"Final rows: {len(df_cleaned)}")
    
    return df_cleaned

df_customers_cleaned = clean_customer_data(df_customers)

# Save cleaned customer data
df_customers_cleaned.to_csv('output-data/cleaned_customers.csv', index=False)
print("\nCleaned customer data saved to 'output-data/cleaned_customers.csv'")