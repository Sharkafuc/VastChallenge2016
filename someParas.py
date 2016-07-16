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
    return render_template("somePara.html")

@app.route('/getBuildingdata')
def getTotalParas():
    # sql = "select `Date/Time`,(`F_1_Z_1: Thermostat Temp`-`F_1_Z_1: Thermostat Cooling Setpoint`)*\
    #         `F_1_Z_1 SUPPLY INLET Mass Flow Rate`+\
    #         (`F_1_Z_2: Thermostat Temp`-`F_1_Z_2: Thermostat Cooling Setpoint`)*\
    #         `F_1_Z_2 SUPPLY INLET Mass Flow Rate`+\
    #         (`F_1_Z_3: Thermostat Temp`-`F_1_Z_3: Thermostat Cooling Setpoint`)*\
    #         `F_1_Z_3 SUPPLY INLET Mass Flow Rate`+\
    #         (`F_1_Z_4: Thermostat Temp`-`F_1_Z_4: Thermostat Cooling Setpoint`)*\
    #         `F_1_Z_4 SUPPLY INLET Mass Flow Rate`+\
    #         (`F_1_Z_5: Thermostat Temp`-`F_1_Z_5: Thermostat Cooling Setpoint`)*\
    #         `F_1_Z_5 SUPPLY INLET Mass Flow Rate`+\
    #         (`F_1_Z_7: Thermostat Temp`-`F_1_Z_7: Thermostat Cooling Setpoint`)*\
    #         `F_1_Z_7 SUPPLY INLET Mass Flow Rate`+\
    #         (`F_1_Z_8A: Thermostat Temp`-`F_1_Z_8A: Thermostat Cooling Setpoint`)*\
    #         `F_1_Z_8A SUPPLY INLET Mass Flow Rate`+\
    #         (`F_1_Z_8B: Thermostat Temp`-`F_1_Z_8B: Thermostat Cooling Setpoint`)*\
    #         `F_1_Z_8B SUPPLY INLET Mass Flow Rate`,\
    #         `F_1_VAV_SYS COOLING COIL Power`/1000,2 from bldg"
    # sql = "select `Date/Time`,`F_1_Z_1: Thermostat Temp`,\
    #       `F_1_Z_1 REHEAT COIL Power`/100,\
    #       `F_1_Z_1 SUPPLY INLET Temperature`,\
    #       `F_1_Z_1 SUPPLY INLET Mass Flow Rate`*100 from bldg"
    # sql = "select `Date/Time`,(`F_3_Z_9: Thermostat Temp`-`F_1_Z_1: Thermostat Cooling Setpoint`)*\
    #         `F_1_Z_1 SUPPLY INLET Mass Flow Rate`+\
    #         (`F_1_Z_2: Thermostat Temp`-`F_1_Z_2: Thermostat Cooling Setpoint`)*\
    #         `F_1_Z_2 SUPPLY INLET Mass Flow Rate`+\
    #         (`F_1_Z_3: Thermostat Temp`-`F_1_Z_3: Thermostat Cooling Setpoint`)*\
    #         `F_1_Z_3 SUPPLY INLET Mass Flow Rate`+\
    #         (`F_1_Z_4: Thermostat Temp`-`F_1_Z_4: Thermostat Cooling Setpoint`)*\
    #         `F_1_Z_4 SUPPLY INLET Mass Flow Rate`+\
    #         (`F_1_Z_5: Thermostat Temp`-`F_1_Z_5: Thermostat Cooling Setpoint`)*\
    #         `F_1_Z_5 SUPPLY INLET Mass Flow Rate`+\
    #         (`F_1_Z_7: Thermostat Temp`-`F_1_Z_7: Thermostat Cooling Setpoint`)*\
    #         `F_1_Z_7 SUPPLY INLET Mass Flow Rate`+\
    #         (`F_1_Z_8A: Thermostat Temp`-`F_1_Z_8A: Thermostat Cooling Setpoint`)*\
    #         `F_1_Z_8A SUPPLY INLET Mass Flow Rate`+\
    #         (`F_1_Z_8B: Thermostat Temp`-`F_1_Z_8B: Thermostat Cooling Setpoint`)*\
    #         `F_1_Z_8B SUPPLY INLET Mass Flow Rate`,\
    #         `F_1_VAV_SYS COOLING COIL Power`/4000 from bldg"
    # floor = '3'
    # zone = '9'
    # sql = "select `Date/Time`,0,\
    #               `F_"+floor+"_Z_"+zone+" RETURN OUTLET CO2 Concentration`/200,\
    #               `F_"+floor+"_Z_"+zone+" SUPPLY INLET Mass Flow Rate`*20,\
    #               `F_"+floor+"_Z_"+zone+" SUPPLY INLET Temperature`,\
    #               0,\
    #               0,\
    #               `F_"+floor+"_Z_"+zone+": Lights Power`/20,\
    #               `F_"+floor+"_Z_"+zone+": Thermostat Temp`,\
    #               `F_"+floor+"_Z_"+zone+": Thermostat Cooling Setpoint`,\
    #               `F_"+floor+"_Z_"+zone+": Thermostat Heating Setpoint`,\
    #               `Drybulb Temperature` \
    #                from bldg"
    # c.execute(sql)
    # rows = c.fetchall()
    # c.execute(sql)
    # ones = []
    # rows = c.fetchall()
    # for i in range(1,12):
    #     one = []
    #     for row in rows:
    #         one.append([row[0]+8*3600000,row[i]])
    #     ones.append(one)

    #print ones
    # ones = []
    # rows = c.fetchall()
    # for i in range(1,5):
    #     one = []
    #     for row in rows:
    #         one.append([row[0]+8*3600000,row[i]])
    #     ones.append(one)
    ones = []
    sql = "select floor(UNIX_TIMESTAMP(Date))*1000,concentrate from `f1z8a-MC2`"
    one = []
    c.execute(sql)
    rows = c.fetchall()
    for row in rows:
        one.append([row[0]+8*3600000,row[1]])
    ones.append(one)

    sql = "select floor(UNIX_TIMESTAMP(Date))*1000,concentrate from `f2z2-MC2`"
    one = []
    c.execute(sql)
    rows = c.fetchall()
    for row in rows:
        one.append([row[0]+8*3600000,row[1]])
    ones.append(one)

    sql = "select floor(UNIX_TIMESTAMP(Date))*1000,concentrate from `f2z4-MC2`"
    one = []
    c.execute(sql)
    rows = c.fetchall()
    for row in rows:
       one.append([row[0]+8*3600000,row[1]])
    ones.append(one)

    sql = "select floor(UNIX_TIMESTAMP(Date))*1000,concentrate from `f3z1-MC2`"
    one = []
    c.execute(sql)
    rows = c.fetchall()
    for row in rows:
        one.append([row[0]+8*3600000,row[1]])
    ones.append(one)

    sql = "select `Date/Time`,`F_1_Z_8a RETURN OUTLET CO2 Concentration`/100 from bldg"
    one = []
    c.execute(sql)
    rows = c.fetchall()
    for row in rows:
        one.append([row[0]+8*3600000,row[1]])
    ones.append(one)

    sql = "select `Date/Time`,`F_2_Z_2 RETURN OUTLET CO2 Concentration`/100 from bldg"
    one = []
    c.execute(sql)
    rows = c.fetchall()
    for row in rows:
        one.append([row[0]+8*3600000,row[1]])
    ones.append(one)

    sql = "select `Date/Time`,`F_2_Z_4 RETURN OUTLET CO2 Concentration`/100 from bldg"
    one = []
    c.execute(sql)
    rows = c.fetchall()
    for row in rows:
        one.append([row[0]+8*3600000,row[1]])
    ones.append(one)

    sql = "select `Date/Time`,`F_3_Z_1 RETURN OUTLET CO2 Concentration`/100 from bldg"
    one = []
    c.execute(sql)
    rows = c.fetchall()
    for row in rows:
        one.append([row[0]+8*3600000,row[1]])
    ones.append(one)

    sql = "select `Date/Time`,`F_1_Z_8A: Thermostat Cooling Setpoint` from bldg"
    one = []
    c.execute(sql)
    rows = c.fetchall()
    for row in rows:
        one.append([row[0]+8*3600000,row[1]])
    ones.append(one)

    sql = "select `Date/Time`,`F_2_Z_2: Thermostat Cooling Setpoint` from bldg"
    one = []
    c.execute(sql)
    rows = c.fetchall()
    for row in rows:
        one.append([row[0]+8*3600000,row[1]])
    ones.append(one)

    sql = "select `Date/Time`,`F_2_Z_4: Thermostat Cooling Setpoint` from bldg"
    one = []
    c.execute(sql)
    rows = c.fetchall()
    for row in rows:
        one.append([row[0]+8*3600000,row[1]])
    ones.append(one)

    sql = "select `Date/Time`,`F_3_Z_1: Thermostat Cooling Setpoint` from bldg"
    one = []
    c.execute(sql)
    rows = c.fetchall()
    for row in rows:
        one.append([row[0]+8*3600000,row[1]])
    ones.append(one)

    sql = "select `Date/Time`,`F_1_Z_8A: Thermostat Heating Setpoint` from bldg"
    one = []
    c.execute(sql)
    rows = c.fetchall()
    for row in rows:
        one.append([row[0]+8*3600000,row[1]])
    ones.append(one)

    sql = "select `Date/Time`,`F_2_Z_2: Thermostat Heating Setpoint` from bldg"
    one = []
    c.execute(sql)
    rows = c.fetchall()
    for row in rows:
        one.append([row[0]+8*3600000,row[1]])
    ones.append(one)

    sql = "select `Date/Time`,`F_2_Z_4: Thermostat Heating Setpoint` from bldg"
    one = []
    c.execute(sql)
    rows = c.fetchall()
    for row in rows:
        one.append([row[0]+8*3600000,row[1]])
    ones.append(one)

    sql = "select `Date/Time`,`F_3_Z_1: Thermostat Heating Setpoint` from bldg"
    one = []
    c.execute(sql)
    rows = c.fetchall()
    for row in rows:
        one.append([row[0]+8*3600000,row[1]])
    ones.append(one)

    return json.dumps(ones)

if __name__ == '__main__':
    app.run(debug=True)