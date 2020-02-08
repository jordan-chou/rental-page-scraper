#!/usr/bin/python

import csv
from collections import defaultdict
from requests import get
from bs4 import BeautifulSoup
import pandas as pd


csvDict = defaultdict(list)

try:
    with open("RentScraper.csv", 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            csvDict['Address'].append(row['Address'])
            csvDict['Rent'].append(row['Rent'])
            csvDict['Bedrooms'].append(row['Bedrooms'])
            csvDict['Webpage'].append(row['Webpage'])
except:
    pass

# Extracts homepage from url
def extract_homepage(url):
    thirdSlash = -1
    for i in range(0, 3):
        thirdSlash = url.find('/', thirdSlash+1)
    return url[:thirdSlash+1]

url = input("Submit webpage: ")
print()



# Declare info
address = ""
rent = ""
beds = ""

website = extract_homepage(url)  # Gets homepage from URL

if website == 'https://www.royallepage.ca/':
    r = get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    data = soup.find('div', id='rlp-data')
    address = data['data-address1']
    rent = "$"+data['data-price'].replace(' ','').strip()
    beds = data['data-beds']
else:
    print("Webpage not Supported")
    exit()


print("Address: " + address)
print("Monthly Rent: " + rent)
print("Number of beds: " + beds)
print("Link to page: " + url)

# Store into dictionary
csvDict['Address'].append(address)
csvDict['Rent'].append(rent)
csvDict['Bedrooms'].append(beds)
csvDict['Webpage'].append(url)



df = pd.DataFrame(csvDict)

print("\nSaving to RentScraper.csv")
df.to_csv('RentScraper.csv', index=False)

exit()
