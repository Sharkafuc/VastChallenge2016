#coding=utf-8

import numpy as np
import MySQLdb
from sklearn import preprocessing

conn = MySQLdb.connect(host = "localhost",user = "root",passwd = "wangjunwei",db = "vastChallenge" ,port = 3306)

cursor =conn.cursor()

sql = "select * from bldg"
result = cursor.execute(sql)
#print result
data = []
for eachrow in cursor.fetchall():
    line = eachrow[1:]
    data.append(line)

#print len(data)
#print (data[1])
datamat = np.matrix(data)
datamat = preprocessing.scale(datamat)
u,sigma,vt = np.linalg.svd(datamat)
sig2 = sigma**2
totalsv = sum(sig2)
print totalsv*0.9
svd = sum(sig2[:30])
print svd
print svd/totalsv


