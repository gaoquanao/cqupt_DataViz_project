# -*- coding:utf-8 -*-
# db.log.aggregate([{$group: {_id: "$time", count: {$sum: 1}}}])
from pymongo import MongoClient
