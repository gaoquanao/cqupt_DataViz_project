# -*- coding:utf-8 -*-
from pymongo import MongoClient

conn = MongoClient("localhost", 27017)
db = conn['log_vis']

with open("www_access_20140823.log","r") as f:
    res = {}
    for line in f:
        # 获取IP URL STATUS
        arr = line.split(' ')
        ip = arr[0]
        url = arr[6]
        status = arr[8]
        db.log.insert({
            "ip":ip,
            "url":url,
            "status":status
        })

# 获取HTTP状态码的
# db.log.aggregate([{$group : {_id : "$status", num_count : {$sum : 1}}}])
{ "_id" : "403", "num_count" : 1 }
{ "_id" : "301", "num_count" : 2 }
{ "_id" : "206", "num_count" : 6 }
{ "_id" : "304", "num_count" : 3549 }
{ "_id" : "200", "num_count" : 15347 }
{ "_id" : "404", "num_count" : 834 }
