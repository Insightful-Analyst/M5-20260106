import streamlit as st
import json
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Data Pipeline Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📊 Library Data Cleaning Pipeline Dashboard")
st.markdown("---")

# File path for metrics
metrics_file = 'C:/Users/Admin/Desktop/M5-20260106/output-data/pipeline_metrics.json'

# Check if metrics file exists
if not os.path.exists(metrics_file):
    st.error(f"⚠️ Metrics file not found at: {metrics_file}")
    st.info("Please run the data cleaning pipeline first to generate metrics.")
    st.stop()

# Load metrics
try:
    with open(metrics_file, 'r') as f:
        metrics = json.load(f)
except Exception as e:
    st.error(f"Error loading metrics: {e}")
    st.stop()

# Display execution timestamp
st.sidebar.header("Pipeline Execution Info")
st.sidebar.info(f"**Last Run:** {metrics.get('execution_timestamp', 'N/A')}")

# Refresh button
if st.sidebar.button("🔄 Refresh Dashboard"):
    st.rerun()

# Create tabs for different views
tab1, tab2, tab3 = st.tabs(["📈 Overview", "📚 Systembook Details", "👥 Customers Details"])

# Tab 1: Overview
with tab1:
    st.header("Pipeline Execution Overview")
    
    # Key metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    systembook = metrics.get('systembook_metrics', {})
    customers = metrics.get('customers_metrics', {})
    
    with col1:
        st.metric(
            "Systembook: Initial Rows",
            systembook.get('initial_row_count', 0)
        )
    
    with col2:
        st.metric(
            "Systembook: Final Rows",
            systembook.get('final_row_count', 0)
        )
    
    with col3:
        st.metric(
            "Customers: Initial Rows",
            customers.get('initial_row_count', 0)
        )
    
    with col4:
        st.metric(
            "Customers: Final Rows",
            customers.get('final_row_count', 0)
        )
    
    st.markdown("---")
    
    # Data retention rates
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📚 Systembook Data Retention")
        retention_rate = systembook.get('data_retention_rate', 0)
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = retention_rate,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Retention Rate (%)"},
            delta = {'reference': 100},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 80], 'color': "gray"},
                    {'range': [80, 100], 'color': "lightblue"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("👥 Customers Data Retention")
        retention_rate_customers = customers.get('data_retention_rate', 0)
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = retention_rate_customers,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Retention Rate (%)"},
            delta = {'reference': 100},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkgreen"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 80], 'color': "gray"},
                    {'range': [80, 100], 'color': "lightgreen"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    # Row changes comparison
    st.markdown("---")
    st.subheader("Row Count Changes")
    
    df_comparison = pd.DataFrame({
        'Dataset': ['Systembook', 'Customers'],
        'Initial': [systembook.get('initial_row_count', 0), customers.get('initial_row_count', 0)],
        'Final': [systembook.get('final_row_count', 0), customers.get('final_row_count', 0)],
        'Dropped': [systembook.get('total_rows_dropped', 0), customers.get('total_rows_dropped', 0)]
    })
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Initial', x=df_comparison['Dataset'], y=df_comparison['Initial'], marker_color='lightblue'))
    fig.add_trace(go.Bar(name='Final', x=df_comparison['Dataset'], y=df_comparison['Final'], marker_color='darkblue'))
    fig.add_trace(go.Bar(name='Dropped', x=df_comparison['Dataset'], y=df_comparison['Dropped'], marker_color='red'))
    
    fig.update_layout(barmode='group', title="Row Counts by Dataset", xaxis_title="Dataset", yaxis_title="Number of Rows")
    st.plotly_chart(fig, use_container_width=True)

# Tab 2: Systembook Details
with tab2:
    st.header("📚 Systembook Dataset Details")
    
    # Metrics cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Rows Dropped", systembook.get('total_rows_dropped', 0))
        st.metric("Duplicates Dropped", systembook.get('duplicates_dropped', 0))
    
    with col2:
        st.metric("Blank Cells Found", systembook.get('blank_cells_found', 0))
        st.metric("NA Rows Dropped", systembook.get('na_rows_dropped', 0))
    
    with col3:
        st.metric("Invalid Loans Found", systembook.get('invalid_loans_found', 0))
        st.metric("ID Columns Converted", systembook.get('id_columns_converted', 0))
    
    st.markdown("---")
    
    # Date validation metrics
    st.subheader("Date Validation Metrics")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Book Checkout Date**")
        st.metric("Invalid Dates", systembook.get('Book checkout_invalid_dates', 0))
        st.metric("Rows Dropped", systembook.get('Book checkout_rows_dropped', 0))
    
    with col2:
        st.markdown("**Book Returned Date**")
        st.metric("Invalid Dates", systembook.get('Book Returned_invalid_dates', 0))
        st.metric("Rows Dropped", systembook.get('Book Returned_rows_dropped', 0))
    
    st.markdown("---")
    
    # Breakdown of dropped rows
    st.subheader("Data Quality Issues Breakdown")
    
    issues_data = {
        'Issue Type': [],
        'Count': []
    }
    
    if systembook.get('duplicates_dropped', 0) > 0:
        issues_data['Issue Type'].append('Duplicates')
        issues_data['Count'].append(systembook.get('duplicates_dropped', 0))
    
    if systembook.get('na_rows_dropped', 0) > 0:
        issues_data['Issue Type'].append('Missing Values')
        issues_data['Count'].append(systembook.get('na_rows_dropped', 0))
    
    if systembook.get('Book checkout_rows_dropped', 0) > 0:
        issues_data['Issue Type'].append('Invalid Checkout Dates')
        issues_data['Count'].append(systembook.get('Book checkout_rows_dropped', 0))
    
    if systembook.get('Book Returned_rows_dropped', 0) > 0:
        issues_data['Issue Type'].append('Invalid Return Dates')
        issues_data['Count'].append(systembook.get('Book Returned_rows_dropped', 0))
    
    if systembook.get('invalid_loans_dropped', 0) > 0:
        issues_data['Issue Type'].append('Invalid Loan Duration')
        issues_data['Count'].append(systembook.get('invalid_loans_dropped', 0))
    
    if issues_data['Issue Type']:
        df_issues = pd.DataFrame(issues_data)
        fig = px.pie(df_issues, values='Count', names='Issue Type', title='Distribution of Data Quality Issues')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.success("✅ No data quality issues found!")

# Tab 3: Customers Details
with tab3:
    st.header("👥 Customers Dataset Details")
    
    # Metrics cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Rows Dropped", customers.get('total_rows_dropped', 0))
    
    with col2:
        st.metric("Duplicates Dropped", customers.get('duplicates_dropped', 0))
    
    with col3:
        st.metric("NA Rows Dropped", customers.get('na_rows_dropped', 0))
    
    st.markdown("---")
    
    # Additional metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Blank Cells Found", customers.get('blank_cells_found', 0))
    
    with col2:
        st.metric("ID Columns Converted", customers.get('id_columns_converted', 0))
    
    st.markdown("---")
    
    # Data quality summary
    st.subheader("Data Quality Summary")
    
    if customers.get('total_rows_dropped', 0) == 0:
        st.success("✅ No rows were dropped! Customer data is clean.")
    else:
        issues_data_customers = {
            'Issue Type': [],
            'Count': []
        }
        
        if customers.get('duplicates_dropped', 0) > 0:
            issues_data_customers['Issue Type'].append('Duplicates')
            issues_data_customers['Count'].append(customers.get('duplicates_dropped', 0))
        
        if customers.get('na_rows_dropped', 0) > 0:
            issues_data_customers['Issue Type'].append('Missing Values')
            issues_data_customers['Count'].append(customers.get('na_rows_dropped', 0))
        
        if issues_data_customers['Issue Type']:
            df_issues_customers = pd.DataFrame(issues_data_customers)
            fig = px.bar(df_issues_customers, x='Issue Type', y='Count', title='Data Quality Issues')
            st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("**Data Pipeline Dashboard** | Built with Streamlit 📊")