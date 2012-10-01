#!/usr/bin/python
import re
from xml.dom import minidom 

path = "PET4/"
f = open(path + "4_PET_CT_WB_FDG_terapi_uden_IV.Adult",'r')
proto = f.read()
f.close()

xmldoc = minidom.parse(path + "4_PET_CT_WB_FDG_terapi_uden_IV.Adult")
proto = xmldoc.toxml()

proto = proto.split("\n")[2:-4]
#print len(proto)

goo = ""

for item in proto:
    goo += item + "\n"

f = open("goo.txt",'w')
f.write(goo)
f.close()


foo = ""
for item in proto:
    item = item.replace("\t"," ")
    item = item.split("/")[0]
    item = item.replace(">"," ")
    item = item.lstrip(" ")[1:-1]
    foo += item + "\n"
    if item.startswith("MlModeEntryType EntryNo="):
        item = "PROTOCOL_ENTRY_NO: " + item[25] + "\nMlModeRecon_Begin: 138"


foo = "MlScanProtocolAttributes_Begin: 138\n" + foo[:-1] + "\nMlScanProtocol_End: 138"


reconnumber = [0,0,0]
ri = -1


for item in foo.split("\n"):
    if item.startswith("MlModeReconType ReconJob"):
        if int(item[26]) == 1:
            ri += 1
            reconnumber[ri] += 1
        elif int(item[26]) > 1:
            reconnumber[ri] += 1

print reconnumber




 #   if item.startswith("MlModeReconType ReconJob="1"):
   #     item = "MlModeScan_End: 138\nNo_Of_Valid_Recons: 1\nMlModeRecon_Begin: 138"







#for i in proto:
#    print i + "\n"
print foo
