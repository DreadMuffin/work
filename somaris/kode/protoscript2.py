#!/usr/bin/python

import re
import os

FIELDS = "scanfieldspraktisk"

f = open(FIELDS,'r')
fields = f.read()
fields = fields.split("\n")

path = "protokoller2/"
path2 = "fprotokoller/"
listing = os.listdir(path)
for file in listing:

    f = open(path + file,'r')
    proto = f.read()
    proto = proto.split("\n")

    newProto = []
    for item in proto:
        item = item.rstrip('\r\n')
        item = item.replace("\t"," ")
        item = re.sub(' +',' ',item)
        newProto.append(item)

    proto = newProto



    screens = {0 : dict()}
    screenno = 0
    index = 0
    rindex = -1
    recon = [0,0,0]
    fieldlist = ""
    reconpos = [i for i, x in enumerate(fields) if x == "No_Of_Valid_Recons"]

    for item in proto:
        if item.startswith(fields[index]):
            if item.startswith("No_Of_Valid_Recons"):
                rindex+=1
                recon[rindex] = int(item.split(" ")[1])
            elif item.startswith("MlModeRecon_End"):
                recon[rindex]-= 1
                if recon[rindex] > 0:
                    if rindex == 0:
                        index = reconpos[0]
                    elif rindex == 1:
                        index = reconpos[1]
                    else: index = reconpos[2]
            index+=1
            fieldlist+=item + "\n"
    




    fieldlist = fieldlist[:-1]
    f = open(path2 + "fields_" + file,'w')
    f.write(fieldlist)
    f.close()



