#!/usr/bin/env python
#
# osgav
# mm-import.py
#
# 1 open json data files
# 2 parse data into sale_record's
# 3 send sale_record's to elasticsearch
#


import json
from elasticsearch import Elasticsearch


def send_elastic_doc(es, elastic_index, elastic_doc):
    publish = es.index(index=elastic_index, doc_type='_doc', body=elastic_doc)
    # publish = es.index(index=elastic_index, doc_type='_doc', body=elastic_doc, id=elastic_doc['id'])
    # including an id helps elasticsearch auto de-dup things - revisit this later...


def create_elastic_doc(sale_record):
    elastic_doc = sale_record
    elastic_doc['timestamp'] = str(sale_record['timestamp']) + "000"
    # do other things to elastic_doc as desired
    # e.g. parse ItemAdderText into separate fields
    return elastic_doc


def setup_elastic_index(es, index_name):
    '''
    setup elasticsearch index and field mappings
    '''
    timestamp_mapping = {
        "mappings": {
            "_doc": {
                "properties": {
                    "timestamp": {
                        "type": "date"
                    }
                }
            }
        }
    }
    set_timestamp_mapping = es.indices.create(index=index_name, ignore=400, body=timestamp_mapping)
    print("[+] setup_elastic_index: %s" % (set_timestamp_mapping))


def setup_elastic_connection():
    '''
    connect to localhost elasticsearch instance
    '''
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    return es


def main():

    elastic_index_name = "mm-data-001"
    es = setup_elastic_connection()
    setup_elastic_index(es, elastic_index_name)

    with open('MM00Data.json', 'r') as handle:
        mm = json.loads(handle.read())

# sale record:
#
#       itemDesc
#       itemAdderText
#       seller
#       buyer
#       guild
#       quant
#       timestamp
#       wasKiosk
#       id
#       price

    sale_record = {}
    mmdata = 'mm["Default"]["MasterMerchant"]["$AccountWide"]["SalesData"]'

    for sale_list in eval(mmdata):

        for item in mm["Default"]["MasterMerchant"]["$AccountWide"]["SalesData"][sale_list]:
        # for item in eval(mmdata + '["%s"]' % sale_list):
            sale_record['item_desc'] =        mm["Default"]["MasterMerchant"]["$AccountWide"]["SalesData"][sale_list][item]["itemDesc"]
            sale_record['item_adder_text'] =  mm["Default"]["MasterMerchant"]["$AccountWide"]["SalesData"][sale_list][item]["itemAdderText"]

            for item_sale in mm["Default"]["MasterMerchant"]["$AccountWide"]["SalesData"][sale_list][item]["sales"]:

                sale_record['seller'] =       mm["Default"]["MasterMerchant"]["$AccountWide"]["SalesData"][sale_list][item]["sales"][item_sale]["seller"]
                sale_record['buyer'] =        mm["Default"]["MasterMerchant"]["$AccountWide"]["SalesData"][sale_list][item]["sales"][item_sale]["buyer"]
                sale_record['guild'] =        mm["Default"]["MasterMerchant"]["$AccountWide"]["SalesData"][sale_list][item]["sales"][item_sale]["guild"]
                sale_record['quant'] =        mm["Default"]["MasterMerchant"]["$AccountWide"]["SalesData"][sale_list][item]["sales"][item_sale]["quant"]
                sale_record['timestamp'] =    mm["Default"]["MasterMerchant"]["$AccountWide"]["SalesData"][sale_list][item]["sales"][item_sale]["timestamp"]
                sale_record['wasKiosk'] =     mm["Default"]["MasterMerchant"]["$AccountWide"]["SalesData"][sale_list][item]["sales"][item_sale]["wasKiosk"]
                sale_record['id'] =           mm["Default"]["MasterMerchant"]["$AccountWide"]["SalesData"][sale_list][item]["sales"][item_sale]["id"]
                sale_record['price'] =        mm["Default"]["MasterMerchant"]["$AccountWide"]["SalesData"][sale_list][item]["sales"][item_sale]["price"]

                doc = create_elastic_doc(sale_record)
                send_elastic_doc(es, elastic_index_name, doc)

            sale_record = {}    


if __name__ == "__main__":
    main()
