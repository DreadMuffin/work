#!/usr/bin/python

import os
import pymysql

print "Creating the database"

source = "dprotokoller/"
listing = os.listdir(source)

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root',
        passwd='mysql',db='protokoller')
cur = conn.cursor()
cur.execute("set autocommit = 0")
conn.commit()

cur.execute("use protokoller")
tables = ["Protocols","Topograms","CT","CTrecon","Pause","PET","PETrecon"]

for t in tables:
    try:
        cur.execute("drop table " + t + ";")
    except:
        pass

cur.execute("create table Protocols (Protocolname varchar(200), " +
        "CustomProtocol int, PETscanner " +
        "char(10),Bodysize char(20),Length int,Date datetime,PRIMARY " +
        "KEY (Protocolname,PETscanner));")

cur.execute("create table Topograms (Protocolname varchar(200), PETscanner char(10)" +
        ",Modenr int,Name varchar(20), mA int,kV int,Topogramlength int," +
        "TubePosition varchar(10),Delay int,Direction varchar(20)" +
        ",APIid int,Kernel varchar(30),Window varchar(30),Primary key " +
        "(Protocolname,PETscanner,Modenr))")

cur.execute("create table CT (Protocolname varchar(200),PETscanner char(10), Modenr" +
        " int,Recons int, Name varchar(20)" +
        ",Eff_mAs int,kV int,Care_Dose4D varchar(10),CareDoseType varchar(30)" +
        ",CTDlvol double,ScanTime double,Delay int,Slice int,Tilt int," +
        "QualityRefmAs int,Rotationtime double,Pitch int,Direction varchar(30)" +
        ",Primary Key (Protocolname,PETscanner,Modenr))")

cur.execute("create table CTrecon (Protocolname varchar(200),PETscanner char(10)," +
        "Modenr int,Reconnumber int," +
        "Seriesdescription varchar(40),Slice double,Kernel varchar(20),Window " +
        "varchar(30),ExtendedFoV varchar(10),FoV int, CenterX int, CenterY " +
        "int, Mirroring varchar(20),ExtendedCTscale varchar(20),ReconJob " +
        "varchar(20),ReconAxis varchar(20),ImageOrder varchar(20)," +
        "ReconIncrement double,No_of_images int,Primary key (Protocolname," +
        "PETscanner,Modenr,Reconnumber))")

cur.execute("create table Pause (Protocolname varchar(200),PETscanner char(10)," +
        "Modenr int,Primary key (Protocolname,PETscanner,Modenr))")

cur.execute("create table PET (Protocolname varchar(200),PETscanner char(10)," +
        "Modenr int,Recons int, Name varchar(20), Isotope varchar(20)," +
        "Pharm varchar(20),Injdose int,Injdoseunit varchar(15)," +
        "Scanmode varchar(15)," +
        "Scanrange varchar(20),Numberofbeds int,Scanduration double," +
        "Scandurationunit varchar(10)," +
        "Autoload varchar(5),Rebinnerlut varchar(5),Scanoutput varchar(15)," +
        "Sinogrammode varchar(10),Inputtriggersignal varchar(15),LLD int," +
        "ULD int,Primary key(Protocolname,PETscanner,Modenr))")

cur.execute("create table PETrecon (Protocolname varchar(200),PETscanner char(10)," +
        "Modenr int,Reconnumber int,Seriesdescription varchar(30),Reconrange" +
        " varchar(30),Outputimagetype varchar(20),Reconmethod varchar(20)," +
        "Iterations int,Subsets int,Imagesize int,Zoom int,Filter varchar(20),"+
        "FVHM int,Offsetx int,Offsety int,Attenuationcorrection varchar(10)," +
        "ScatterCorrection varchar(10),MatchCTslicelocation varchar(10)," +
        "Saveintermediatedata varchar(10),Primary key(Protocolname,PETscanner," +
        "Modenr,Reconnumber))")

for file in listing:
    if file.startswith("."):
        pass
    else:
        f = open(source+file,'r')
        lines = f.read().split("\n")
        for line in lines[:-1]:
            cur.execute(line)

conn.commit()
conn.close()

# r = cur.fetchall()
# print r
# ...or...
#for r in cur.fetchall():
#    print r

#    cur.close()
#    conn.close()
