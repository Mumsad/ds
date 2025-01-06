import pandas as pd
import xml.etree.ElementTree as ET

# Function to convert DataFrame to XML
def df2xml(data):
    header = data.columns
    root = ET.Element('root')
    for row in range(data.shape[0]):
        entry = ET.SubElement(root, 'entry')
        for index in range(data.shape[1]):
            schild = str(header[index])
            child = ET.SubElement(entry, schild)
            if str(data[schild][row]) != 'nan':
                child.text = str(data[schild][row])
            else:
                child.text = 'n/a'
            entry.append(child)
    result = ET.tostring(root)
    return result

# Function to convert XML to DataFrame
def xml2df(xml_data):
    root = ET.XML(xml_data)
    all_records = []
    for child in root:
        record = {}
        for subchild in child:
            record[subchild.tag] = subchild.text if subchild.text != 'n/a' else None  # Convert 'n/a' back to None
        all_records.append(record)
    return pd.DataFrame(all_records)

#=============================================================
# Load XML file and convert to DataFrame
sInputFileName = 'C:/Users/kazis/Desktop/NOTES MSC P1/Prac/DS/Country_Code.xml'  # Fixed file path with no leading spaces
with open(sInputFileName, 'r', encoding='utf-8') as file: 'C:/Users/kazis/Desktop/NOTES MSC P1/Prac/DS/Country_Code.xml'
InputData = file.read()

print('=====================================================')
print('Input Data Values===================================')
print('=====================================================')
print(InputData)
print('=====================================================')

# Convert XML to DataFrame
ProcessData = xml2df(InputData)

# Drop unnecessary columns and process data
ProcessData.drop('ISO-2-CODE', axis=1, inplace=True, errors='ignore')  # Ignore errors if column not found
ProcessData.drop('ISO-3-Code', axis=1, inplace=True, errors='ignore')  # Ignore errors if column not found
ProcessData.rename(columns={'Country': 'CountryName'}, inplace=True)
ProcessData.rename(columns={'ISO-M49': 'CountryNumber'}, inplace=True)

# Set 'CountryNumber' as index
ProcessData.set_index('CountryNumber', inplace=True)

# Sort data by 'CountryName' in descending order
ProcessData.sort_values('CountryName', ascending=False, inplace=True)

print('=====================================================')
print('Processed Data Values================================')
print('=====================================================')
print(ProcessData)
print('=====================================================')

# Output data to CSV file
sOutputFileName = 'C:/Users/kazis/Desktop/Country_Codes.csv'  # Correct output file path
ProcessData.to_csv(sOutputFileName, index=True)

print('=====================================================')
print('XML to CSV - Done')
print('=====================================================')
