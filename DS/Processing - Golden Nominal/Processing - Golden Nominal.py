import sys
import os
import sqlite3 as sq
import pandas as pd
from datetime import datetime, timedelta
from pytz import timezone, all_timezones
from random import randint
import uuid

# Check platform
if sys.platform == 'linux': 
    Base = os.path.expanduser('~') + '/VKHCG'
else:
    Base = r'C:\Users\kazis\Desktop\NOTES MSC P1\Prac\DS\VKHCG'

print('################################')
print('Working Base:', Base, ' using ', sys.platform)
print('################################')

Company = '04-Clark'
sInputFileName = '02-Assess/01-EDS/02-Python/Assess_People.csv'

# Set paths for SQLite databases
sDataBaseDir = Base + '/' + Company + '/03-Process/SQLite'
if not os.path.exists(sDataBaseDir):
    os.makedirs(sDataBaseDir)

sDatabaseName = sDataBaseDir + '/clark.db'
conn1 = sq.connect(sDatabaseName)

sDataVaultDir = Base + '/88-DV'
if not os.path.exists(sDataVaultDir):
    os.makedirs(sDataVaultDir)

sDatabaseName = sDataVaultDir + '/datavault.db'
conn2 = sq.connect(sDatabaseName)

# Import data
sFileName = Base + '/' + Company + '/' + sInputFileName
print('################################')
print('Loading:', sFileName)
print('################################')
RawData = pd.read_csv(sFileName, header=0, low_memory=False, encoding="latin-1")
RawData.drop_duplicates(keep='first', inplace=True)

# Generate random birthdates
start_date = datetime(1900, 1, 1, 0, 0, 0)
start_date_utc = start_date.replace(tzinfo=timezone('UTC'))

HoursBirth = 100 * 365 * 24
RawData['BirthDateUTC'] = RawData.apply(lambda row: (start_date_utc + timedelta(hours=randint(0, HoursBirth))), axis=1)

zonemax = len(all_timezones) - 1
RawData['TimeZone'] = RawData.apply(lambda row: (all_timezones[randint(0, zonemax)]), axis=1)

RawData['BirthDateISO'] = RawData.apply(lambda row: row["BirthDateUTC"].astimezone(timezone(row['TimeZone'])), axis=1)
RawData['BirthDateKey'] = RawData.apply(lambda row: row["BirthDateUTC"].strftime("%Y-%m-%d %H:%M:%S"), axis=1)
RawData['BirthDate'] = RawData.apply(lambda row: row["BirthDateISO"].strftime("%Y-%m-%d %H:%M:%S"), axis=1)
RawData['PersonID'] = RawData.apply(lambda row: str(uuid.uuid4()), axis=1)

# Prepare data for SQLite insertions
Data = RawData.copy()
Data.drop(['BirthDateUTC', 'BirthDateISO'], axis=1, inplace=True)
indexed_data = Data.set_index(['PersonID'])

# Insert into 'Process_Person' table
sTable = 'Process_Person'
print('Storing:', sDatabaseName, ' Table:', sTable)
indexed_data.to_sql(sTable, conn1, if_exists="replace")

# Person Hub
PersonHubRaw = Data[['PersonID', 'FirstName', 'SecondName', 'LastName', 'BirthDateKey']]
PersonHubRaw['PersonHubID'] = RawData.apply(lambda row: str(uuid.uuid4()), axis=1)
PersonHub = PersonHubRaw.drop_duplicates(keep='first', inplace=False)
indexed_PersonHub = PersonHub.set_index(['PersonHubID'])
sTable = 'Hub-Person'
print('Storing:', sDatabaseName, ' Table:', sTable)
indexed_PersonHub.to_sql(sTable, conn2, if_exists="replace")

# Person Satellite Gender
PersonSatelliteGenderRaw = Data[['PersonID', 'FirstName', 'SecondName', 'LastName', 'BirthDateKey', 'Gender']]
PersonSatelliteGenderRaw['PersonSatelliteID'] = RawData.apply(lambda row: str(uuid.uuid4()), axis=1)
PersonSatelliteGender = PersonSatelliteGenderRaw.drop_duplicates(keep='first', inplace=False)
indexed_PersonSatelliteGender = PersonSatelliteGender.set_index(['PersonSatelliteID'])
sTable = 'Satellite-Person-Gender'
print('Storing:', sDatabaseName, ' Table:', sTable)
indexed_PersonSatelliteGender.to_sql(sTable, conn2, if_exists="replace")

# Person Satellite Birthday
PersonSatelliteBirthdayRaw = Data[['PersonID', 'FirstName', 'SecondName', 'LastName', 'BirthDateKey', 'TimeZone', 'BirthDate']]
PersonSatelliteBirthdayRaw['PersonSatelliteID'] = RawData.apply(lambda row: str(uuid.uuid4()), axis=1)
PersonSatelliteBirthday = PersonSatelliteBirthdayRaw.drop_duplicates(keep='first', inplace=False)
indexed_PersonSatelliteBirthday = PersonSatelliteBirthday.set_index(['PersonSatelliteID'])
sTable = 'Satellite-Person-Names'
print('Storing:', sDatabaseName, ' Table:', sTable)
indexed_PersonSatelliteBirthday.to_sql(sTable, conn2, if_exists="replace")

# Output to CSV
sFileDir = Base + '/' + Company + '/03-Process/01-EDS/02-Python'
if not os.path.exists(sFileDir):
    os.makedirs(sFileDir)

sOutputFileName = sTable + '.csv'
sFileName = sFileDir + '/' + sOutputFileName
print('################################')
print('Storing:', sFileName)
print('################################')
RawData.to_csv(sFileName, index=False)

# Vacuum Databases
print('################')
print('Vacuum Databases')
sSQL = "VACUUM;"
conn1.execute(sSQL)
conn2.execute(sSQL)
print('################')

print('### Done!! ############################################')
