from platform import platform
from market_service import MarketService
import pymongo
import pandas as pd
from market_service import MarketService

client = pymongo.MongoClient('mongodb+srv://admin:admin@db.5m3qg.mongodb.net/test?authSource=admin&replicaSet=atlas-dzj3vd-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true', 
                             username='admin', password='admin')

db = client["token"]
col = db["coincap"]

service = MarketService()

coincap5000 = pd.read_csv('data/coincap5000.csv')
coincap5000id = coincap5000['id'].to_list()

for id in coincap5000id:
  print(id)
  mongo_id = 'token/' + id

  platform = service.get_list_address_by_id(id)  
  col.find_one_and_update({"_id": mongo_id}, 
                          {"$set": {"platforms": platform}})

  col.update_many