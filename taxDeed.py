#!/user/bin/env python3 
"""
taxDeed.py: This program is used for tax deed purposes.
Requirements: python2.7 or later.

Error Codes:
------------
1) Endpoint is none. 
2) Endpoint authentication failed. 
"""

__author__ = "Michael Shobitan"
__copyright__ = "Copyright 2020, UIF Platform Engineering"
__credits__ = ["Michael Shobitan"]
__license__ = "UIF"
__version__ = "0.1.2"
__maintainer__ = "Michael Shobitan"
__email__ = "michael.shobitan@yahoo.com"
__status__ = "Development"

import os
import re
import sys
import csv
import json
import time
import atexit
import shutil
import locale
import urllib3
import inspect
import argparse
import requests
import subprocess
import pandas as pd
from columnar import columnar
from collections import defaultdict
locale.setlocale(locale.LC_ALL, 'en_US')
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

temp = sys.stdout

fileDate = (time.strftime('%Y%m%d'))
fileTime = (time.strftime('%H%M%S'))

headers = {'Content-type':'application/json'}
endpoints = ['UIF-DRM1P', 'UIF-SOM1D']

if(__name__ == "__main__"):
    parser = argparse.ArgumentParser(
            usage='use "python %(prog)s -h" for help',
            formatter_class=argparse.RawTextHelpFormatter,
            add_help=False)                                         

    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                        help='''Show this help message and exit.

arguments for cluster creation
    -e|--endpoint ENDPOINT, Rancher Endpoint
    -f|--fileName FILENAME, Tax Deed File
    -pl|--printLineCount PRINTLINECOUNT, Number of Lines to Print
''')                                  

    requiredNamed = parser.add_argument_group('required arguments')
                                    
    requiredNamed.add_argument('-e',
                        '--endpoint',
                        choices=endpoints,
                        type=str,
                        help=argparse.SUPPRESS)
    requiredNamed.add_argument('-f',
                        '--fileName',
                        type=str,
                        required=True,
                        help=argparse.SUPPRESS)
    parser.add_argument('-pl',
                        '--printLineCount',
                        type=int,
                        help=argparse.SUPPRESS)

    args = parser.parse_args()

taxDeedListFileCSV = args.fileName + '.csv'
totalYearsDelinquentCSV = 'totalYearsDelinquent.csv'
filesToDelete = [taxDeedListFileCSV, totalYearsDelinquentCSV]

def error_handling():
    unexpected_error = ("Unexpected error:", sys.exc_info()[0])
    error = (sys.exc_info()[1])
    if("UPDATE_IN_PROGRESS" in str(error)):
        print("ERROR: The current cluster is in UPDATE_IN_PROGRESS state and can not be updated.")
    elif("No updates are to be performed" in str(error)):
        print("INFO: No updates are to be performed.")
    elif("No cluster found for name" in str(error)):
        print("EEROR: Cluster not found!")
    elif("list index out of range" in str(error)):
        print("ERROR: Please check your tag options!")
    elif("is in UPDATE_ROLLBACK_FAILED state" in str(error)):
        print("INFO: " + cluster + " is in update rollback failed state, cannot be updated.")
    elif("ResourceInUseException" in str(error)):
        print("INFO: " + cluster + " currently has update in progress!")
    elif("Cluster is already at the desired configuration" in str(error)):
        print("INFO: " + cluster + " is already at the desired configuration!")
    elif("No changes needed for the logging config provided" in str(error)):
        print("INFO: " + cluster + " is already at the desired configuration!")
    else:
        print("Unexpected error:", sys.exc_info()[1])
        raise
        print("ERROR: Unknown error, exiting...")
        removeAnsibleJSON_File()
        sys.exit(13)

def get_env_creds(argument):
    switch = {
        "UIF-DRM1P" : {"env_url" : "http://uif-drm1p.yahoo.com/v3",
                 "key" : "token-c8s9d",
                 "secret" : "sd7r7wwd4g7wzg86h7xjzxfgkqttqw6n9vxnxxk6k6vpx8t7rmg9dg",
                    },
        "UIF-SOM1D" : {"env_url" : "http://uif-som1d.yahoo.com/v3",
                 "key" : "toekn-xgswk",
                 "secret" : "hf2f52jmdtszlw9wx64d68dz2rrfdb9ls8vh87mmkp48gv98kl6w6n",
                    },
    }
    data = switch.get(argument, "ERROR: Invalid Environment!")

    env_url = data['env_url']
    key = data['key']
    secret = data['secret']

    return env_url, key, secret

endpointList = ['UIF-DRM1P', 'UIF-SOM1D']

taxDeedListFileExcel = args.fileName + '.xlsx'

cd = os.chdir('/Users/mike/Documents/Life/Business/United Investments/Tax Deed List (Auction)')

