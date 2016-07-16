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
    return render_template("radar.html")

@app.route('/getBuildingdatas')
def getTotalParas():
    # sql = "select `Date/Time`,`Drybulb Temperature` as d,`Supply Side Inlet Temperature` as s,\
    #       `Drybulb Temperature`+`Supply Side Inlet Temperature` as sum from bldg"
    # sql = "select `Date/Time`,`Drybulb Temperature` as d,`Supply Side Inlet Temperature` as s,\
    #       -`Drybulb Temperature`+`Supply Side Inlet Temperature` as sum from bldg"
    #sql = "select `Date/Time`,`HVAC Electric Demand Power` as sum from bldg"
#     sql = "select `Date/Time`,FROM_UNIXTIME(`Date/Time`/1000,'%Y-%m-%d %H:%i:%S'),`F_1_Z_1: Lights Power`+`F_1_Z_2: Lights Power`+`F_1_Z_4: Lights Power`+`F_1_Z_5: Lights Power`+`F_1_Z_7: Lights Power`+`F_2_Z_1: Lights Power`+`F_2_Z_10: Lights Power`+`F_2_Z_11: Lights Power`+\
# `F_2_Z_14: Lights Power`+`F_2_Z_15: Lights Power`+`F_2_Z_16: Lights Power`+`F_2_Z_2: Lights Power`+`F_2_Z_3: Lights Power`+`F_2_Z_4: Lights Power`+`F_2_Z_5: Lights Power`+`F_2_Z_6: Lights Power`+`F_2_Z_7: Lights Power`+`F_2_Z_8: Lights Power`+`F_2_Z_9: Lights Power`+\
# `F_3_Z_1: Lights Power`+`F_3_Z_10: Lights Power`+`F_3_Z_2: Lights Power`+`F_3_Z_3: Lights Power`+`F_3_Z_5: Lights Power`+`F_3_Z_6: Lights Power`+`F_3_Z_7: Lights Power`+`F_3_Z_8: Lights Power`+`F_3_Z_9: Lights Power`+\
# `F_1_Z_1: Equipment Power`+`F_1_Z_2: Equipment Power`+`F_1_Z_4: Equipment Power`+`F_1_Z_5: Equipment Power`+`F_1_Z_7: Equipment Power`+\
# `F_2_Z_1: Equipment Power`+`F_2_Z_10: Equipment Power`+`F_2_Z_11: Equipment Power`+`F_2_Z_14: Equipment Power`+`F_2_Z_15: Equipment Power`+`F_2_Z_16: Equipment Power`+`F_2_Z_2: Equipment Power`+`F_2_Z_3: Equipment Power`+\
# `F_2_Z_4: Equipment Power`+`F_2_Z_5: Equipment Power`+`F_2_Z_6: Equipment Power`+`F_2_Z_7: Equipment Power`+`F_2_Z_8: Equipment Power`+`F_2_Z_9: Equipment Power`+\
# `F_3_Z_1: Equipment Power`+`F_3_Z_10: Equipment Power`+`F_3_Z_2: Equipment Power`+`F_3_Z_3: Equipment Power`+`F_3_Z_5: Equipment Power`+`F_3_Z_6: Equipment Power`+`F_3_Z_7: Equipment Power`+`F_3_Z_8: Equipment Power`+\
# `HVAC Electric Demand Power`-`Total Electric Demand Power` as tdiff from bldg order by `Date/Time`"
    #sql = "select `Date/Time`,`F_2_BATH_EXHAUST:Fan Power` from bldg"
    #sql = "select `Date/Time`,`F_3_VAV_SYS AIR LOOP INLET Mass Flow Rate` from bldg"
    #sql = "select `Date/Time`,`F_3_VAV_SYS SUPPLY FAN OUTLET Mass Flow Rate` from bldg"
    #sql = "select `Date/Time`,`F_3_VAV_SYS Outdoor Air Mass Flow Rate` from bldg"
    #sql = "select `Date/Time`,`F_2_VAV_SYS AIR LOOP INLET Temperature` from bldg"
    #sql = "select `Date/Time`,`Drybulb Temperature` from bldg"
    sql = "select `Date/Time`,`F_3_VAV_SYS COOLING COIL Power` from bldg"
    sql = "select `Date/Time`,`F_3_VAV_SYS Outdoor Air Flow Fraction` from bldg"
    #sql = "select `Date/Time`,`F_1_VAV_SYS Outdoor Air Mass Flow Rate`/`F_1_VAV_SYS SUPPLY FAN OUTLET Mass Flow Rate` from bldg"
    sql = "select `Date/Time`,`Water Heater Gas Rate` from bldg"
    sql = "select `Date/Time`,`F_1_VAV_SYS AIR LOOP INLET Temperature` from bldg"
    sql = "select `Date/Time`,`F_3_VAV_SYS SUPPLY FAN:Fan Power` from bldg"
    sql = "select `Date/Time`,`F_2_VAV_SYS SUPPLY FAN OUTLET Temperature` from bldg"

    #sql = "select `Date/Time`,(`F_1_Z_1: Thermostat Cooling Setpoint`+`F_1_Z_1: Thermostat Heating Setpoint`)/2 from bldg"
    #sql = "select `Date/Time`,`F_2_Z_4: Thermostat Cooling Setpoint` from bldg"
    sql = "select `Date/Time`,`F_1_Z_1: Thermostat Temp` from bldg"
    sql = "select `Date/Time`,`F_1_Z_1: Thermostat Cooling Setpoint` from bldg"
    sql = "select `Date/Time`,`F_1_Z_1: Thermostat Heating Setpoint` from bldg"
    sql = "select `Date/Time`,`F_1_Z_1 SUPPLY INLET Temperature` from bldg"
    sql = "select `Date/Time`,`F_1_VAV_SYS Outdoor Air Flow Fraction` from bldg"
    sql = "select `Date/Time`,`F_1_VAV_SYS SUPPLY FAN OUTLET Temperature` from bldg" #hvac fan

    sql = "select `Date/Time`,`F_1_Z_1 SUPPLY INLET Temperature` from bldg" #supply box to zone
    sql = "select `Date/Time`,`F_1_Z_1: Thermostat Cooling Setpoint` from bldg"
    sql = "select `Date/Time`,`F_1_Z_1: Thermostat Temp` from bldg"
    sql = "select `Date/Time`,`F_1_VAV_SYS AIR LOOP INLET Temperature` from bldg"
    sql = "select `Date/Time`,`F_1_Z_1: Thermostat Temp`,`F_1_VAV_SYS SUPPLY FAN OUTLET Temperature` from bldg"
    #sql = "select `Date/Time`,`F_1_VAV_SYS Outdoor Air Flow Fraction` from bldg"
    #sql = "select `Date/Time`,(`F_1_Z_1: Thermostat Heating Setpoint`+`F_1_Z_1: Thermostat Cooling Setpoint`*2)/2 from bldg"
    #sql = "select `Date/Time`,`F_1_Z_3: Thermostat Cooling Setpoint` from bldg"
    #sql = "select `Date/Time`,`F_1_Z_1: Thermostat Temp` from bldg"
    #sql = "select `Date/Time`,`Drybulb Temperature` from bldg"
    #sql = "select `Date/Time`,`F_3_VAV_SYS AIR LOOP INLET Temperature` from bldg"
    #sql = "select `Date/Time`,`F_1_VAV_SYS HEATING COIL Power` from bldg"
    # sql = "select `Date/Time`,`F_1_Z_1: Thermostat Temp`,\
    #               `Drybulb Temperature`,\
    #               `F_1_Z_1: Thermostat Cooling Setpoint`,\
    #               `F_1_Z_1: Thermostat Heating Setpoint`,\
    #               `F_1_Z_1 SUPPLY INLET Temperature`,\
    #               `F_1_VAV_SYS SUPPLY FAN OUTLET Temperature`,\
    #               `F_1_Z_1 SUPPLY INLET Mass Flow Rate`*10,\
    #               `F_1_VAV_SYS AIR LOOP INLET Temperature`,\
    #               `F_1_Z_1 RETURN OUTLET CO2 Concentration`/100,\
    #               `F_1 VAV Availability Manager Night Cycle Control Status` from bldg"
    # sql = "select `Date/Time`,`F_1_Z_8a REHEAT COIL Power`/200,\
    #               `F_1_Z_8a RETURN OUTLET CO2 Concentration`/100,\
    #               `F_1_Z_8a SUPPLY INLET Mass Flow Rate`*10,\
    #               `F_1_Z_8a SUPPLY INLET Temperature`,\
    #               `F_1_Z_8a VAV REHEAT Damper Position`,\
    #               `F_1_Z_8a: Equipment Power`/20,\
    #               `F_1_Z_8a: Lights Power`/20,\
    #               `F_1_Z_8a: Thermostat Temp`,\
    #               `F_1_Z_8a: Thermostat Cooling Setpoint`,\
    #               `F_1_Z_8a: Thermostat Heating Setpoint`,\
    #               `Drybulb Temperature` \
    #                from bldg"
    sql = "select `Date/Time`,`F_2_Z_8 REHEAT COIL Power`/200,\
                  `F_2_Z_8 RETURN OUTLET CO2 Concentration`/200,\
                  `F_2_Z_8 SUPPLY INLET Mass Flow Rate`*10,\
                  `F_2_Z_8 SUPPLY INLET Temperature`,\
                  `F_2_Z_8 VAV REHEAT Damper Position`,\
                  `F_2_Z_8: Equipment Power`/20,\
                  `F_2_Z_8: Lights Power`/20,\
                  `F_2_Z_8: Thermostat Temp`,\
                  `F_2_Z_8: Thermostat Cooling Setpoint`,\
                  `F_2_Z_8: Thermostat Heating Setpoint`,\
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
    sql = "select floor(UNIX_TIMESTAMP(Date)*1000),concentrate from `f3z1-MC2`"
    c.execute(sql)
    rows = c.fetchall()
    one = []
    for row in rows:
        one.append([row[0]+8*3600000,row[1]])
    ones.append(one)
    return json.dumps(ones)

@app.route('/getBuildingdata')
def getTotalPara():
    sql = "select `Date/Time`,`F_1_Z_5 REHEAT COIL Power`/100 from bldg"
    c.execute(sql)
    ones = [[i[0]+8*3600000,i[1]] for i in c.fetchall()]
    return json.dumps(ones)

def weekAverageDistribute(name):
    proxid = name
    origintime = 1464624000
    sql = "select floor,zone,office from employlist where proxid like '"+name+"%'"
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
        sql = "select floor,zone,office,unixtime from locationwithtime where proxid like '"+name+"%' and unixtime >= "+str(time)+" and unixtime < "+str(time+24*3600)
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
    sql = "select floor,zone,office,unixtime from locationwithtime where proxid like '"+name+"%' and unixtime >= "+str(time)+" and unixtime <= "+str(time+24*3600)
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
    sql = "select floor,zone,office from employlist where proxid like '"+name+"%'"
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

if __name__ == '__main__':
    app.run(debug=True)