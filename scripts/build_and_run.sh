#!/bin/bash

#Build and run
#Parameters:
#   - $1: Path to client secret json file

set -e #Exit on error

tox
source .tox/py35/Scripts/activate

source scripts/set_credentials.sh $1
python dialogflow_accuracy_test/main.py

