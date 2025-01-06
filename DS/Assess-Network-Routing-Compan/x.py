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
# Path for storing files
sFileAssessDir = Base + '/' + Company + '/' + InputAssessDir
if not os.path.exists(sFileAssessDir):
    os.makedirs(sFileAssessDir)

################################################################
# Path for the input file
sFileName = Base + '/' + Company + '/00-RawData/' + InputFileName

################################################################
# Check if the file exists
if not os.path.exists(sFileName):
    raise FileNotFoundError(f"Input file not found: {sFileName}")

df = pd.read_excel(sFileName)
print(f"Dataset loaded. Shape: {df.shape}")

# Clean data
df['Description'] = df['Description'].str.strip()
df.dropna(axis=0, subset=['InvoiceNo'], inplace=True)
df['InvoiceNo'] = df['InvoiceNo'].astype('str')

# Filter out cancellations (InvoiceNo contains 'C')
df = df[~df['InvoiceNo'].str.contains('C')]

# Prepare basket data (France)
basket = (df[df['Country'] == "France"]
          .groupby(['InvoiceNo', 'Description'])['Quantity']
          .sum().unstack().reset_index().fillna(0)
          .set_index('InvoiceNo'))

# Function to encode the data (binary encoding for the apriori algorithm)
def encode_units(x):
    if x <= 0:
        return 0
    return 1  # if x > 0, return 1

basket_sets = basket.applymap(encode_units)

# Drop the 'POSTAGE' column if it exists
if 'POSTAGE' in basket_sets.columns:
    basket_sets.drop('POSTAGE', inplace=True, axis=1)

# Run apriori algorithm
frequent_itemsets = apriori(basket_sets, min_support=0.07, use_colnames=True)

# Generate association rules
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)

# Filter rules based on lift and confidence
filtered_rules = rules[(rules['lift'] >= 6) & (rules['confidence'] >= 0.8)]
print(f"Filtered rules (Lift >= 6 and Confidence >= 0.8):\n{filtered_rules.head()}")

# Export the rules to a CSV file
sOutputFileName = 'association_rules_report.csv'
sOutputFilePath = sFileAssessDir + '/' + sOutputFileName
filtered_rules.to_csv(sOutputFilePath, index=False)
print(f"Association rules report saved to {sOutputFilePath}")

# Check product sales for France
sProduct1 = 'ALARM CLOCK BAKELIKE GREEN'
if sProduct1 in basket.columns:
    print(f"{sProduct1} sold quantity: {basket[sProduct1].sum()}")
else:
    print(f"Product {sProduct1} not found in the dataset.")

sProduct2 = 'ALARM CLOCK BAKELIKE RED'
if sProduct2 in basket.columns:
    print(f"{sProduct2} sold quantity: {basket[sProduct2].sum()}")
else:
    print(f"Product {sProduct2} not found in the dataset.")

################################################################
# Generate basket for Germany
basket2 = (df[df['Country'] == "Germany"]
           .groupby(['InvoiceNo', 'Description'])['Quantity']
           .sum().unstack().reset_index().fillna(0)
           .set_index('InvoiceNo'))

# Apply binary encoding for the German basket
basket_sets2 = basket2.applymap(encode_units)

# Drop 'POSTAGE' column if it exists
if 'POSTAGE' in basket_sets2.columns:
    basket_sets2.drop('POSTAGE', inplace=True, axis=1)

# Perform apriori for Germany
frequent_itemsets2 = apriori(basket_sets2, min_support=0.05, use_colnames=True)

# Generate association rules for Germany
rules2 = association_rules(frequent_itemsets2, metric="lift", min_threshold=1)

# Filter the rules for Germany
filtered_rules2 = rules2[(rules2['lift'] >= 4) & (rules2['confidence'] >= 0.5)]
print(f"Filtered rules for Germany (Lift >= 4 and Confidence >= 0.5):\n{filtered_rules2.head()}")

# Export the rules for Germany to a CSV file
sOutputFileName2 = 'germany_association_rules_report.csv'
sOutputFilePath2 = sFileAssessDir + '/' + sOutputFileName2
filtered_rules2.to_csv(sOutputFilePath2, index=False)
print(f"Germany association rules report saved to {sOutputFilePath2}")

################################################################
print('### Report Generation Completed ############################################')
################################################################
