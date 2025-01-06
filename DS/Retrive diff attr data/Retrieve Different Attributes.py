# -*- coding: utf-8 -*-
import sys
import os
import pandas as pd

# Define base path (ensure to use raw string or double slashes in file path)
Base = r'C:\Users\kazis\Desktop\NOTES MSC P1\Prac\DS\VKHCG'

# File path for reading the data
sFileName = os.path.join(Base, '01-Vermeulen', '00-RawData', 'IP_DATA_ALL.csv')
print('Loading:', sFileName)

# Load the CSV file with proper encoding
IP_DATA_ALL = pd.read_csv(sFileName, header=0, low_memory=False, encoding="latin-1")

# File path for saving the fixed data
sFileDir = os.path.join(Base, '01-Vermeulen', '01-Retrieve', '01-EDS', '02-Python')

# Ensure the directory exists
if not os.path.exists(sFileDir):
    os.makedirs(sFileDir)

# Display the number of rows and columns
print('Rows:', IP_DATA_ALL.shape[0])
print('Columns:', IP_DATA_ALL.shape[1])

print('### Raw Data Set #####################################')
# Loop through columns and print their names and types
for col in IP_DATA_ALL.columns:
    print(f'{col}: {type(col)}')

print('### Fixed Data Set ###################################')

# Fix column names: strip spaces and replace them with dots
IP_DATA_ALL_FIX = IP_DATA_ALL.copy()
for i, col in enumerate(IP_DATA_ALL_FIX.columns):
    cNameOld = col + '     '  # Add spaces for visual representation
    cNameNew = cNameOld.strip().replace(" ", ".")  # Strip spaces and replace with dots
    IP_DATA_ALL_FIX.columns.values[i] = cNameNew  # Apply the new name

# Display fixed column names and their types
for col in IP_DATA_ALL_FIX.columns:
    print(f'{col}: {type(col)}')

print('Fixed Data Set with ID')

# Add an index name 'RowID'
IP_DATA_ALL_with_ID = IP_DATA_ALL_FIX.copy()
IP_DATA_ALL_with_ID.index.names = ['RowID']

# Save the fixed data to CSV
sFileName2 = os.path.join(sFileDir, 'Retrieve_IP_DATA.csv')
IP_DATA_ALL_with_ID.to_csv(sFileName2, index=True, encoding="latin-1")

print('### Done!! ############################################')
