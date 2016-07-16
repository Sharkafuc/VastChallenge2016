#coding=utf-8

import MySQLdb as mysql
import json
from flask import Flask,request,render_template
from flask.ext.bootstrap import Bootstrap
import re

app = Flask(__name__)
bootstrap = Bootstrap(app)
db = mysql.connect(host = "localhost",port = 3306, user = "root", passwd = "wangjunwei" ,db = "vastChallenge")
db.autocommit(True)
c = db.cursor()
@app.route('/')
def hello_world():
    return render_template("floorPlan.html")

@app.route('/timeplace')
def timeplace():
    return render_template("timePlaceStack.html")

@app.route('/getTotalParas')
def getTotalParas():
    sql = "select `Date/Time`,`DELI-FAN Power`,`Total Electric Demand Power`/2000,`HVAC Electric Demand Power`/1000,`Drybulb Temperature`,`Supply Side Inlet Temperature` from bldg"
    c.execute(sql)
    rows = c.fetchall()
    ones = []
    for i in range(1,6):
        one = []
        for row in rows:
            one.append([row[0]+8*3600000,row[i]])
        ones.append(one)
    return json.dumps(ones)

@app.route('/getSelectPara')
def getSelectPara():
    selectPara = request.args.get('para')
    selectTime = request.args.get('time')
    #print selectPara
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
            sql = sql+"`"+select[i]+"` from bldg where `Date/Time` = "+str(selectTime)+";"
        else:
            sql = sql+"`"+select[i]+"`,"
    print sql
    c.execute(sql)
    #print c.fetchall()
    datas = []#ones parainfo; twos peplenuminfo
    ones = []
    rows = c.fetchall()
    if len(rows)>0:
        rows = rows[0]
    else:
        return json.dumps(datas)

    for i in range(len(rows)):
        pat = re.compile(r'F_(\d)_Z_(\d{1,2}\w?)[:\s].+?')
        zonelist = pat.findall(select[i])
        if len(zonelist)>0:
            ones.append({"floor":zonelist[0][0],
                    "zone":zonelist[0][1],
                    "value":rows[i]})
        else:
            pat = re.compile(r'F_(\d)_[^Z].+?_.+?')
            floorlist = pat.findall(select[i])
            ones.append({"floor":floorlist[0][0],"value":rows[i]})
    datas.append(ones)

    twos = []
    if int(selectTime) <=1464624000000:
        twos = [{"floor":1,"zone":1,"count":0},{"floor":1,"zone":6,"count":0},{"floor":1,"zone":4,"count":0},{"floor":2,"zone":4,"count":0},
                {"floor":3,"zone":4,"count":0},{"floor":3,"zone":1,"count":0},{"floor":3,"zone":6,"count":0},{"floor":2,"zone":1,"count":1},
                {"floor":2,"zone":2,"count":0},{"floor":2,"zone":7,"count":0},{"floor":2,"zone":6,"count":0},{"floor":3,"zone":2,"count":0},
                {"floor":3,"zone":3,"count":0},{"floor":1,"zone":2,"count":0},{"floor":2,"zone":3,"count":0},{"floor":1,"zone":8,"count":0},
                {"floor":1,"zone":7,"count":0},{"floor":3,"zone":7,"count":0},{"floor":1,"zone":3,"count":0},{"floor":1,"zone":5,"count":0}
                ]
    else:
        sql = "select floor,zone,count from zoominter5min where floor(UNIX_TIMESTAMP(timestamp))*1000 ="+str(selectTime)
        c.execute(sql)
        rows = c.fetchall()
        for i in range(len(rows)):
            twos.append({"floor":rows[i][0],"zone":rows[i][1],"count":rows[i][2]})
    datas.append(twos)

    return json.dumps(datas)

@app.route('/getCurTimeOfBldg')
def getCurTimeOfBldg():
    curtime = request.args.get("time")
    sql = "select `Date/Time` from bldg where `Date/Time`<= "+str(curtime)+ " and `Date/Time`+300000 > "+str(curtime)
    #print sql
    c.execute(sql)
    rows = c.fetchall()
    #print rows[0][0]
    return json.dumps(rows[0][0])

