#!/usr/bin/python

import re
import os

FIELDS = "scanfields34"

f = open(FIELDS,'r')
tfields = f.read()
tfields = tfields.split("newmode:")

start = tfields[0].split("\n")[:-1]
topogram = tfields[1].split("\n")[1:-1]
ct = tfields[2].split("\n")[1:-1]
pause = tfields[3].split("\n")[1:-1]
pet = tfields[4].split("\n")[1:-1]


path = "protokoller34/"
path2 = "fprotokoller/"
listing = os.listdir(path)

def listappend(list,input):
    for item in input:
        list.append(item)

for file in listing:
#    try:


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

        searching = False
        searchingtc = False
        fields = []
        listappend(fields,start)
        protoorder = []
    
        for i,item in enumerate(proto):
            if searching:
                if item.startswith("MlPause_Begin"):
                    searching = False
                    listappend(fields,pause)
                    protoorder.append("pause")
                elif item.startswith("MlOtherModalityEntry_Begin"):
                    searching = False
                    listappend(fields,pet)
                    protoorder.append("pet")
                elif item.startswith("MlModeScan_Begin:"):
                    searchingtc = True
                    searching = False
            elif searchingtc:
                if item.startswith("RangeName") and item.endswith("\"Topogram\""):
                    protoorder.append("topo")
                    listappend(fields,topogram)
                    searchingtc = False
                elif item.startswith("RangeName"):
                    protoorder.append("ct")
                    listappend(fields,ct)
                    searchingtc = False
            elif item.startswith("PROTOCOL_ENTRY_NO"):
                searching = True
        print protoorder


        fields.append("MlScanProtocol_End")
        fields.append("Det her slutter den ikke med")
        findex = 0
        rindex = -1
        recon = [0] * (len(protoorder) - protoorder.count("p"))
        protonr = 0
        fieldlist = ""
        reconpos = [i for i, x in enumerate(fields) if x == "No_Of_Valid_Recons"]
    
        for i,item in enumerate(proto):
            if item.startswith(fields[findex]):
                if item.startswith("No_Of_Valid_Recons"):
                    rindex+=1
                    recon[rindex] = int(item.split(" ")[1])
                elif item.startswith("MlModeRecon_End"):
                    recon[rindex]-= 1
                    if recon[rindex] > 0:
                        findex = reconpos[rindex]
                elif item.startswith("PROTOCOL_ENTRY_NO"):
                    item = protoorder[protonr] + "\n" + item
                    protonr+=1
                findex+=1
                fieldlist+=item + "\n"
                
    
        fieldlist = fieldlist[:-1]
        f = open(path2 + "fields34_" + file,'w')
        f.write(fieldlist)
        f.close()

#    except:
# 
