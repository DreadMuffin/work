#!/usr/bin/python

import os
import pymysql

source = "dprotokoller/"
listing = os.listdir(source)

#conn = pymysql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock',
#user='root', passwd=None, db='mysql')

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='mysql',
                       db='protokoller')
cur = conn.cursor()

cur.execute("use protokoller")
cur.execute("drop table Protokoller;")
cur.execute("create table Protokoller (Name varchar(200),PETscanner " +
        "char(10),Bodysize char(20),Lenght int,Date datetime);")

for file in listing:
    print file
    f = open(source+file,'r').read()
    print "insert into Protokoller values (" + f + ");"
    cur.execute("insert into Protokoller values (" + f + ");")

cur.execute("SELECT * FROM Protokoller")

print cur.description

# r = cur.fetchall()
# print r
# ...or...
for r in cur.fetchall():
    print r

    cur.close()
#    conn.close()
