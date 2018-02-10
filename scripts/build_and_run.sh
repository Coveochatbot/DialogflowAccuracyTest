#!/bin/bash

#Build and run
#Parameters:
#   - $1: dialogflow_client_access_token E.g.: 12312312312mytoken123123123

set -e #Exit on error

tox
source .tox/py35/Scripts/activate
python dialogflow_accuracy_test/main.py --dialogflow_client_access_token $1