data_xls = pd.read_excel(taxDeedListFileExcel, 'Sheet1', index_col=None)
data_xls.to_csv(taxDeedListFileCSV, index=False, header=1, encoding='utf-8')
with open(taxDeedListFileCSV, 'r') as f:
    d_reader = csv.DictReader(f)

    headers = d_reader.fieldnames

    data = []
    for line in d_reader:
        row = []
        for header in headers:
            row.append(line[header])
        
        data.append(row)

table = columnar(data, headers, no_borders=True)
# print(table)

addressYearsDelinquentHighest = ''
totalYearsDelinquentHighest = 0
totalYearsDelinquentHighestOO = ''

addressBalanceHighest = ''
balanceHighest = 0
balanceHighestOO = ''

addressPropertyValueHighest = ''
propertyValueHighest = 0
propertyValueHighestOO = ''

highestValueDict = {}
for row in data:
    address = (row[0])
    ownerOccupied = (row[1])
    totalYearsDelinquent = (row[2])
    balance = (row[4])
    propertyValue = (row[5])
    if(totalYearsDelinquent != ''):
        totalYearsDelinquent = float(totalYearsDelinquent)
        if(totalYearsDelinquent > totalYearsDelinquentHighest):
            addressYearsDelinquentHighest = address
            totalYearsDelinquentHighestOO = ownerOccupied
            totalYearsDelinquentHighest = totalYearsDelinquent

    if(balance != ''):
        balance = float(balance)
        if(balance > balanceHighest):
            addressBalanceHighest = address
            balanceHighestOO = ownerOccupied
            balanceHighest = balance

    if(propertyValue != ''):
        propertyValue = float(propertyValue)
        if(propertyValue > propertyValueHighest):
            addressPropertyValueHighest = address
            propertyValueHighestOO = ownerOccupied
            propertyValueHighest = propertyValue
    else:
        # print('INFO: No value')
        pass

cd = os.chdir('/Users/mike/Documents/Scripts/Business/United Investments')
sys.stdout = open('log.txt', 'w')
cd = os.chdir('/Users/mike/Documents/Life/Business/United Investments/Tax Deed List (Auction)')

print('Tax Delinquent Sale: ' + args.fileName + '\n')

print('INFO: Most Years Delinquent \'' + addressYearsDelinquentHighest + '\'')
print('INFO: Owner Occupied ' + totalYearsDelinquentHighestOO)
print('INFO: Years ' + str(int(totalYearsDelinquentHighest)))

print('\nINFO: Highest Tax Balance \'' + addressBalanceHighest + '\'')
print('INFO: Owner Occupied ' + balanceHighestOO)
balanceHighest = locale.format_string("%.2f", balanceHighest, grouping=True)
print('INFO: Balance $' + str(balanceHighest))

print('\nINFO: Highest Property Value \'' + addressPropertyValueHighest + '\'')
print('INFO: Owner Occupied ' + propertyValueHighestOO)
propertyValueHighest = locale.format_string("%.2f", propertyValueHighest, grouping=True)
print('INFO: Balance $' + str(propertyValueHighest))

df = pd.read_csv(taxDeedListFileCSV)
df = df.sort_values('Total Years Deliquent', ascending=False)
df.to_csv(totalYearsDelinquentCSV, index=False)

with open(totalYearsDelinquentCSV, 'r') as f:
    d_reader = csv.DictReader(f)

    headers = d_reader.fieldnames

    data = []
    printLineCounter = 0
    if(args.printLineCount is None):
        printLineCount = 5
    else:
        printLineCount = args.printLineCount

    if(printLineCount < 10):
        print('\nINFO: Top ' + str(printLineCount) + ' Total Years Deliquent Properties\n--------------------------------------------')
    elif(printLineCount < 100):
        print('\nINFO: Top ' + str(printLineCount) + ' Total Years Deliquent Properties\n---------------------------------------------')
    elif(printLineCount >= 100):
        print('\nINFO: Top ' + str(printLineCount) + ' Total Years Deliquent Properties\n----------------------------------------------')

    for line in d_reader:
        row = []
        for header in headers:
            if(header == 'Total Years Deliquent'):
                row.append(line[header])
                if(line['Total Years Deliquent'] != ''):
                    if(printLineCounter < printLineCount):
                        printLineCounter += 1
                        print(str(printLineCounter) + ') ' + line['Address'] + ', ' + str(int(float(line[header]))) + ' years deliquent')
                    else:
                        break
        
        data.append(row)

table = columnar(data, headers, no_borders=True)
# print(table)

sys.stdout.close()
sys.stdout = temp   
# print("back to normal")    

for thisFile in filesToDelete:
    if(os.path.isfile(thisFile)):
        os.remove(thisFile)
