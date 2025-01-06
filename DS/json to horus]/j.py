import pandas as pd

# Input File Path (Updated)
sInputFileName = 'Country_Code.json'

# Load JSON data
InputData = pd.read_json(sInputFileName, orient='index')  # No encoding parameter for read_json

print('Input Data Values===================================')
print(InputData)
print('=====================================================')

# Processing Data
ProcessData = InputData

# Drop unnecessary columns
ProcessData.drop('ISO-2-CODE', axis=1, inplace=True)
ProcessData.drop('ISO-3-Code', axis=1, inplace=True)

# Rename columns
ProcessData.rename(columns={'Country': 'CountryName'}, inplace=True)
ProcessData.rename(columns={'ISO-M49': 'CountryNumber'}, inplace=True)

# Set 'CountryNumber' as the index
ProcessData.set_index('CountryNumber', inplace=True)

# Sort data by 'CountryName' in descending order
ProcessData.sort_values('CountryName', ascending=False, inplace=True)

print('Process Data Values==================================')
print(ProcessData)
print('=====================================================')

# Output File Path (Updated)
sOutputFileName = 'HORUS-JSON-Country.csv'

# Save the processed data to CSV
OutputData = ProcessData
OutputData.to_csv(sOutputFileName, index=False)

print('JSON to HORUS - Done')
print('=====================================================')
