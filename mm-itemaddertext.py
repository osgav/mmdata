#!/usr/bin/env python
#
# osgav
# mm-itemaddertext.py
#
# send ItemAdderText field contents to plain text file
#

import json



def main():

    with open('MM00Data.json', 'r') as handle:
        mm = json.loads(handle.read())

    mmdata = 'mm["Default"]["MasterMerchant"]["$AccountWide"]["SalesData"]'
    item_adders = []
    sale_record = {}

    for sale_list in eval(mmdata):
        for item in eval(mmdata + '["%s"]' % sale_list):
            sale_record['item_desc'] = eval(mmdata + '["%s"]["%s"]["itemDesc"]' % (sale_list, item))
            sale_record['item_adder_text'] = eval(mmdata + '["%s"]["%s"]["itemAdderText"]' % (sale_list, item))
            item_adders.append(sale_record['item_adder_text'])
    
    # for itemlist in item_adders:
    #     print(len(itemlist.split("  ")))

    with open('MMItemAdderText.txt', 'w') as handle:
        for item in item_adders:
            handle.write(item + '\n')

if __name__ == "__main__":
    main()
