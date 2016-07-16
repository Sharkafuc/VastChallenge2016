import MySQLdb

conn = MySQLdb.connect(host = "localhost",user = "root",passwd = "wangjunwei",db = "vastChallenge",port = 3306)

cursor = conn.cursor()
sql = "describe bldg"
cursor.execute(sql)
for row in cursor.fetchall():
    #print row[0]
    sql = "select distinct `"+row[0]+"` from bldg "
    result = cursor.execute(sql)
    if result == 1:
        sql = "alter table bldg drop column `"+row[0]+"`"
        cursor.execute(sql)
