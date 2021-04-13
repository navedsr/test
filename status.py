#!/bin/bash/env python3

############ Website Status Check ###########
# Language      :       Python 3            #
# Environment   :       Production          #
# Created       :       12/04/2021          #
# By            :       Syed Rafiq          #
#############################################

#############################################
#           Import Library Block            #
#############################################
import sys
import requests
import json
import datetime
import re
import urllib.error
from requests.exceptions import Timeout
############ Block End ######################


#############################################
#           User Input Block                #
#############################################
def multi_input():
    print('Type website URLs and Press Enter')
    try:
        while True:
            data=input()    # multi-line input
            if not data:         
                break
            yield data
    except KeyboardInterrupt: # input sequence breaks if press enter
        return
    
userInput = list(multi_input()) # storing user input in an array
############ Block End ######################


#############################################
#           URL Status Check Block          #
#############################################

# Standard Output and Standard Error
stdout_fileno = sys.stdout
stderr_fileno = sys.stderr
  
# Redirect sys.stdout to the file
sys.stdout = open('Output.json', 'w')
sys.stderr = open('Errors.txt', 'w')

# Loop to go through every url in array i.e.userInput
for i in range(len(userInput)):
    datentime = datetime.datetime.now()

    # validates url format before checking status
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    # Checks for valid URL format (e.g. http:// OR https://)
    if re.match(regex, userInput[i]) is not None: 

        # for all valid format urls, run below code
        try:
            response = requests.get(userInput[i], timeout=10) # timeout check

        # if times-out then run below code
        except Timeout as timout_err:
            x = {
            "URL": userInput[i],
            "Error": 'URL Timeout',
            }
            #print (" ### Exception Block - 1 Start ### ")
            sys.stderr.write(f'Timeout Error: \n {timout_err}'+'\n')  # errors in a Errors.txt file            
            sys.stdout.write(json.dumps (x, indent=4, separators=(", ", " : "))+'\n') # output in Output.json file
            stdout_fileno.write(json.dumps(x, indent=4, separators=(", ", " : "))+'\n') # output on screen
            #print (" ### Exception Block - 1 End ### ")

        # if any other exception occurs then run below code
        except Exception as err:
            x = {
            "URL": userInput[i],
            "Error": 'Exception',
            }
            #print (" ### Exception Block - 3 Start ### ")
            sys.stderr.write(f'Other Exception: \n {err}' + '\n')  # errors in a Errors.txt file            
            sys.stdout.write(json.dumps(x, indent=4, separators=(", ", " : "))+'\n') # output in Output.json file
            stdout_fileno.write(json.dumps(x, indent=4, separators=(", ", " : "))+'\n') # output on screen
            #print (" ### Exception Block - 3 End ### ")

        # if website exists but page not found then run below code        
        else:
            x = {
            "URL": userInput[i],
            "Status_code": response.status_code,
            #"Content_length": int(response.headers['Content-Length']),
            "Date": datentime.strftime("%a" + ", " + "%d " + "%b " + "%Y " + "%X " + "%Z")
            }
            #print (" ### Exception Block - 5 Start ### ")
            sys.stdout.write(json.dumps(x, indent=4, separators=(", ", " : "))+'\n') # output in Output.json file
            stdout_fileno.write(json.dumps(x, indent=4, separators=(", ", " : "))+'\n') # output on screen
            #print (" ### Exception Block - 5 End ### ")

    # for all invalid format urls run below code        
    else:
        x = {
        "URL": userInput[i],
        "Error": 'Invalid URL',
        }
        #print (" ### Exception Block - 6 Start ### ")
        sys.stdout.write(json.dumps(x, indent=4, separators=(", ", " : "))+'\n') # output in Output.json file
        sys.stderr.write("Invalid URL: " + userInput[i] + '\n' + "URL is not starting with http:// OR https:// OR Invalid character(s) found in URL" + '\n')  # errors in a Errors.txt file
        stderr_fileno.write(json.dumps(x, indent=4, separators=(", ", " : "))+'\n') # output on screen
        #print (" ### Exception Block - 6 End ### ")

############ Block End ######################

# Close the files
stdout_fileno.write("Files created:" + '\n' + "Output.json and Errors.txt" + '\n' +" ## Thank You ##"+'\n') # output in Output.json file
sys.stdout.close()
sys.stderr.close()

