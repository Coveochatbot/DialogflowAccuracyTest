#!/bin/bash
set -e #Exit on error

tox
source .tox/py37/Scripts/activate
python dialogflow_accuracy_test/main.py

