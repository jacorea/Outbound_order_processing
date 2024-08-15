import streamlit as st
import pandas as pd
from io import StringIO

def process_csv(file):
    # Read the CSV file
    df = pd.read_csv(file)
    
    # Convert Planned Shipped Date from yyyymmdd to mm/dd/yyyy
    df['Planned Ship Date'] = pd.to_datetime(df['Planned Ship Date'], format='%Y%m%d').dt.strftime('%m/%d/%Y')
    
    # Move the Carrier column data to Shipping Conditions column
    df['Shipping Conditions'] = df['Carrier']
    
    # Clear the original Carrier column but keep it in the DataFrame
    df['Carrier'] = ''
    
    # Group by Delivery Number, Product ID, and aggregate the Quantity
    df = df.groupby(['Delivery Number', 'Product ID'], as_index=False).agg({
        'Company Name/Contact Name': 'first',
        'Address 1': 'first',
        'Address 2': 'first',
        'Address 3': 'first',
        'City': 'first',
        'State': 'first',
        'Postal Code': 'first',
        'Country': 'first',
        'Quantity': 'sum',
        'Sales Order': 'first',
        'Shipping Conditions': 'first',
        'Delivery Instructions': 'first',
        'Carrier': 'first',
        'Planned Ship Date': 'first'
    })
    
    # Reorder columns
    df = df[['Delivery Number', 'Company Name/Contact Name', 'Address 1', 'Address 2', 'Address 3',
             'City', 'State', 'Postal Code', 'Country', 'Product ID', 'Quantity', 'Sales Order',
             'Shipping Conditions', 'Delivery Instructions', 'Carrier', 'Planned Ship Date']]
    
    return df

def main():
    st.title('CSV File Processor')
    
    # File upload
    uploaded_file = st.file_uploader('Upload your CSV file', type=['csv'])
    
    if uploaded_file is not None:
        # Process the file
        processed_df = process_csv(uploaded_file)
        
        # Display the processed DataFrame
        st.write('Processed Data:')
        st.dataframe(processed_df)
        
        # Provide a download button for the processed CSV without an index
        csv_buffer = StringIO()
        processed_df.to_csv(csv_buffer, encoding='utf-8', index=False)  # Remove the index
        csv_data = csv_buffer.getvalue()

        st.download_button(
            label="Download Processed CSV",
            data=csv_data,
            file_name='processed_file.csv',
            mime='text/csv'
        )

if __name__ == "__main__":
    main()
