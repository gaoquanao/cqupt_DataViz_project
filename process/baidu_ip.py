# -*- coding:utf-8 -*-

import json
import time
import requests
from ratelimiter import RateLimiter
from pymongo import MongoClient


conn = MongoClient("localhost", 27017)
db = conn['log_vis']

ak = """7L9mxsMyepmGrMoednU5ivCLEnr6Ey1c"""


@RateLimiter(max_calls=100, period=1)
def get_geo(ip):
    url = "https://api.map.baidu.com/location/ip?ak={}&coor=bd09ll&ip={}".format(
        ak, ip)
    try:
        r = requests.get(url)
        json_dict = json.loads(r.text)
        return json_dict
    except:
        print 'Error: geting {} address fail.'.format(ip)
        return 0


def get_id_ip():
    cursor = db.log.find({}, {"ip": 1})
    while True:
        try:
            item = cursor.next()
            id = item['_id']
            ip = item['ip']
            mydict = get_geo(ip)

            if mydict.get('status') == 0:
                city = mydict['content']['address_detail']['city']
                x = mydict['content']['point']['x']
                y = mydict['content']['point']['y']

                db.address.insert({
                    "city": city,
                    "longitude": x,
                    "latitude": y
                })
                print "adding city:%s longitude:%s latitude:%s into database" % (city, x, y)

        except StopIteration:
            break

def new_get_id_ip():
    cursor = db.log.find({}, {"ip": 1})
    while True:
        try:
            item = cursor.next()
            id = item['_id']
            ip = item['ip']
            mydict = get_geo(ip)

            if mydict.get('status') == 0:
                city = mydict['content']['address_detail']['city']
                x = mydict['content']['point']['x']
                y = mydict['content']['point']['y']

                db.address.insert({
                    "city": city,
                    "longitude": x,
                    "latitude": y
                })
                print "adding city:%s longitude:%s latitude:%s into database" % (city, x, y)

        except StopIteration:
            break



if __name__ == '__main__':
    start = time.time()
    get_id_ip()
    stop = time.time()
    # 使用迭代器，最终插入了18773条数据到新的数据库中，花了7754秒
    # API配额是每天10万次，每分钟并发6000次
    print "Time costed:{}".format(stop - start)
