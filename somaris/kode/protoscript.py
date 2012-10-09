#!/usr/bin/python

import re
import os

FIELDS = "fieldsopdelt"

f = open(FIELDS,'r')
fields = f.read()
fields = fields.split("newmode:")

start = fields[0].split("\n")[:-1]
topogram = fields[1].split("\n")[1:-1]
ct = fields[2].split("\n")[1:-1]
pause = fields[3].split("\n")[1:-1]
pet = fields[4].split("\n")[1:-1]


path = "prototest/"
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
        fields = start
        protoorder = []
    
        for i,item in enumerate(proto):
            if searching:
                if item.startswith("MlPause_Begin"):
                    searching = False
                    listappend(fields,pause)
                    protoorder.append("p")
                elif item.startswith("MlOtherModalityEntry_Begin"):
                    searching = False
                    listappend(fields,pet)
                    protoorder.append("r")
                elif item == "MapProtocolEntryUID: 1":
                    searching = False
                    protoorder.append("t")
                    listappend(fields,topogram)
                elif item == "MapProtocolEntryUID: 2":
                    searching = False
                    protoorder.append("c")
                    listappend(fields,ct)
            elif item.startswith("PROTOCOL_ENTRY_NO"):
                searching = True
    
        findex = 0
        rindex = -1
        recon = [0] * (len(protoorder) - protoorder.count("p"))
        fieldlist = ""
        reconpos = [i for i, x in enumerate(fields) if x == "No_Of_Valid_Recons"]
      

        print fields
    
        for i,item in enumerate(proto):
            if item.startswith(fields[findex]):
                if item.startswith("No_Of_Valid_Recons"):
                    rindex+=1
                    recon[rindex] = int(item.split(" ")[1])
                    print recon
                elif item.startswith("MlModeRecon_End"):
                    recon[rindex]-= 1
                    if recon[rindex] > 0:
                        findex = reconpos[rindex]
#                        if rindex == 0:
#                            findex = reconpos[0]
#                        elif rindex == 1:
#                            findex = reconpos[1]
#                        else: findex = reconpos[2]
                findex+=1
                fieldlist+=item + " " + str(i) + "\n"
#            if item.startswith("MapProtocolEntryUID:") and int(item[-1]) == 6:
#                print file + " " + item
    




        fieldlist = fieldlist[:-1]
        f = open(path2 + "fields56_" + file,'w')
        f.write(fieldlist)
        f.close()

#    except:
#        pass

