#!/usr/bin/python

import redis
import MySQLdb
from collections import Counter

r = redis.StrictRedis('ElastiCacheRedisEndpoint',port=6379,db=0)
database = MySQLdb.connect("RDSEndpoint","databaseadmin","AWSNYLoft","landsat")

cursor = database.cursor()
select = 'SELECT entityId, UNIX_TIMESTAMP(acquisitionDate), cloudCover, processingLevel, path, row, min_lat, min_lon, max_lat, max_lon, download_url FROM scene_list'
cursor.execute(select)
data = cursor.fetchall()

for row in data:
    r.hmset(row[0],{'acquisitionDate':row[1],'cloudCover':row[2],'processingLevel':row[3],'path':row[4],'row':row[5],'min_lat':row[6],'min_lon':row[7],'max_lat':row[8],'max_lon':row[9],'download_url':row[10]})
r.zadd('cCov',row[2],row[0])
r.zadd('acqDate',row[1],row[0])

cursor.close()
database.close()