@app.route('/getTrajectory')
def getTrajectory():
    type = int(request.args.get("type"))
    proxid = request.args.get("proxid")
    proxid2 = request.args.get("proxid2")
    curtime = request.args.get("time")
    print type,int(curtime)
    datas = []
    men = []

    proxidtwo = proxid[:-1]+str(int(proxid[-1])+1)

    # #print proxidtwo
    # sql = "select unixtime*1000 from locationWithTime where proxid like '"+proxidtwo+"'"
    # c.execute()
    # twotime = c.fetchall()[0][0]

    sql = "select unixtime*1000,floor,zone,x,y,office from locationWithTime where proxid like '"+proxid+"'"
    print sql
    c.execute(sql)

    rows = c.fetchall()
    onepre = []
    for i in range(len(rows)):
        if i == len(rows)-1 and type == 1:
            one = {"time":rows[i][0],"floor":rows[i][1],"zone":rows[i][2],"x":rows[i][3],"y":rows[i][4],"office":"black"}
            onepre = {"floor":rows[i][1],"zone":rows[i][2],"x":rows[i][3],"y":rows[i][4],"office":rows[i][5]}
            break
        #print curtime,i,rows[i][0],rows[i+1][0]
        if i == 0 and rows[i][0]> int(curtime):
            #print "1step"
            one = {"time":rows[i][0],"floor":rows[i][1],"zone":rows[i][2],"x":rows[i][3],"y":rows[i][4],"office":rows[i][5]}
            onepre = {"floor":rows[i][1],"zone":rows[i][2],"x":rows[i][3],"y":rows[i][4],"office":rows[i][5]}
            break
            #return json.dumps(one)
        elif rows[i][0]< int(curtime) and rows[i+1][0]> int(curtime) :
            if type == 0:
                one = {"time":curtime,"floor":rows[i][1],"zone":rows[i][2],"x":rows[i][3],"y":rows[i][4],"office":rows[i][5]}
                onepre = {"floor":rows[i][1],"zone":rows[i][2],"x":rows[i][3],"y":rows[i][4],"office":rows[i][5]}
            elif type == -1:
                one = {"time":rows[i][0],"floor":rows[i][1],"zone":rows[i][2],"x":rows[i][3],"y":rows[i][4],"office":rows[i][5]}
                if i == 0:
                    onepre = {"floor":rows[i][1],"zone":rows[i][2],"x":rows[i][3],"y":rows[i][4],"office":rows[i][5]}
                else:
                    onepre = {"floor":rows[i-1][1],"zone":rows[i-1][2],"x":rows[i-1][3],"y":rows[i-1][4],"office":rows[i-1][5]}
            elif type == 1:
                one = {"time":rows[i+1][0],"floor":rows[i+1][1],"zone":rows[i+1][2],"x":rows[i+1][3],"y":rows[i+1][4],"office":rows[i+1][5]}
                onepre = {"floor":rows[i][1],"zone":rows[i][2],"x":rows[i][3],"y":rows[i][4],"office":rows[i][5]}
                sql = "select * from locationWithTime where proxid like '"+proxidtwo+"' and unixtime*1000 <= "+str(rows[i+1][0])
                print sql
                tworesult = c.execute(sql)
                if tworesult >0:
                    one["office"] = "black"
            break
            #return json.dumps(one)
        elif rows[i][0] < int(curtime) and rows[i+1][0] == int(curtime) and type == -1:
            one = {"time":rows[i][0],"floor":rows[i][1],"zone":rows[i][2],"x":rows[i][3],"y":rows[i][4],"office":rows[i][5]}
            if i == 0:
                onepre = {"floor":rows[i][1],"zone":rows[i][2],"x":rows[i][3],"y":rows[i][4],"office":rows[i][5]}
            else:
                onepre = {"floor":rows[i-1][1],"zone":rows[i-1][2],"x":rows[i-1][3],"y":rows[i-1][4],"office":rows[i-1][5]}
            break
            #return json.dumps(one)
        elif rows[i][0] == int(curtime) and rows[i+1][0] > int(curtime) and type == 1:
            print rows[i]
            one = {"time":rows[i+1][0],"floor":rows[i+1][1],"zone":rows[i+1][2],"x":rows[i+1][3],"y":rows[i+1][4],"office":rows[i+1][5]}
            onepre = {"floor":rows[i][1],"zone":rows[i][2],"x":rows[i][3],"y":rows[i][4],"office":rows[i][5]}
            sql = "select * from locationWithTime where proxid like '"+proxidtwo+"' and unixtime*1000 <= "+str(rows[i+1][0])
            print sql
            tworesult = c.execute(sql)
            if tworesult >0:
                one["office"] = "black"
            print "next"
            break
            #return json.dumps(one)
        elif rows[i][0] == int(curtime) and rows[i+1][0] > int(curtime) and type == 0:
            print rows[i]
            one = {"time":curtime,"floor":rows[i][1],"zone":rows[i][2],"x":rows[i][3],"y":rows[i][4],"office":rows[i][5]}
            if i == 0:
                onepre = {"floor":rows[i][1],"zone":rows[i][2],"x":rows[i][3],"y":rows[i][4],"office":rows[i][5]}
            else:
                onepre = {"floor":rows[i-1][1],"zone":rows[i-1][2],"x":rows[i-1][3],"y":rows[i-1][4],"office":rows[i-1][5]}
            print "cur"
            break
            #return json.dumps(one)
    else:
        one = {"time":rows[len(rows)-1][0],"floor":rows[len(rows)-1][1],"zone":rows[len(rows)-1][2],"x":rows[len(rows)-1][3],"y":rows[len(rows)-1][4],"office":rows[len(rows)-1][5]}
        onepre = {"floor":rows[len(rows)-2][1],"zone":rows[len(rows)-2][2],"x":rows[len(rows)-2][3],"y":rows[len(rows)-2][4],"office":rows[len(rows)-2][5]}

    men.append(one)

    if proxid2 != '':
        #print proxid2
        twopre = []
        sql = "select unixtime*1000,floor,zone,x,y,office from locationWithTime where proxid like '"+proxid2+"'"
        #print sql
        c.execute(sql)
        rows = c.fetchall()
        for i in range(len(rows)):
            if i == 0 and rows[i][0]> int(curtime):
                two = {"time":rows[i][0],"floor":rows[i][1],"zone":rows[i][2],"x":rows[i][3],"y":rows[i][4],"office":rows[i][5]}
                twopre = {"floor":rows[i][1],"zone":rows[i][2],"x":rows[i][3],"y":rows[i][4],"office":rows[i][5]}
                break
            elif rows[i][0]< int(curtime) and rows[i+1][0]> int(curtime) :
                if type == 0:
                    two = {"time":curtime,"floor":rows[i][1],"zone":rows[i][2],"x":rows[i][3],"y":rows[i][4],"office":rows[i][5]}
                    twopre = {"floor":rows[i][1],"zone":rows[i][2],"x":rows[i][3],"y":rows[i][4],"office":rows[i][5]}
                elif type == -1:
                    two = {"time":rows[i][0],"floor":rows[i][1],"zone":rows[i][2],"x":rows[i][3],"y":rows[i][4],"office":rows[i][5]}
                    if i == 0:
                        twopre = {"floor":rows[i][1],"zone":rows[i][2],"x":rows[i][3],"y":rows[i][4],"office":rows[i][5]}
                    else:
                        twopre = {"floor":rows[i-1][1],"zone":rows[i-1][2],"x":rows[i-1][3],"y":rows[i-1][4],"office":rows[i-1][5]}
                elif type == 1:
                    two = {"time":rows[i+1][0],"floor":rows[i+1][1],"zone":rows[i+1][2],"x":rows[i+1][3],"y":rows[i+1][4],"office":rows[i+1][5]}
                    twopre = {"floor":rows[i][1],"zone":rows[i][2],"x":rows[i][3],"y":rows[i][4],"office":rows[i][5]}
                break
            elif rows[i][0] < int(curtime) and rows[i+1][0] == int(curtime) and type == -1:
                two = {"time":rows[i][0],"floor":rows[i][1],"zone":rows[i][2],"x":rows[i][3],"y":rows[i][4],"office":rows[i][5]}
                if i == 0:
                    twopre = {"floor":rows[i][1],"zone":rows[i][2],"x":rows[i][3],"y":rows[i][4],"office":rows[i][5]}
                else:
                    twopre = {"floor":rows[i-1][1],"zone":rows[i-1][2],"x":rows[i-1][3],"y":rows[i-1][4],"office":rows[i-1][5]}
                break
            elif rows[i][0] == int(curtime) and rows[i+1][0] > int(curtime) and type == 1:
                print rows[i]
                two = {"time":rows[i+1][0],"floor":rows[i+1][1],"zone":rows[i+1][2],"x":rows[i+1][3],"y":rows[i+1][4],"office":rows[i+1][5]}
                twopre = {"floor":rows[i][1],"zone":rows[i][2],"x":rows[i][3],"y":rows[i][4],"office":rows[i][5]}
                print "next"
                break
            elif rows[i][0] == int(curtime) and rows[i+1][0] > int(curtime) and type == 0:
                print rows[i]
                two = {"time":rows[i][0],"floor":rows[i][1],"zone":rows[i][2],"x":rows[i][3],"y":rows[i][4],"office":rows[i][5]}
                if i == 0:
                    twopre = {"floor":rows[i][1],"zone":rows[i][2],"x":rows[i][3],"y":rows[i][4],"office":rows[i][5]}
                else:
                    twopre = {"floor":rows[i-1][1],"zone":rows[i-1][2],"x":rows[i-1][3],"y":rows[i-1][4],"office":rows[i-1][5]}
                print "cur"
                break
        else:
            two = {"time":rows[len(rows)-1][0],"floor":rows[len(rows)-1][1],"zone":rows[len(rows)-1][2],"x":rows[len(rows)-1][3],"y":rows[len(rows)-1][4],"office":rows[len(rows)-1][5]}
            twopre = {"floor":rows[len(rows)-2][1],"zone":rows[len(rows)-2][2],"x":rows[len(rows)-2][3],"y":rows[len(rows)-2][4],"office":rows[len(rows)-2][5]}
        men.append(two)

        print one["time"],two["time"]
        if one["time"] != two["time"]:
            if one["time"] < two["time"]:
                men[1]["time"] = one["time"]
                men[1]["floor"] = twopre["floor"]
                men[1]["zone"] = twopre["zone"]
                men[1]["x"] = twopre["x"]
                men[1]["y"] = twopre["y"]
                men[1]["office"] = twopre["office"]
            else:
                men[0]["time"] = two["time"]
                men[0]["floor"] = onepre["floor"]
                men[0]["zone"] = onepre["zone"]
                men[0]["x"] = onepre["x"]
                men[0]["y"] = onepre["y"]
                men[0]["office"] = onepre["office"]

    datas.append(men)
    twos = []
    if men[0]["time"] <=1464624000000:
        twos = [{"floor":1,"zone":1,"count":0},{"floor":1,"zone":6,"count":0},{"floor":1,"zone":4,"count":0},{"floor":2,"zone":4,"count":0},
                {"floor":3,"zone":4,"count":0},{"floor":3,"zone":1,"count":0},{"floor":3,"zone":6,"count":0},{"floor":2,"zone":1,"count":1},
                {"floor":2,"zone":2,"count":0},{"floor":2,"zone":7,"count":0},{"floor":2,"zone":6,"count":0},{"floor":3,"zone":2,"count":0},
                {"floor":3,"zone":3,"count":0},{"floor":1,"zone":2,"count":0},{"floor":2,"zone":3,"count":0},{"floor":1,"zone":8,"count":0},
                {"floor":1,"zone":7,"count":0},{"floor":3,"zone":7,"count":0},{"floor":1,"zone":3,"count":0},{"floor":1,"zone":5,"count":0}
                ]
    else:
        sql = "select `Date/Time` from bldg where `Date/Time`<= "+str(men[0]["time"])+ " and `Date/Time`+300000 > "+str(men[0]["time"])
        c.execute(sql)
        time = c.fetchall()[0][0]
        sql = "select floor,zone,count from zoominter5min where floor(UNIX_TIMESTAMP(timestamp))*1000 ="+str(time)
        c.execute(sql)
        rows = c.fetchall()
        for i in range(len(rows)):
            twos.append({"floor":rows[i][0],"zone":rows[i][1],"count":rows[i][2]})
    datas.append(twos)
    return json.dumps(datas)

