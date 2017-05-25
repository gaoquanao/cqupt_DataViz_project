# -*- coding:utf-8 -*-

# 1.插入解析过的时间到数据库 形如"2000-06-05 13:05:12",5(该时间访问次数)
# 2.数据库的插新 而不是删除掉之前的数据库 $set upsert=false,multi=true
# 3.时间如何解析成要求的样子 已解决 datetime.strptime 正则
# 4.如何获取毫秒级的访问次数 一个思路找到数据库中的时间然后count
# 5.存成json格式[time, count]

from pymongo import MongoClient
import datetime
import re

conn = MongoClient("localhost", 27017)
db = conn['log_vis']


with open("../data/www_access_20140823.log","r") as f:
    for line in f:
        log_time = re.findall("(\[[^\[\]]+\])", line)[0][1:-1]
        log_time = datetime.datetime.strptime(log_time, "%d/%b/%Y:%H:%M:%S +0800")
        db.log.update({}, {"$set": {"time": str(log_time)}}, upsert=False, multi=True)

# 嗯 很花时间才不到两万条数据
# 时间长的问题所在multi=true 相当于每一时间都插入了19000多次，也就是19000*19000 怪不得要这么长的时间
conn.close()
