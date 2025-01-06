# -*- coding: utf-8 -*-
import sys
import os
import pandas as pd

# Disable chained assignment warnings
pd.options.mode.chained_assignment = None

# Define the base directory
Base = r'C:\Users\kazis\Desktop\NOTES MSC P1\Prac\DS\VKHCG'

# Print working base
print('################################')
print('Working Base :', Base, ' using Windows')
print('################################')

# Define input and output file paths
sInputFileName1 = '01-Retrieve/01-EDS/01-R/Retrieve_Country_Code.csv'
sInputFileName2 = '01-Retrieve/01-EDS/02-Python/Retrieve_Router_Location.csv'
sInputFileName3 = '01-Retrieve/01-EDS/01-R/Retrieve_IP_DATA.csv'
sOutputFileName = 'Assess-Network-Routing-Company.csv'
Company = '01-Vermeulen'

# ###### Import Country Data ######
sFileName = os.path.join(Base, Company, sInputFileName1)
print('################################')
print('Loading :', sFileName)
print('################################')
CountryData = pd.read_csv(sFileName, header=0, low_memory=False, encoding="latin-1")
print('Loaded Country:', CountryData.columns.values)
print('################################')

# Assess and clean Country Data
print('################################')
print('Changed :', CountryData.columns.values)
CountryData.rename(columns={'Country': 'Country_Name', 'ISO-2-CODE': 'Country_Code'}, inplace=True)
CountryData.drop(['ISO-M49', 'ISO-3-Code', 'RowID'], axis=1, inplace=True)
print('To :', CountryData.columns.values)
print('################################')

# ###### Import Company Data ######
sFileName = os.path.join(Base, Company, sInputFileName2)
print('################################')
print('Loading :', sFileName)
print('################################')
CompanyData = pd.read_csv(sFileName, header=0, low_memory=False, encoding="latin-1")
print('Loaded Company :', CompanyData.columns.values)
print('################################')

# Assess and clean Company Data
print('################################')
print('Changed :', CompanyData.columns.values)
CompanyData.rename(columns={'Country': 'Country_Code'}, inplace=True)
print('To :', CompanyData.columns.values)
print('################################')

# ###### Import Customer Data ######
sFileName = os.path.join(Base, Company, sInputFileName3)
print('################################')
print('Loading :', sFileName)
print('################################')
CustomerRawData = pd.read_csv(sFileName, header=0, low_memory=False, encoding="latin-1")
print('################################')
print('Loaded Customer :', CustomerRawData.columns.values)
print('################################')

# Clean Customer Data (drop rows with NaN values)
CustomerData = CustomerRawData.dropna(axis=0, how='any')
print('################################')
print('Remove Blank Country Code')
print(f'Reduce Rows from {CustomerRawData.shape[0]} to {CustomerData.shape[0]}')
print('################################')

# Rename Customer Data columns
print('################################')
print('Changed :', CustomerData.columns.values)
CustomerData.rename(columns={'Country': 'Country_Code'}, inplace=True)
print('To :', CustomerData.columns.values)
print('################################')

# ###### Merge Company and Country Data ######
print('################################')
print('Merge Company and Country Data')
print('################################')
CompanyNetworkData = pd.merge(CompanyData, CountryData, how='inner', on='Country_Code')

# Rename columns to add "Company_" prefix
print('################################')
print('Change ', CompanyNetworkData.columns.values)
CompanyNetworkData = CompanyNetworkData.rename(columns={col: f'Company_{col}' for col in CompanyNetworkData.columns})
print('To ', CompanyNetworkData.columns.values)
print('################################')

# ###### Saving the final merged data ######
sFileDir = os.path.join(Base, Company, '02-Assess', '01-EDS', '02-Python')
if not os.path.exists(sFileDir):
    os.makedirs(sFileDir)

sFileName = os.path.join(sFileDir, sOutputFileName)
print('################################')
print('Storing :', sFileName)
print('################################')
CompanyNetworkData.to_csv(sFileName, index=False, encoding="latin-1")

# Print done message
print('################################')
print('### Done!! #####################')
print('################################')
