# -*- coding: utf-8 -*-
################################################################
import sys
import os
import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
################################################################

if sys.platform == 'linux': 
    Base = os.path.expanduser('~') + '/VKHCG'
else:
    Base = r'C:\Users\kazis\Desktop\NOTES MSC P1\Prac\DS\VKHCG'

print('################################')
print('Working Base :', Base, ' using ', sys.platform)
print('################################')

################################################################
Company = '01-Vermeulen'
InputFileName = 'Online-Retail-Billboard.xlsx'
EDSAssessDir = '02-Assess/01-EDS'
InputAssessDir = EDSAssessDir + '/02-Python'

################################################################
sFileAssessDir = Base + '/' + Company + '/' + InputAssessDir
if not os.path.exists(sFileAssessDir):
    os.makedirs(sFileAssessDir)

################################################################
sFileName = Base + '/' + Company + '/00-RawData/' + InputFileName

################################################################
# Check if the file exists
if not os.path.exists(sFileName):
    raise FileNotFoundError(f"Input file not found: {sFileName}")

df = pd.read_excel(sFileName)
print(df.shape)

# Check if required columns exist
required_columns = ['Description', 'InvoiceNo', 'Quantity', 'Country']
missing_columns = [col for col in required_columns if col not in df.columns]

if missing_columns:
    raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")

################################################################
df['Description'] = df['Description'].str.strip()
df.dropna(axis=0, subset=['InvoiceNo'], inplace=True)
df['InvoiceNo'] = df['InvoiceNo'].astype('str')

# Remove rows where 'InvoiceNo' contains 'C' (cancellations)
df = df[~df['InvoiceNo'].str.contains('C')]

# Create basket for France
basket = (df[df['Country'] == "France"]
          .groupby(['InvoiceNo', 'Description'])['Quantity']
          .sum().unstack().reset_index().fillna(0)
          .set_index('InvoiceNo'))

# Function to encode values
def encode_units(x):
    if x <= 0:
        return 0
    return 1  # if x > 0, return 1

# Apply the encoding to the basket
basket_sets = basket.applymap(encode_units)

# Drop 'POSTAGE' column if it exists
if 'POSTAGE' in basket_sets.columns:
    basket_sets.drop('POSTAGE', inplace=True, axis=1)

# Perform apriori algorithm
frequent_itemsets = apriori(basket_sets, min_support=0.07, use_colnames=True)

# Generate association rules
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
print(rules.head())

# Filter rules with specific conditions
filtered_rules = rules[(rules['lift'] >= 6) & (rules['confidence'] >= 0.8)]
print(filtered_rules)

################################################################
# Check products sales for France
sProduct1 = 'ALARM CLOCK BAKELIKE GREEN'
if sProduct1 in basket.columns:
    print(sProduct1)
    print(basket[sProduct1].sum())
else:
    print(f"Product {sProduct1} not found in the dataset.")

sProduct2 = 'ALARM CLOCK BAKELIKE RED'
if sProduct2 in basket.columns:
    print(sProduct2)
    print(basket[sProduct2].sum())
else:
    print(f"Product {sProduct2} not found in the dataset.")

################################################################
# Create basket for Germany
basket2 = (df[df['Country'] == "Germany"]
           .groupby(['InvoiceNo', 'Description'])['Quantity']
           .sum().unstack().reset_index().fillna(0)
           .set_index('InvoiceNo'))

# Apply the encoding to the basket
basket_sets2 = basket2.applymap(encode_units)

# Drop 'POSTAGE' column if it exists
if 'POSTAGE' in basket_sets2.columns:
    basket_sets2.drop('POSTAGE', inplace=True, axis=1)

# Perform apriori algorithm for Germany
frequent_itemsets2 = apriori(basket_sets2, min_support=0.05, use_colnames=True)

# Generate association rules for Germany
rules2 = association_rules(frequent_itemsets2, metric="lift", min_threshold=1)

# Filter rules for Germany with specific conditions
filtered_rules2 = rules2[(rules2['lift'] >= 4) & (rules2['confidence'] >= 0.5)]
print(filtered_rules2)

################################################################
print('### Done!! ############################################')
################################################################
