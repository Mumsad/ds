import pandas as pd

# Input Agreement
sInputFileName = 'Country_Code.csv'
InputData = pd.read_csv(sInputFileName, encoding="latin-1")
print('Input Data Values ===== ')
print(InputData)
print('=======')

# Processing Rules
ProcessData = InputData
ProcessData.drop('ISO-2-CODE', axis=1, inplace=True)  # Corrected axis=1 and inplace=True
ProcessData.drop('ISO-3-Code', axis=1, inplace=True)  # Corrected axis=1 and inplace=True

# Rename Country and ISO-M49 columns
ProcessData.rename(columns={'Country': 'CountryName'}, inplace=True)  # Fixed syntax of rename
ProcessData.rename(columns={'ISO-M49': 'CountryNumber'}, inplace=True)  # Fixed syntax of rename

# Set new Index
ProcessData.set_index('CountryNumber', inplace=True)

# Sort data by CountryName
ProcessData.sort_values('CountryName', ascending=False, inplace=True)  # Fixed 'axis-e' to correct sort_values usage

print('Processed Data Values ==== ')
print(ProcessData)
print('=======')

# Output Agreement
OutputData = ProcessData
sOutputFileName = 'HORUS-CSV-Country.csv'  # Fixed filename variable
OutputData.to_csv(sOutputFileName, index=False)

print('CSV to HORUS - Done')
