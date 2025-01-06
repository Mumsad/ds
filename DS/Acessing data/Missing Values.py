# -*- coding: utf-8 -*-
import os
import pandas as pd

# Base directory (ensure correct path handling across platforms)
Base = r'C:\Users\kazis\Desktop\NOTES MSC P1\Prac\DS\VKHCG'

# Input and Output file names
sInputFileName = 'Good-or-Bad.csv'
sOutputFileName = 'Good-or-Bad-01.csv'
Company = '01-Vermeulen'

# Create output directory if it doesn't exist
sFileDir = os.path.join(Base, Company, '02-Assess', '01-EDS', '02-Python')
if not os.path.exists(sFileDir):
    os.makedirs(sFileDir)

# Load the data
sFileName = os.path.join(Base, Company, '00-RawData', sInputFileName)
print(f"Loading: {sFileName}")
RawData = pd.read_csv(sFileName, header=0)

# Print Raw Data values and data profile
print('################################')
print('## Raw Data Values')
print('################################')
print(RawData)
print('################################')
print('## Data Profile')
print('################################')
print(f"Rows: {RawData.shape[0]}")
print(f"Columns: {RawData.shape[1]}")
print('################################')

# Save Raw Data to the output directory
sFileName = os.path.join(sFileDir, sInputFileName)
RawData.to_csv(sFileName, index=False)

# Drop columns with all NaN values
TestData = RawData.dropna(axis=1, how='all')

# Print Test Data values and data profile
print('################################')
print('## Test Data Values')
print('################################')
print(TestData)
print('################################')
print('## Data Profile')
print('################################')
print(f"Rows: {TestData.shape[0]}")
print(f"Columns: {TestData.shape[1]}")
print('################################')

# Save the processed data (Test Data) to the output directory
sFileName2 = os.path.join(sFileDir, sOutputFileName)
TestData.to_csv(sFileName2, index=False)

# Final print message
print('################################')
print('### Done!! #####################')
print('################################')
