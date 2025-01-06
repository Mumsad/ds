import pandas as pd
# File paths
InputFileName = 'IP_DATA_CORE.csv'
OutputFileName = 'Retrieve_Router_Location.csv'
Base = 'C:/Users/kazis/Desktop/NOTES MSC P1/Prac/DS/VKHCG'
print('################################')
print('Working Base:', Base)
print('################################')
# File path for CSV file
sFileName = Base + '/01-Vermeulen/00-RawData/' + InputFileName
print('Loading :', sFileName)
# Load the data
IP_DATA_ALL = pd.read_csv(sFileName, header=0, low_memory=False,
                          usecols=['Country', 'Place Name', 'Latitude', 'Longitude'], encoding="latin-1")
# Rename columns to make them consistent
IP_DATA_ALL.rename(columns={'Place Name': 'Place_Name'}, inplace=True)
# Filter data for 'London'
LondonData = IP_DATA_ALL.loc[IP_DATA_ALL['Place_Name'] == 'London']
AllData = LondonData[['Country', 'Place_Name', 'Latitude']]
print('All Data:')
print(AllData)
# Calculate the mean and standard deviation for Latitude, grouped by Country and Place_Name
MeanData = AllData.groupby(['Country', 'Place_Name'])['Latitude'].mean()
StdData = AllData.groupby(['Country', 'Place_Name'])['Latitude'].std()
# Merge the mean and std back into the AllData
AllData = AllData.merge(MeanData, on=['Country', 'Place_Name'], suffixes=('', '_Mean'))
AllData = AllData.merge(StdData, on=['Country', 'Place_Name'], suffixes=('', '_Std'))
# Calculate upper and lower bounds based on mean and standard deviation
AllData['UpperBound'] = AllData['Latitude_Mean'] + AllData['Latitude_Std']
AllData['LowerBound'] = AllData['Latitude_Mean'] - AllData['Latitude_Std']
print('Outliers:')
# Outliers above the Upper Bound
OutliersHigher = AllData[AllData['Latitude'] > AllData['UpperBound']]
print('Higher than Upper Bound:')
print(OutliersHigher)
# Outliers below the Lower Bound
OutliersLower = AllData[AllData['Latitude'] < AllData['LowerBound']]
print('Lower than Lower Bound:')
print(OutliersLower)
# Data that is not an outlier
OutliersNot = AllData[(AllData['Latitude'] >= AllData['LowerBound']) & 
                       (AllData['Latitude'] <= AllData['UpperBound'])]
print('Not Outliers:')
print(OutliersNot)
