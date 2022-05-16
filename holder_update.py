from crawler_service import TokenHolderStats
import pymongo
import pandas as pd

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