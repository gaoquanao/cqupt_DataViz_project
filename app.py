# -*- coding:utf-8 -*-
from flask import Flask
from flask import render_template
from pymongo import MongoClient
import json
from bson import json_util
from bson.json_util import dumps

app = Flask(__name__)

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DBS_NAME = 'log_vis'
COLLECTION_NAME = 'log'


@app.route("/")
def index():
    return render_template("pie_index.html")

# 该路由用于ajax获取数据
@app.route("/data")
def data():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][COLLECTION_NAME]
    # 统计出 HTTP status 出现的次数
    projects = collection.aggregate([{"$group" : {"_id" : "$status", "num_count" : {"$sum" : 1}}}])
    json_projects = []
    for project in projects:
        json_projects.append(project)
    json_projects = json.dumps(json_projects, default=json_util.default)
    connection.close()

    return json_projects

@app.route("/time")
def time():
    conn = MongoClient("localhost", 27017)
    db = conn['log_vis']
    projects = db.log.aggregate([{"$group" : {"_id" : "$time", "count" : {"$sum" : 1}}}])
    json_projects = []
    for project in projects:
        json_projects.append(project)
    json_projects = json.dumps(json_projects, default=json_util.default)
    conn.close()

    return  json_projects

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
