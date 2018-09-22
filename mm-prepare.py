#!/usr/bin/env python
#
# osgav
# mm-prepare.py
#
# 1. open .lua file
# 2. decode lua table
# 3. write as json to new file
# 4. repeat
#
# https://stackoverflow.com/questions/39838489/converting-lua-table-to-a-python-dictionary
# pip install git+https://github.com/SirAnthony/slpp
#

import os
import json

from slpp import slpp


MM_DATA_PATH = "../2018-09-22-datacopy"
# this folder should contain your MM00Data.lua, MM01Data.lua, etc files

for file in os.listdir(MM_DATA_PATH):

    if "Data.lua" in file:
        
        with open('%s/%s' % (MM_DATA_PATH, file), 'r') as handle:
            luafile = handle.readlines()
        luastring = "".join(luafile[1:])
        tada = slpp.decode(luastring)

        jsonfile = file.replace('lua', 'json')
        with open('%s/json/%s' % (MM_DATA_PATH, jsonfile), 'w') as handle:
            handle.write(json.dumps(tada))
