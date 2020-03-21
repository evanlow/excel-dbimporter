import mysql.connector
import datetime
import os
import pickle
import sys
import calendar
import csv
import xlrd
import re
from datetime import datetime

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

now = datetime.now()
timestampstr = now.strftime("%Y%m%d%H%M%S")
newtable = "IMPORTED_" + timestampstr



dbconfigfile = csv.reader(open(".dbconfig", "r"))
for dbconfig in dbconfigfile:
    dbhost = dbconfig[0]
    dbuser = dbconfig[1]
    dbpasswd = dbconfig[2]
    db = dbconfig[3]

mysqldb = mysql.connector.connect(
    host = dbconfig[0],
    user = dbconfig[1],
    passwd = dbconfig[2],
    database = dbconfig[3]
)

cursor = mysqldb.cursor()

print("Reading File: " + sys.argv[1])
wb = csv.reader(open(sys.argv[1], "r"))
rowItem=[None]*200
alphanum_regular_expression = re.compile("[^a-zA-Z0-9]")
reccount = 0
rownum = 0
headercolcount = 0


cretabsql = "CREATE TABLE " + newtable + " ("

for row in wb:
        idx = 0
        ins_sql = "INSERT INTO " + newtable + " VALUES ("
        #if reccount == 0:
        #    reccount += 1
        #    continue
        #else:
        #    reccount +=
        for col in row:
            if rownum == 0:
                print("### detecting header columns ###")
                colval = col.replace("'","''").lstrip().rstrip().replace("\r","").replace("\n","").replace(" ","").replace("(","").replace(")","")
                rowItem[idx] = re.sub(alphanum_regular_expression,"",colval)
                print("rowItem[%d" %(idx) + "]: %s" %(rowItem[idx]))
                if len(col) == 0:
                    print("Empty column found")
                else:
                    if idx == 0:
                        cretabsql = cretabsql + rowItem[idx] + " VARCHAR(200)"
                    else:
                        cretabsql = cretabsql + ", " + rowItem[idx] + " VARCHAR(200)"

                    headercolcount += 1
                idx += 1
            else:
                rowItem[idx] = col.replace("'","''").lstrip().rstrip().replace("\r","").replace("\n","")
                print("rowItem[%d" %(idx) + "]: %s" %(rowItem[idx]))
                if idx<headercolcount:
                    if idx == 0:
                        ins_sql = ins_sql + "'" + rowItem[idx] + "'"
                    else:
                        ins_sql = ins_sql + "," + "'" + rowItem[idx] + "'"

                idx += 1

        if rownum == 0:
            cretabsql = cretabsql + ")"
            #create table and Columns
            print("Create TABLE ", newtable, "###", cretabsql ,"###")
            cursor.execute(cretabsql)
        else:
            ins_sql = ins_sql + ")"
            print("INSERTING: ","####", ins_sql, "####")
            cursor.execute(ins_sql)


        rownum +=1


mysqldb.commit()
mysqldb.close()
