# -*- coding:utf-8 -*-
from pymongo import MongoClient
import json
from bson import json_util
from bson.json_util import dumps


MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DBS_NAME = 'log_vis'
COLLECTION_NAME = 'log'

city_set = set()
info_dict = {}

conn = MongoClient("localhost", 27017)
db = conn['log_vis']
result = db.address.find({}, {"city":1, "latitude":1, "longitude":1 ,"_id":0})

for item_dict in result:
    city = item_dict.get("city")
    # 纬度
    latitude = item_dict.get("latitude")
    # 经度
    longitude = item_dict.get("longitude")
    # 有脏数据 没有城市名 只有经纬度
    if len(city) != 0:
        city_set.add(city)
        info_dict[city] = [longitude, latitude]


for city in city_set:
    count = db.address.find({"city": city}).count()
    [longitude, latitude] = info_dict[city]
    info_dict[city] = [longitude, latitude, count]


final_json = []
for key, value in info_dict.items():
    record = {"name": key, "value": value}
    final_json.append(record)

json_projects = json.dumps(final_json, default=json_util.default)
conn.close()





