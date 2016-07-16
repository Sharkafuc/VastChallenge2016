#coding=utf-8

import MySQLdb
import json

conn = MySQLdb.connect(host="localhost",port=3306,user="root",passwd="wangjunwei",db="vastChallenge")
c = conn.cursor()
#selectPara = "Lights Power"
selectPara = "Thermostat Temp"
sql = "describe bldg"
c.execute(sql)
select = []
for row in c.fetchall():
    if selectPara in row[0]:
        select.append(row[0])
#print select
sql = "select "
for i in range(len(select)):
    if i == len(select)-1:
        sql = sql+"`"+select[i]+"` from bldg"
    else:
        sql = sql+"`"+select[i]+"`,"
#print sql
c.execute(sql)
#print len(c.fetchall())
result = []
for row in c.fetchall():
    #print row
    for j in range(len(select)):
        result.append(row[j])
print min(result),max(result)
