from platform import platform
from crawler_service import TokenHolderStats
import pymongo
import pandas as pd
import logging

client = pymongo.MongoClient('mongodb+srv://admin:admin@db.5m3qg.mongodb.net/test?authSource=admin&replicaSet=atlas-dzj3vd-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true', 
                             username='admin', password='admin')

db = client["token"]
col = db["coincap5k"]

service = TokenHolderStats('0x1')

coincap5000 = pd.read_csv('data/coincap5000.csv')
coincap5000id = coincap5000['id'].to_list()

mapping = {}

for x in col.find():
  try:
    mapping[x['id']] = x['platforms']
  except:
    pass

scan_mapping = {
  "ethereum": "0x1",
  "polygon-pos": "0x89",
  "binance-smart-chain": "0x38",
  # "optimistic-ethereum": "0xa",
  # "arbitrum-one": "0xa4b1",
  # "moonriver": "0x505",
  "fantom": "0xfa",
  # "moonbeam": "0x504",
}
  
total_holder_mapping = {}
error_list = []

total_holder_mapping = {}
error_list = []

for id in coincap5000id:  
  total_holder = 0
  
  try:
    for key, value in mapping[id].items():
      try:
        if (key in scan_mapping):
          service = TokenHolderStats(scan_mapping[key])
          holder = service.get_holder(value)
          total_holder += holder['total_holders'] 
          
      except:
        error_list.append(id)
    
    # Open a file with access mode 'a'
    file_object = open('data/coin_holder.txt', 'a')
    # Append 'hello' at the end of file
    s = id + ' ' + str(total_holder) + '\n' 
    file_object.write(s)
    # Close the file
    file_object.close()
      
  except:
    error_list.append(id)
    # Open a file with access mode 'a'
    file_object = open('data/error.txt', 'a')
    # Append 'hello' at the end of file
    file_object.write("\n".join(error_list))
    # Close the file
    file_object.close()

