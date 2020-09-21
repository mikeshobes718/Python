#!/usr/bin/env python

import requests
import json
import subprocess
import argparse
import sys
import time

subprocess.call(["clear"])

headers = {'Content-type':'application/json'}

parser = argparse.ArgumentParser(description='Note: None of these arguments are mandatory',
        usage='use "python %(prog)s -h" for help\nNote: *** Astericks represent mandatory fields',
        formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-u',
                    '--url',
                    type=str,
                    help='Enter Requests URL')
parser.add_argument('-k',
                    '--key',
                    type=str,
                    help='Enter Requests Key')
parser.add_argument('-s',
                    '--secret',
                    type=str,
                    help='Enter Requests Secret')                                        

args = parser.parse_args()

# SET REQUEST CREDENTIALS MANUALLY
# MAKE SURE TO REVERT CREDENTIALS BACK TO NONE IN THE SCRIPT!!!!!!!
url = None
key = None
secret = None

requests_statically_set = False

# print len(sys.argv)
if all(v is None for v in [url, key, secret]):
    if all(v is not None for v in [args.url, args.key, args.secret]):
        try:
            url = args.url
            key = args.key
            secret = args.secret
        except:
            subprocess.call(["clear"])
            print("ERROR: Please re-run the program with proper input!")
            sys.exit(2)
    elif 3 <= len(sys.argv) <= 5:
        # SET REQUESTS CREDENTIALS DYNAMICALLY
        print("ERROR: You didn't specify all of the necessary arguments '-u', '-k', '-s'\nPlease enter your requests credentials below!\n")
        url = raw_input("Enter Requests URL: ")
        key = raw_input("Enter Requests Key: ")
        secret = raw_input("Enter Requests Secret: ")
        if all(v is not None for v in [url, key, secret]):
            pass
        else:
            subprocess.call(["clear"])
            "ERROR: Please Specify Requests Credentials!"
            sys.exit(1)
    else:
        # SET REQUESTS CREDENTIALS DYNAMICALLY
        url = raw_input("Enter Requests URL: ")
        key = raw_input("Enter Requests Key: ")
        secret = raw_input("Enter Requests Secret: ")
        if all(v is not None for v in [url, key, secret]):
            pass
        else:
            subprocess.call(["clear"])
            "ERROR: Please Specify Requests Credentials!"
            sys.exit(1)
else:
    requests_statically_set = True
    counter = 0
    while counter < 3:
        subprocess.call(["clear"])
        print("HELP: You modified the program to use your requests credentials statically!\nPlease remember to set the Requests Credentials back to python's reserved keyword None")
        time.sleep(0.4)
        subprocess.call(["clear"])
        time.sleep(0.4)
        counter += 1
    subprocess.call(["clear"])
    print("HELP: You modified the program to use your requests credentials statically!\nPlease remember to set the Requests Credentials back to python's reserved keyword None")
    time.sleep(2)
    pass

response = requests.get(url, auth=(key, secret), headers=headers)

def print_request_information():
    subprocess.call(["clear"])
    print("Requests URL: " + url)
    print("Requests Key: " + key)
    print("Requests Secret: " + secret)
    print("\n")

    print("REQUEST INFORMATION\n-------------------")
    print("URL: " + url + "\n")
    if(200 <= response.status_code <= 299):
        print("STATUS: OK")
    elif(400 <= response.status_code <= 499):
        print("ERROR: Unauthorized!")
    else:
        print(json_string)
    print("\nRESPONSE: " + str(response.status_code))

print_request_information()

if(requests_statically_set == True):
    time.sleep(1)
    print("\nHELP: You modified the program to use your requests credentials statically!\nPlease remember to set the Requests Credentials back to python's reserved keyword None")
    counter_two = 0 
    while counter_two < 31:
        print_request_information()
        print("\nHELP: You modified the program to use your requests credentials statically!\nPlease remember to set the Requests Credentials back to python's reserved keyword None\n")
        time.sleep(2)
        subprocess.call(["clear"])
        time.sleep(0.3)
        counter_two += 1

binary = response.content
output = json.loads(binary)
json_string = json.dumps(output, indent=4)

# print json_string
print("")
