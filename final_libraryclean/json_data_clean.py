## Before starting, in terminal run 'pip install -r requirements.txt'

import pandas as pd
import os
import json
from datetime import datetime

class MetricsLogger:
    """Class to track and log data cleaning metrics"""
    
    def __init__(self):
        self.metrics = {
            'execution_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'systembook_metrics': {},
            'customers_metrics': {}
        }
    
    def log_metric(self, dataset, metric_name, value):
        """Log a metric for a specific dataset"""
        if dataset not in self.metrics:
            self.metrics[dataset] = {}
        self.metrics[dataset][metric_name] = value
    
    def save_metrics(self, output_path):
        """Save metrics to a JSON file"""
        try:
            with open(output_path, 'w') as f:
                json.dump(self.metrics, f, indent=4)
            print(f"Metrics saved to {output_path}")
        except Exception as e:
            print(f"Error saving metrics: {e}")
    
    def print_summary(self):
        """Print a summary of all metrics"""
        print("\n" + "="*60)
        print("PIPELINE EXECUTION METRICS SUMMARY")
        print("="*60)
        for dataset, metrics in self.metrics.items():
            if dataset != 'execution_timestamp':
                print(f"\n{dataset.upper()}:")
                for metric, value in metrics.items():
                    print(f"  {metric}: {value}")
        print("="*60 + "\n")

# Initialize global metrics logger
metrics_logger = MetricsLogger()

# Function to output dataframe that can be manipulated via a filepath
def fileLoader(filepath, dataset_name):
    data = pd.read_csv(filepath)
    initial_rows = len(data)
    metrics_logger.log_metric(dataset_name, 'initial_row_count', initial_rows)
    print(f"Loaded {initial_rows} rows from {filepath}")
    return data 

# Duplicate Dropping Function
def duplicateCleaner(df, dataset_name):
    initial_count = len(df)
    df_cleaned = df.drop_duplicates().reset_index(drop=True)
    duplicates_dropped = initial_count - len(df_cleaned)
    metrics_logger.log_metric(dataset_name, 'duplicates_dropped', duplicates_dropped)
    print(f"Dropped {duplicates_dropped} duplicate rows")
    return df_cleaned

# NA handler - future scope can handle errors more elegantly. 
def naCleaner(df, dataset_name):
    initial_count = len(df)
    na_count = df.isna().sum().sum()
    metrics_logger.log_metric(dataset_name, 'blank_cells_found', int(na_count))
    
    df_cleaned = df.dropna().reset_index(drop=True)
    na_rows_dropped = initial_count - len(df_cleaned)
    metrics_logger.log_metric(dataset_name, 'na_rows_dropped', na_rows_dropped)
    print(f"Found {na_count} blank cells, dropped {na_rows_dropped} rows with NAs")
    return df_cleaned

# Turning date columns into datetime
def dateCleaner(col, df, dataset_name):
    initial_count = len(df)
    
    # Strip any quotes from dates
    df[col] = df[col].str.replace('"', "", regex=True)

    try:
        df[col] = pd.to_datetime(df[col], dayfirst=True, errors='coerce')
    except Exception as e:
        print(f"Error while converting column {col} to datetime: {e}")

    # Identify rows with invalid dates
    error_flag = pd.to_datetime(df[col], dayfirst=True, errors='coerce').isna()
    invalid_dates = error_flag.sum()
    
    # Keep only valid rows in df
    df = df[~error_flag].copy()
    
    # Reset index for the cleaned DataFrame
    df.reset_index(drop=True, inplace=True)
    
    rows_dropped = initial_count - len(df)
    metrics_logger.log_metric(dataset_name, f'{col}_invalid_dates', int(invalid_dates))
    metrics_logger.log_metric(dataset_name, f'{col}_rows_dropped', rows_dropped)
    print(f"Found {invalid_dates} invalid dates in '{col}', dropped {rows_dropped} rows")
    
    return df

def idCleaner(id_columns, df, dataset_name):
    """
    Convert ID columns to integers
    """
    converted_columns = []
    for col in id_columns:
        if col in df.columns:
            try:
                df[col] = df[col].astype('Int64')
                converted_columns.append(col)
                print(f"Converted {col} to integer")
            except Exception as e:
                print(f"Error converting {col} to integer: {e}")
    
    metrics_logger.log_metric(dataset_name, 'id_columns_converted', len(converted_columns))
    return df

