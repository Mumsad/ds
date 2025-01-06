 
import sys
import os
import pandas as pd
if sys.platform == 'linux': 
    Base = os.path.expanduser('~') + '/VKHCG'
else:
    Base = r'C:\Users\kazis\Desktop\NOTES MSC P1\Prac\DS\VKHCG'
sFileName = os.path.join(Base, '01-Vermeulen', '00-RawData', 'IP_DATA_CORE.csv')
print('Loading:', sFileName)
IP_DATA_ALL = pd.read_csv(sFileName, header=0, low_memory=False, encoding="latin-1")
sFileDir = os.path.join(Base, '01-Vermeulen', '01-Retrieve', '01-EDS', '02-Python')
if not os.path.exists(sFileDir):
    os.makedirs(sFileDir)
print('Rows:', IP_DATA_ALL.shape[0])
print('Columns:', IP_DATA_ALL.shape[1])
print('### Raw Data Set #####################################')
for col in IP_DATA_ALL.columns:
    print(f'{col}: {type(col)}')
print('### Fixed Data Set ###################################')
IP_DATA_ALL_FIX = IP_DATA_ALL.copy()
for i, col in enumerate(IP_DATA_ALL_FIX.columns):
    cNameOld = col + '     '  # Add spaces for visual representation
    cNameNew = cNameOld.strip().replace(" ", ".")  # Strip spaces and replace with dots
    IP_DATA_ALL_FIX.columns.values[i] = cNameNew  # Apply the new name
for col in IP_DATA_ALL_FIX.columns:
    print(f'{col}: {type(col)}')
print(IP_DATA_ALL_FIX.head())
print('Fixed Data Set with ID')
IP_DATA_ALL_with_ID = IP_DATA_ALL_FIX.copy()
IP_DATA_ALL_with_ID.index.names = ['RowID']
print(IP_DATA_ALL_with_ID.head())
sFileName2 = os.path.join(sFileDir, 'Retrieve_IP_DATA.csv')
IP_DATA_ALL_with_ID.to_csv(sFileName2, index=True, encoding="latin-1")
print('### Done!! ############################################')