@app.route('/getRobotTrajectory')
def getRobotTrajectory():
    type = int(request.args.get("type"))
    curtime = request.args.get("time")

    sql = "select unixtime*1000,x,y,office,floor,zone from locationWithTime where type like 'mobile-prox'"
    c.execute(sql)
    rows = c.fetchall()
    datas = []

    for i in range(len(rows)):
        if i == 0 and rows[i][0]> int(curtime):
            one = {"time":rows[i][0],"x":rows[i][1],"y":rows[i][2],"office":rows[i][3],"floor":rows[i][4],"zone":rows[i][5]}
            break
        elif rows[i][0]< int(curtime) and rows[i+1][0]> int(curtime) :
            if type == 0:
                one = {"time":curtime,"x":rows[i][1],"y":rows[i][2],"office":rows[i][3],"floor":rows[i][4],"zone":rows[i][5]}
            elif type == -1:
                one = {"time":rows[i][0],"x":rows[i][1],"y":rows[i][2],"office":rows[i][3],"floor":rows[i][4],"zone":rows[i][5]}
            elif type == 1:
                one = {"time":rows[i+1][0],"x":rows[i+1][1],"y":rows[i+1][2],"office":rows[i+1][3],"floor":rows[i+1][4],"zone":rows[i+1][5]}
            break
        elif rows[i][0] < int(curtime) and rows[i+1][0] == int(curtime) and type == -1:
            one = {"time":rows[i][0],"x":rows[i][1],"y":rows[i][2],"office":rows[i][3],"floor":rows[i][4],"zone":rows[i][5]}
            break
        elif rows[i][0] == int(curtime) and rows[i+1][0] > int(curtime) and type == 1:
            one = {"time":rows[i+1][0],"x":rows[i+1][1],"y":rows[i+1][2],"office":rows[i+1][3],"floor":rows[i+1][4],"zone":rows[i+1][5]}
            print "next"
            break
            #return json.dumps(one)
        elif rows[i][0] == int(curtime) and rows[i+1][0] > int(curtime) and type == 0:
            one = {"time":curtime,"x":rows[i][1],"y":rows[i][2],"office":rows[i][3],"floor":rows[i][4],"zone":rows[i][5]}
            print "cur"
            break
    else:
        one = {"time":rows[len(rows)-1][0],"x":rows[len(rows)-1][1],"y":rows[len(rows)-1][2],"office":rows[len(rows)-1][3],"floor":rows[len(rows)-1][4],"zone":rows[len(rows)-1][5]}
    datas.append(one)

    two = []
    if one["time"] <=1464624000000:
        two = [{"floor":1,"zone":1,"count":0},{"floor":1,"zone":6,"count":0},{"floor":1,"zone":4,"count":0},{"floor":2,"zone":4,"count":0},
                {"floor":3,"zone":4,"count":0},{"floor":3,"zone":1,"count":0},{"floor":3,"zone":6,"count":0},{"floor":2,"zone":1,"count":1},
                {"floor":2,"zone":2,"count":0},{"floor":2,"zone":7,"count":0},{"floor":2,"zone":6,"count":0},{"floor":3,"zone":2,"count":0},
                {"floor":3,"zone":3,"count":0},{"floor":1,"zone":2,"count":0},{"floor":2,"zone":3,"count":0},{"floor":1,"zone":8,"count":0},
                {"floor":1,"zone":7,"count":0},{"floor":3,"zone":7,"count":0},{"floor":1,"zone":3,"count":0},{"floor":1,"zone":5,"count":0}
                ]
    else:
        sql = "select `Date/Time` from bldg where `Date/Time`<= "+str(one["time"])+ " and `Date/Time`+300000 > "+str(one["time"])
        c.execute(sql)
        time = c.fetchall()[0][0]
        sql = "select floor,zone,count from zoominter5min where floor(UNIX_TIMESTAMP(timestamp))*1000 ="+str(time)
        c.execute(sql)
        rows = c.fetchall()
        for i in range(len(rows)):
            two.append({"floor":rows[i][0],"zone":rows[i][1],"count":rows[i][2]})
    datas.append(two)
    return json.dumps(datas)

