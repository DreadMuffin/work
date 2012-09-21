#!/usr/bin/python

import re
import os

path = "/protokoller"
FIELDS = "scanfieldspraktisk"
PROTOKOL = "WB_FDG_PET_CT_5.MlAdult"

f = open(PROTOKOL,'r')
proto = f.read()
proto = proto.split("\n")

f = open(FIELDS,'r')
fields = f.read()
fields = fields.split("\n")

newProto = []
for item in proto:
    item = item.rstrip('\r\n')
    item = item.replace("\t"," ")
    item = re.sub(' +',' ',item)
#    if len(item) > 2:
    newProto.append(item)

proto = newProto



screens = {0 : dict()}
screenno = 0
index = 0
rindex = -1
recon = [0,0,0]
fieldlist = ""

for item in proto:
    if item.startswith(fields[index]):
        if item.startswith("No_Of_Valid_Recons"):
            rindex+=1
            recon[rindex] = int(item.split(" ")[1])
        elif item.startswith("MlModeRecon_End"):
            recon[rindex]-= 1
            if recon[rindex] > 0:
                if rindex == 0:
                    index = 15
                elif rindex == 1:
                    index = 42
                else: index = 82
        index+=1
        fieldlist+=item + "\n"

fieldlist = fieldlist[:-1]
f = open("fields_" + PROTOKOL,'w')
f.write(fieldlist)
f.close()