def enrich_dateDuration(colA, colB, df, dataset_name):
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
    metrics_logger.log_metric(dataset_name, 'invalid_loans_found', int(invalid_count))
    
    if invalid_count > 0:
        print(f"Warning: Found {invalid_count} invalid loan(s) where return date is before checkout date. Removing these records.")
    
    df = df[df['valid_loan_flag']].copy()
    df.reset_index(drop=True, inplace=True)
    
    metrics_logger.log_metric(dataset_name, 'invalid_loans_dropped', int(invalid_count))

    return df

if __name__ == '__main__':
    print('**************** Starting Clean ****************')

    # Instantiation - Using Windows paths
    filepath_input = 'C:/Users/Admin/Desktop/M5-20260106/sample-data/03_Library Systembook.csv'
    date_columns = ['Book checkout', 'Book Returned']
    id_columns_loans = ['Id', 'Customer ID']
    output_dir = 'C:/Users/Admin/Desktop/M5-20260106/output-data'

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Process systembook data
    data = fileLoader(filepath=filepath_input, dataset_name='systembook_metrics')

    # Drop duplicates & NAs
    data = duplicateCleaner(data, dataset_name='systembook_metrics')
    data = naCleaner(data, dataset_name='systembook_metrics')

    # Converting date columns into datetime
    for col in date_columns:
        data = dateCleaner(col, data, dataset_name='systembook_metrics')
    
    # Enriching the dataset and removing invalid loans
    data = enrich_dateDuration(df=data, colA='Book checkout', colB='Book Returned', dataset_name='systembook_metrics')

    # Convert ID columns to integers
    data = idCleaner(id_columns_loans, data, dataset_name='systembook_metrics')
    
    # Log final row count
    final_rows = len(data)
    metrics_logger.log_metric('systembook_metrics', 'final_row_count', final_rows)
    initial_rows = metrics_logger.metrics['systembook_metrics']['initial_row_count']
    total_dropped = initial_rows - final_rows
    metrics_logger.log_metric('systembook_metrics', 'total_rows_dropped', total_dropped)
    metrics_logger.log_metric('systembook_metrics', 'data_retention_rate', round((final_rows / initial_rows) * 100, 2))

    print(data)

    # Cleaning the customer file
    filepath_input_2 = 'C:/Users/Admin/Desktop/M5-20260106/sample-data/03_Library SystemCustomers.csv'
    id_columns_customers = ['Customer ID']

    data2 = fileLoader(filepath=filepath_input_2, dataset_name='customers_metrics')

    # Drop duplicates & NAs
    data2 = duplicateCleaner(data2, dataset_name='customers_metrics')
    data2 = naCleaner(data2, dataset_name='customers_metrics')

    # Convert ID columns to integers
    data2 = idCleaner(id_columns_customers, data2, dataset_name='customers_metrics')
    
    # Log final row count
    final_rows_customers = len(data2)
    metrics_logger.log_metric('customers_metrics', 'final_row_count', final_rows_customers)
    initial_rows_customers = metrics_logger.metrics['customers_metrics']['initial_row_count']
    total_dropped_customers = initial_rows_customers - final_rows_customers
    metrics_logger.log_metric('customers_metrics', 'total_rows_dropped', total_dropped_customers)
    metrics_logger.log_metric('customers_metrics', 'data_retention_rate', round((final_rows_customers / initial_rows_customers) * 100, 2))

    print(data2)
    print('**************** DATA CLEANED ****************')

    # Print metrics summary
    metrics_logger.print_summary()

    # Save metrics to JSON file
    metrics_file = f'{output_dir}/pipeline_metrics.json'
    metrics_logger.save_metrics(metrics_file)

    print('Writing cleaned data to CSV files...')

    # Write cleaned data to CSV
    data.to_csv(f'{output_dir}/cleaned_library_systembook.csv', index=False)
    data2.to_csv(f'{output_dir}/cleaned_customers.csv', index=False)
    
    print('**************** End ****************')