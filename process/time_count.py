# -*- coding:utf-8 -*-
# db.log.aggregate([{$group: {_id: "$time", count: {$sum: 1}}}])

import json
from bson import json_util
from pymongo import MongoClient

conn = MongoClient("localhost", 27017)
db = conn['log_vis']

def get_json():
    projects = db.log.aggregate([{"$group" : {"_id" : "$time", "count" : {"$sum" : 1}}}])
    json_projects = []
    for project in projects:
        json_projects.append(project)
    json_projects = json.dumps(json_projects, default=json_util.default)
    return  json_projects

if __name__ == '__main__':
    result = get_json()
    print len(result)
    with open("time.json","w") as f:
        f.write(result)
