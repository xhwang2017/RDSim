#!/usr/bin/env python
# coding: utf-8


import xml.etree.ElementTree as ET
import pandas as pd



# OrphaCode and Inheritance information "en_product9_ages.xml" is available on this website 
# https://github.com/Orphanet/Orphadata_aggregated/tree/master/Epidemiological%20data/Rare%20diseases%20natural%20history

tree = ET.parse('en_product9_ages.xml')
root = tree.getroot()

# Extract OrphaCode and Type of Inheritance Name (lang="en")
inheritance_data = []
for disorder in root.findall(".//Disorder"):
    orpha_code = disorder.find("OrphaCode").text
    inheritance_element = disorder.find(".//TypeOfInheritanceList/TypeOfInheritance/Name[@lang='en']")
    if inheritance_element is not None:
        inheritance_data.append({
            "OrphaCode": orpha_code,
            "TypeOfInheritance": inheritance_element.text
        })



# Convert list to DataFrame
df = pd.DataFrame(inheritance_data)



print(df)



# Filter rows where TypeOfInheritance is either "Autosomal recessive" or "Autosomal dominant"
df_filtered = df[df['TypeOfInheritance'].isin(['Autosomal recessive', 'Autosomal dominant'])]

# Display the filtered DataFrame
print(df_filtered)



# Use .loc to replace 'Autosomal recessive' with 'AR' and 'Autosomal dominant' with 'AD' directly
df_filtered = df_filtered.copy()
df_filtered.loc[df_filtered['TypeOfInheritance'] == 'Autosomal recessive', 'TypeOfInheritance'] = 'AR'
df_filtered.loc[df_filtered['TypeOfInheritance'] == 'Autosomal dominant', 'TypeOfInheritance'] = 'AD'

# Display the modified DataFrame
print(df_filtered)


# Group by TypeOfInheritance and count occurrences
inheritance_group = df_filtered.groupby('TypeOfInheritance').size().reset_index(name='Count')

# Display grouped data
print(inheritance_group)



# Save DataFrame as a CSV file
df_filtered.to_csv('Orpha_Inheritance.csv', index=False)






