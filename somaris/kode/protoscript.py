#!/usr/bin/python

import re

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
    if len(item) > 2:
        newProto.append(item)

proto = newProto

screens = {0 : dict()}
screenno = 0
index = 0
rindex = -1
recon = [0,0,0]
foo = 0


for item in proto:
    foo+=1
    
    # Identify series
    if item.startswith(fields[index]):
        print index
        print foo
        if item.startswith("No_Of_Valid_Recons"):
            rindex+=1
            recon[rindex] = int(item.split(" ")[1])
        if item.startswith("MlModeRecon_End"):
            recon[rindex]-= 1
            if recon[rindex] > 0:
                print index
                if rindex == 0:
                    index = 15
                elif rindex == 1:
                    index = 42
                else: index = 82
        index+=1
#        print item


print recon
print index
print rindex
print len(proto)