@app.route('/getSelectFloorPara')
def getSelectFloorPara():
    selectPara = request.args.get('para')
    sql = "describe bldg"
    c.execute(sql)
    select = []
    for row in c.fetchall():
        if selectPara in row[0]:
            select.append(row[0])
    #print select
    sql = "select `Date/Time`,"
    for i in range(len(select)):
        if i == len(select)-1:
            sql = sql+"`"+select[i]+"` from bldg;"
        else:
            sql = sql+"`"+select[i]+"`,"
    c.execute(sql)
    ones = []
    rows = c.fetchall()
    for i in range(1,4):
        one = []
        for row in rows:
            one.append([row[0]+8*3600000,row[i]])
        ones.append(one)
    #print len(ones)
    return json.dumps(ones)

@app.route('/getZoneParas')
def getZoneParas():
    zonename = request.args.get('name')
    pat = re.compile(r'f(\d)z(\d{1,2}\w?)')
    location = pat.findall(zonename)
    print location
    floor = str(location[0][0])
    zone = str(location[0][1])
    sql = "select `Date/Time`,`F_"+floor+"_Z_"+zone+" REHEAT COIL Power`/200,\
                  `F_"+floor+"_Z_"+zone+" RETURN OUTLET CO2 Concentration`/100,\
                  `F_"+floor+"_Z_"+zone+" SUPPLY INLET Mass Flow Rate`*50,\
                  `F_"+floor+"_Z_"+zone+" SUPPLY INLET Temperature`,\
                  `F_"+floor+"_Z_"+zone+" VAV REHEAT Damper Position`*20,\
                  `F_"+floor+"_Z_"+zone+": Equipment Power`/63,\
                  `F_"+floor+"_Z_"+zone+": Lights Power`/63,\
                  `F_"+floor+"_Z_"+zone+": Thermostat Temp`,\
                  `F_"+floor+"_Z_"+zone+": Thermostat Cooling Setpoint`,\
                  `F_"+floor+"_Z_"+zone+": Thermostat Heating Setpoint`,\
                  `Drybulb Temperature` \
                   from bldg"
    print sql
    c.execute(sql)
    ones = []
    rows = c.fetchall()
    for i in range(1,12):
        one = []
        for row in rows:
            one.append([row[0]+8*3600000,row[i]])
        ones.append(one)
    return json.dumps(ones)

