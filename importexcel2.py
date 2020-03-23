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

if len(sys.argv) < 3:
    print("ERROR: You only passed in",str(len(sys.argv)-1),"arguments which is insufficient.")
    print("Usage: python importexcel2k.py <path/xlsx_filename.xlsx> <rowlimit>")
    sys.exit()

rowlimit = int(sys.argv[2])

if rowlimit%2000 != 0:
    print("ERROR: rowlimit must be in multiples of 2000")
    sys.exit()

if rowlimit < 2000:
    lowerlimit = 1
    upperlimit = 2000
else:
    lowerlimit = rowlimit -2000 + 1
    upperlimit = rowlimit

print("Range: ",str(lowerlimit),"to", str(upperlimit))

print("Reading File: " + sys.argv[1])
wb = xlrd.open_workbook(sys.argv[1])
sh = wb.sheet_by_index(0)
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
print("Establishing DB Connection")
print(mysqldb)
print("Determined no. of rows:" + str(sh.nrows))
print("Verifying no. of cols:" + str(sh.ncols))

alphanum_regular_expression = re.compile("[^a-zA-Z0-9]")
numcol = 0

cretabsql = "CREATE TABLE " + newtable + "("

for cols_counter in range(sh.ncols):
    print("col:" + str(cols_counter))
    colval = sh.row_values(0)[cols_counter]
    colval2 = colval.lstrip()
    colval3 = colval2.rstrip()
    colval3 = colval3.replace("\r","")
    colval3 = colval3.replace("\n","")
    colval4 = re.sub(alphanum_regular_expression,"",colval3)
    print(colval4)
    if colval4 == "":
        print("Empty Column Found... Revising Number of Columns")
    else:
        if numcol == 0:
            cretabsql = cretabsql + colval4 + " VARCHAR(200)"
        else:
            cretabsql = cretabsql + ", " + colval4 + " VARCHAR(200)"
        numcol += 1

cretabsql = cretabsql + ")"
print("###",cretabsql,"###")
print("Total cols: " + str(numcol))
print("Creating DB table " + newtable)
cursor.execute(cretabsql)


for i in range(sh.nrows):
    pos = 0
    if i == 0:
        print("skipping header row")
        dummy = 1
    else:
        if i<lowerlimit or i>upperlimit:
            print("skipping row",str(i))
        else:
            ins_sql = "INSERT INTO " + newtable + " VALUES ("
            for x in range(numcol):
                if is_number(sh.row_values(i)[x]):
                    #if (sh.row_values(i)[x])%1 == 0:
                    #    cellval = str(int(sh.row_values(i)[x]))
                    #else:
                    #    cellval = str(sh.row_values(i)[x])
                    cellval = str(sh.row_values(i)[x])
                else:
                    cellval = sh.row_values(i)[x]
                    cellval = cellval.replace("'","''")

                if x == 0:
                    ins_sql = ins_sql + "'" + cellval + "'"
                else:
                    ins_sql = ins_sql + ", '" + cellval + "'"

            ins_sql = ins_sql + ")"
            print(str(i+1),"###",ins_sql,"###")
            cursor.execute(ins_sql)

mysqldb.commit()
mysqldb.close()
print("#### Execution Completed for RowLimit ", str(rowlimit), "####")
