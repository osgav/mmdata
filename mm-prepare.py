#!/usr/bin/env python
#
# osgav
# mm-prepare.py
#
# 1 turn .lua files into .py files
# 2 import .py files 
# 3 run slpp against imported data
# 4 save data to .json files
#
# https://stackoverflow.com/questions/39838489/converting-lua-table-to-a-python-dictionary
# pip install git+https://github.com/SirAnthony/slpp
#

# step 2 and 3
from MM00Data import MM00DataSavedVariables
from slpp import slpp 
tada = slpp.decode(MM00DataSavedVariables)

# step 4
import json
with open('MM00Data.json', 'w') as handle:
    handle.write(json.dumps(tada))


