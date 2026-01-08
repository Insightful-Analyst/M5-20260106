import pandas as pd
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


# Read the Library System CSV file
df_library = pd.read_csv('C:/Users/Admin/Desktop/M5-20260106/sample-data/03_Library Systembook.csv')

print("\nOriginal data shape:", df_library.shape)
print("\nFirst few rows:")
print(df_library.head())
print("\nData types:")
print(df_library.dtypes)

# Check for missing values
print("\n--- Missing Values Check ---")
missing_count = df_library.isnull().sum()
print(missing_count)
print(f"Total rows with missing values: {df_library.isnull().any(axis=1).sum()}")

# Create a copy for cleaning
df_library_cleaned = df_library.copy()

# Standardize column names first (capitalize first letter, replace spaces with _)
print("\n--- Standardizing Column Names ---")
print(f"Original column names: {list(df_library_cleaned.columns)}")
df_library_cleaned.columns = df_library_cleaned.columns.str.replace(' ', '_').str.title()
print(f"New column names: {list(df_library_cleaned.columns)}")

# Clean book titles: remove trailing spaces, title case
print("\n--- Cleaning Book Titles ---")
if 'Books' in df_library_cleaned.columns:
    # Remove leading/trailing spaces
    df_library_cleaned['Books'] = df_library_cleaned['Books'].str.strip()
    
    # Convert to title case (capitalizes major words, lowercase for minor words)
    df_library_cleaned['Books'] = df_library_cleaned['Books'].str.title()
    print("Book titles cleaned and formatted")
    print("Sample book titles:")
    print(df_library_cleaned['Books'].head())

# Remove quotation marks from Book_Checkout dates
print("\n--- Removing Quotation Marks from Dates ---")
if 'Book_Checkout' in df_library_cleaned.columns:
    df_library_cleaned['Book_Checkout'] = df_library_cleaned['Book_Checkout'].astype(str).str.replace('"', '').str.replace("'", '')
    print("Quotation marks removed from Book_Checkout column")

# Convert "2 weeks" to days (14 days)
print("\n--- Converting Weeks to Days ---")
if 'Days_Allowed_To_Borrow' in df_library_cleaned.columns:
    # Handle "2 weeks" or similar patterns
    df_library_cleaned['Days_Allowed_To_Borrow'] = df_library_cleaned['Days_Allowed_To_Borrow'].astype(str).str.lower()
    df_library_cleaned['Days_Allowed_To_Borrow'] = df_library_cleaned['Days_Allowed_To_Borrow'].str.replace('weeks', '').str.strip()
    df_library_cleaned['Days_Allowed_To_Borrow'] = pd.to_numeric(df_library_cleaned['Days_Allowed_To_Borrow'], errors='coerce') * 7
    
    # Check for any NaN values after conversion
    invalid_days_count = df_library_cleaned['Days_Allowed_To_Borrow'].isnull().sum()
    if invalid_days_count > 0:
        print(f"Warning: Found {invalid_days_count} rows that couldn't be converted to days")
        print("These rows will be removed")
        df_library_cleaned = df_library_cleaned.dropna(subset=['Days_Allowed_To_Borrow'])
    
    # Now convert to integer
    df_library_cleaned['Days_Allowed_To_Borrow'] = df_library_cleaned['Days_Allowed_To_Borrow'].astype(int)
    print("Converted weeks to days")
    print(f"Sample values: {df_library_cleaned['Days_Allowed_To_Borrow'].head().tolist()}")

# Convert date columns to datetime format and check for incorrect formats
print("\n--- Date Format Check ---")
date_columns = ['Book_Checkout', 'Book_Returned']

for col in date_columns:
    if col in df_library_cleaned.columns:
        print(f"\nProcessing column: {col}")
        # Count nulls before conversion
        nulls_before = df_library_cleaned[col].isnull().sum()
        
        # Try to convert to datetime, coerce errors to NaT
        df_library_cleaned[col] = pd.to_datetime(df_library_cleaned[col], errors='coerce')
        
        # Check how many invalid dates were found
        nulls_after = df_library_cleaned[col].isnull().sum()
        invalid_dates = nulls_after - nulls_before
        if invalid_dates > 0:
            print(f"  Found {invalid_dates} rows with invalid date format")