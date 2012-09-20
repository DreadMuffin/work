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
print proto

screens = {0 : dict()}
screenno = 0

for item in proto:
    # Identify series
    if item.startswith("PROTOCOL_ENTRY_NO:"):
        screenno = item.split()[1]
        screens[screenno] = dict()
        continue

    try:
        screens[screenno][item.split()[0]] = item.split()[1]
    except:
        pass

print screens[0]