@app.route('/getDepartmentTrajectory',methods=['POST'])
def getDepartmentTrajectory():
    data = json.loads(request.form.get('data'))
    datastring = data['value']
    print datastring
    pat = re.compile(r'(\d+)/(\d+)/(\d+)/(\d+)/(\d+)')
    data = pat.findall(datastring)
    startman = data[0][0]
    endman = data[0][1]
    starttime = data[0][2]
    endtime = data[0][3]
    timegap = data[0][4]


    if startman == '' or startman == None:
        startman = 1;
    if endman == '' or endman == None:
        endman = 125;

    employdict = {}
    sql = "select id,proxid from employlist"
    c.execute(sql)
    rows = c.fetchall()
    for row in rows:
        employdict[row[0]] = row[1]
    #print employdict

    allzone = set()
    neededdata = []
    for i in range(int(startman),int(endman)+1):
        sql = "select id,unixtime,place from placewithtimed where id = "+str(i)+" and unixtime >= "+str(starttime)+\
              " and unixtime <= "+str(endtime)
        #print sql
        c.execute(sql)
        rows = c.fetchall()
        personrows = set()
        for j in range(len(rows)-1):
            if rows[j+1][1]-rows[j][1] >= int(timegap):
                personrows.add(int(rows[j][2]))
                neededdata.append(rows[j])
        if len(rows)>0:
            personrows.add(int(rows[len(rows)-1][2]))
            neededdata.append(rows[len(rows)-1])
        #print personrows
        allzone = allzone.union(personrows)

    zonecount = len(allzone)
    zones = list(allzone)
    zones.sort()
    height =50//zonecount
    locationdict = {}
    for i in range(len(zones)):
        locationdict[zones[i]] = 1+i*height

    mdata = []
    for i in range(int(startman),int(endman)+1):
        data = []
        for each in neededdata:
            if each[0] == i:
                data.append([each[1],locationdict[each[2]]])
        if len(data)>0:
            mdata.append({"label":employdict[i][:-3],"data":data})

    print mdata

    des = {}
    #print locationdict
    for each in locationdict:
        if each == 1:
            des[locationdict[each]] = 'OWN OFFICE';
        elif each == 3:
            des[locationdict[each]] = 'CONFERENCE';
        elif each == 5:
            des[locationdict[each]] = 'DELI';
        elif each == 7:
            des[locationdict[each]] = "OTHER'S OFFICE";
        else:
            des[locationdict[each]] = 'floor'+str(each//10)+' zone'+str(each%10)

    result = {"des":des,"mdata":mdata}
    return json.dumps(result)

def weekAverageDistribute(name):
    proxid = name
    origintime = 1464624000
    sql = "select floor,zone,office from employlist where proxid like '"+name[:-3]+"%'"
    c.execute(sql)
    own = c.fetchall()[0]
    ownoffice = own[2]
    ownfloor = own[0]
    ownzone = own[1]
    sql = "select office from employlist"
    c.execute(sql)
    officesres = c.fetchall()
    offices = []
    for each in officesres:
        offices.append(each[0])
    alladdr = {}
    alladdrdata = {}
    for i in range(14):
        time = origintime + 3600*24*i
        sql = "select floor,zone,office,unixtime from locationwithtime where proxid like '"+name+"' and unixtime >= "+str(time)+" and unixtime < "+str(time+24*3600)
        c.execute(sql)
        rows = c.fetchall()
        location = []
        starttime = time
        for i in range(len(rows)):
            if rows[i][3]-starttime >= 7*60 and i>=1:
                row = {}
                row["floor"] = rows[i-1][0]
                row["zone"] = rows[i-1][1]
                row["office"] = rows[i-1][2]
                row["time"] = round((rows[i][3]-starttime)/3600.0,1)
                location.append(row)
            starttime = rows[i][3]
        indicator = {}
        for each in location:
            #print each,each["floor"],each["zone"]
            if each["office"] == ownoffice or (int(each["floor"]) == int(ownfloor) and int(each["zone"]) == int(ownzone)):
                if "ownoffice" in indicator:
                    indicator["ownoffice"] = round(indicator["ownoffice"]+each["time"],1)
                else:
                    indicator["ownoffice"] = each["time"]
            elif each["office"] in offices:
                if "otheroffice" in indicator:
                    indicator["otheroffice"] = round(indicator["otheroffice"]+each["time"],1)
                else:
                    indicator["otheroffice"] = each["time"]
            elif each["office"] in [3330,3700,2700,2365,1030,1050]:
                if "conf" in indicator:
                    indicator["conf"] = round(indicator["conf"]+each["time"],1)
                else:
                    indicator["conf"] = each["time"]
            elif each["office"] == 1060 or (int(each["floor"]) == 1 and int(each["zone"]) == 2):
                if "deli" in indicator:
                    indicator["deli"] = round(indicator["deli"]+each["time"],1)
                else:
                    indicator["deli"] = each["time"]
            else:
                addr = "f"+str(each["floor"])+"z"+str(each["zone"])
                if addr in indicator:
                    indicator[addr] = round(indicator[addr]+each["time"],1)
                else:
                    indicator[addr] = each["time"]
        # print indicator
        # for each in indicator:
        #     if each in alladdr:
        #         alladdr[each] = round(alladdr[each]+indicator[each],1)
        #     else:
        #         alladdr[each] = indicator[each]
        for each in indicator:
            if each in alladdrdata:
                alladdrdata[each].append(indicator[each])
            else:
                alladdrdata[each] = [indicator[each]]
    for each in alladdrdata:
        if len(alladdrdata[each])<10:
            for i in range(10-len(alladdrdata[each])):
                alladdrdata[each].append(0)
        alladdrdata[each].sort()
        alladdr[each] = round(sum(alladdrdata[each][1:-1])/8.0,1)
    #print alladdr,f1z1refers to go outside
    return alladdr

@app.route('/getPersonalRadar')
def getPersonalRadar():
    name = request.args.get("name")
    time = int(request.args.get("time"))
    print name,time
    sql = "select floor,zone,office,unixtime from locationwithtime where proxid like '"+name+"' and unixtime >= "+str(time)+" and unixtime <= "+str(time+24*3600)
    c.execute(sql)
    rows = c.fetchall()
    location = []
    starttime = time
    for i in range(len(rows)):
        if rows[i][3]-starttime >= 7*60 and i>=1:
            row = {}
            row["floor"] = rows[i-1][0]
            row["zone"] = rows[i-1][1]
            row["office"] = rows[i-1][2]
            row["time"] = round((rows[i][3]-starttime)/3600.0,1)
            location.append(row)
        starttime = rows[i][3]
    #print location
    sql = "select floor,zone,office from employlist where proxid like '"+name[:-3]+"%'"
    c.execute(sql)
    own = c.fetchall()[0]
    ownoffice = own[2]
    ownfloor = own[0]
    ownzone = own[1]
    sql = "select office from employlist"
    c.execute(sql)
    officesres = c.fetchall()
    offices = []
    for each in officesres:
        offices.append(each[0])
    #print offices
    #print ownoffice,ownfloor,ownzone
    indicator = {}
    for each in location:
        #print each,each["floor"],each["zone"]
        if each["office"] == ownoffice or (int(each["floor"]) == int(ownfloor) and int(each["zone"]) == int(ownzone)):
            if "ownoffice" in indicator:
                indicator["ownoffice"] = round(indicator["ownoffice"]+each["time"],1)
            else:
                indicator["ownoffice"] = each["time"]
        elif each["office"] in offices:
            if "otheroffice" in indicator:
                indicator["otheroffice"] = round(indicator["otheroffice"]+each["time"],1)
            else:
                indicator["otheroffice"] = each["time"]
        elif each["office"] in [3330,3700,2700,2365,1030,1050]:
            if "conf" in indicator:
                indicator["conf"] = round(indicator["conf"]+each["time"],1)
            else:
                indicator["conf"] = each["time"]
        elif each["office"] == 1060 or (int(each["floor"]) == 1 and int(each["zone"]) == 2):
            if "deli" in indicator:
                indicator["deli"] = round(indicator["deli"]+each["time"],1)
            else:
                indicator["deli"] = each["time"]
        else:
            addr = "f"+str(each["floor"])+"z"+str(each["zone"])
            if addr in indicator:
                indicator[addr] = round(indicator[addr]+each["time"],1)
            else:
                indicator[addr] = each["time"]

    #print indicator
    allindicator = weekAverageDistribute(name)
    #print allindicator
    for each in allindicator:
        if each not in indicator:
            indicator[each] = 0.0
    ones = {'indicator':[],'data':[[[]],[[]]]}
    for each in allindicator:
        ones["indicator"].append({'name':each,'max':12})
        ones['data'][1][0].append(allindicator[each])
        ones['data'][0][0].append(indicator[each])
    #print ones
    return json.dumps(ones)

def tableToJson():


    SQL = """
    SELECT
	`F_2_Z_2: Lights Power` AS Lights_Power,
	`F_2_Z_2: Thermostat Temp` AS Thermostat_Temp,
	`F_2_Z_2: equipment Power` AS Equipment_Power,
	`F_2_VAV_SYS COOLING COIL Power` AS Floor_COOLING_Power,
	`F_2_VAV_SYS SUPPLY FAN:Fan Power` AS Floor_SUPPLY_Power,
	`F_2_Z_2 SUPPLY INLET Temperature` AS Zone_SUPPLY_Temp,
	`F_2_Z_2 VAV REHEAT Damper Position` AS Damper_Position,
	`F_2_Z_2 SUPPLY INLET Mass Flow Rate` AS Zone_SUPPLY_Rate,
	`F_2_Z_2: Thermostat Cooling Setpoint` AS Zone_Cooling_Setpoint,
	`F_2_VAV_SYS Outdoor Air Flow Fraction` AS Floor_Fraction,
	`F_2_VAV_SYS AIR LOOP INLET Temperature` AS Floor_LOOP_Temp,
	`F_2_VAV_SYS Outdoor Air Mass Flow Rate` AS Floor_Outdoor_Rate,
	`F_2_Z_2 RETURN OUTLET CO2 Concentration` AS Zone_CO2,
	`F_2_VAV_SYS SUPPLY FAN OUTLET Temperature` AS Floor_SUPPLY_temp,
	`F_2_VAV_SYS AIR LOOP INLET Mass Flow Rate` AS Floor_LOOP_Rate,
	`F_2_VAV_SYS SUPPLY FAN OUTLET Mass Flow Rate` AS Floor_SUPPLY_Rate,
	`F_1_Z_1: Mechanical Ventilation Mass Flow Rate` AS Ventilation_Rate,
	`Water Heater Gas Rate` AS Heater_Power,
	`Total Electric Demand Power` AS Building_Total_Power,
	-`Supply Side Inlet Temperature` + `Drybulb Temperature` AS Water_Rising_Temp,
	`F_1_Z_1: Lights Power` + `F_1_Z_2: Lights Power` + `F_1_Z_4: Lights Power` +
	`F_1_Z_5: Lights Power` + `F_1_Z_7: Lights Power` + `F_2_Z_1: Lights Power` +
	`F_2_Z_10: Lights Power` + `F_2_Z_11: Lights Power` + `F_2_Z_14: Lights Power` +
	`F_2_Z_15: Lights Power` + `F_2_Z_16: Lights Power` + `F_2_Z_2: Lights Power` +
	`F_2_Z_3: Lights Power` + `F_2_Z_4: Lights Power` + `F_2_Z_5: Lights Power` +
	`F_2_Z_6: Lights Power` + `F_2_Z_7: Lights Power` + `F_2_Z_8: Lights Power` +
	`F_2_Z_9: Lights Power` + `F_3_Z_1: Lights Power` + `F_3_Z_10: Lights Power` +
	`F_3_Z_2: Lights Power` + `F_3_Z_3: Lights Power` + `F_3_Z_5: Lights Power` +
	`F_3_Z_6: Lights Power` + `F_3_Z_7: Lights Power` + `F_3_Z_8: Lights Power` +
	`F_3_Z_9: Lights Power` + `F_1_Z_1: Equipment Power` + `F_1_Z_2: Equipment Power` +
	`F_1_Z_4: Equipment Power` + `F_1_Z_5: Equipment Power` + `F_1_Z_7: Equipment Power` +
	`F_2_Z_1: Equipment Power` + `F_2_Z_10: Equipment Power` + `F_2_Z_11: Equipment Power` +
	`F_2_Z_14: Equipment Power` + `F_2_Z_15: Equipment Power` + `F_2_Z_16: Equipment Power` +
	`F_2_Z_2: Equipment Power` + `F_2_Z_3: Equipment Power` + `F_2_Z_4: Equipment Power` +
	`F_2_Z_5: Equipment Power` + `F_2_Z_6: Equipment Power` + `F_2_Z_7: Equipment Power` +
	`F_2_Z_8: Equipment Power` + `F_2_Z_9: Equipment Power` + `F_3_Z_1: Equipment Power` +
	`F_3_Z_10: Equipment Power` + `F_3_Z_2: Equipment Power` + `F_3_Z_3: Equipment Power` +
	`F_3_Z_5: Equipment Power` + `F_3_Z_6: Equipment Power` + `F_3_Z_7: Equipment Power` +
	`F_3_Z_8: Equipment Power` + `HVAC Electric Demand Power` AS Power_Except,
	(`F_1_Z_1: Thermostat Temp`-`F_1_Z_1: Thermostat Cooling Setpoint`)*
	`F_1_Z_1 SUPPLY INLET Mass Flow Rate`+
	(`F_1_Z_2: Thermostat Temp`-`F_1_Z_2: Thermostat Cooling Setpoint`)*
	`F_1_Z_2 SUPPLY INLET Mass Flow Rate`+
	(`F_1_Z_3: Thermostat Temp`-`F_1_Z_3: Thermostat Cooling Setpoint`)*
	`F_1_Z_3 SUPPLY INLET Mass Flow Rate`+
	(`F_1_Z_4: Thermostat Temp`-`F_1_Z_4: Thermostat Cooling Setpoint`)*
	`F_1_Z_4 SUPPLY INLET Mass Flow Rate`+
	(`F_1_Z_5: Thermostat Temp`-`F_1_Z_5: Thermostat Cooling Setpoint`)*
	`F_1_Z_5 SUPPLY INLET Mass Flow Rate`+
	(`F_1_Z_7: Thermostat Temp`-`F_1_Z_7: Thermostat Cooling Setpoint`)*
	`F_1_Z_7 SUPPLY INLET Mass Flow Rate`+
	(`F_1_Z_8A: Thermostat Temp`-`F_1_Z_8A: Thermostat Cooling Setpoint`)*
	`F_1_Z_8A SUPPLY INLET Mass Flow Rate`+
	(`F_1_Z_8B: Thermostat Temp`-`F_1_Z_8B: Thermostat Cooling Setpoint`)*
	`F_1_Z_8B SUPPLY INLET Mass Flow Rate` as Rooms_Cooling_Sum,
	from_unixtime(
		`Date/Time` / 1000,
		'%Y-%m-%d %H:%i:%s'
	) AS time
	FROM
		bldg
	ORDER BY
		`Date/Time` ASC
    """

    c.execute(SQL)
    data = c.fetchall()
    jsonData = []
    for row in data:
        result = {}
        result['Lights_Power'] = row[0]
        result['Thermostat_Temp'] = row[1]
        result['Equipment_Power'] = row[2]
        result['Floor_COOLING_Power'] = row[3]
        result['Floor_SUPPLY_Power'] = row[4]
        result['Zone_SUPPLY_Temp'] = row[5]
        result['Damper_Position'] = row[6]
        result['Zone_SUPPLY_Rate'] = row[7]
        result['Zone_Cooling_Setpoint'] = row[8]
        result['Floor_Fraction'] = row[9]
        result['Floor_LOOP_Temp'] = row[10]
        result['Floor_Outdoor_Rate'] = row[11]
        result['Zone_CO2'] = row[12]
        result['Floor_SUPPLY_temp'] = row[13]
        result['Floor_LOOP_Rate'] = row[14]
        result['Floor_SUPPLY_Rate'] = row[15]
        result['Ventilation_Rate'] = row[16]
        result['Heater_Power'] = row[17]
        result['Building_Total_Power'] = row[18]
        result['Water_Rising_Temp'] = row[19]
        result['Power_Except'] = row[20]
        result['Rooms_Cooling_Sum'] = row[21]
        result['time'] = row[22]
        jsonData.append(result)
    return json.dumps(jsonData)


@app.route('/explore')
def init():
   return render_template('explore.html')


@app.route('/getData')
def getData():
    jsonData = tableToJson()
    return jsonData

if __name__ == '__main__':
    app.run(debug=True)
