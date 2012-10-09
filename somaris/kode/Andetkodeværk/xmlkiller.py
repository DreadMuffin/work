#!/usr/bin/python
import re
from xml.dom import minidom 

path = "xml34/"

xmldoc = minidom.parse(path + "4_PET_CT_WB_FDG_terapi_uden_IV.Adult")
proto = xmldoc.toxml()

proto = proto.split("\n")[2:-4]
#print len(proto)

def hellsolver(helldex):
    hellreturn = ""
    helvedelist = proto[helldex].split("gt;&lt;")
    hellreturn = "BedDuration: " + helvedelist[4].split(";")[1][:-3] + "(" + helvedelist[5].split(";")[1][:-3] + ")\n"
    if helvedelist[12].split(";")[1][:-3] == "PtSinogramData":
        hellreturn += "RebinnerMode PtOnlineHistogram\n"
    else: hellreturn += "RebinnerMode PtListMode32\n"
    hellreturn += "HistogramMode: Pt" + helvedelist[11].split(";")[1][:-3]
    return hellreturn

reconnumber = [0,0,0]
ri = 0
foo = ""
first = True
startmsg = ""
for i, item in enumerate(proto):
    item = item.replace("\t"," ")
    item = item.split("/")[0]
    item = item.replace(">"," ")
    item = item.replace("&quot;","\"")
    item = item.lstrip(" ")[1:-1]
    if item.startswith("MlModeEntryType EntryNo="):
        reconnumber[ri] = int(item[64])
        if item[25] == "2":
            startmsg = "MlModeRecon_End: 138\n"
        item = startmsg + "PROTOCOL_ENTRY_NO: " + item[25] + "\nMlModeScan_Begin: 138"
        ri +=1
        first = True
    elif item.startswith("MlPauseType"):
        item = "MlModeRecon_End: 138\nMlModeEntry_End: 138\nPROTOCOL_ENTRY_NO: 3\nMlPause_Begin: 138\nMlPause_End: 138"
    elif item.startswith("Window ReadOnly"):
        item = item.split(" ")
        item = "Window[READ_ONLY]: " + item[3]
    elif item.startswith("MlOtherModalityEntryType"):
        reconnumber[ri] = int(item[93])
        item = startmsg + "PROTOCOL_ENTRY_NO: 4\nMlModeScan_Begin: 138"
        ri +=1
        first = True
    elif item.startswith("MlModeReconType ReconJob") or item.startswith("MlOtherModalityModeReconType"):
        if first:
            item = "MlModeScan_End: 138\nNo_Of_Valid_Recons: " + str(reconnumber[ri-1]) + "\nMlModeRecon_Begin: 138"
            first = False
        else: item = "MlModeRecon_End: 138\nMlModeRecon_Begin: 138"
    elif item.startswith("PetBedsInformation"):
        item = hellsolver(i)
    foo += item + "\n"
    


foo = "MlScanProtocolAttributes_Begin: 138\n" + foo[:-1] + "\nMlModeRecon_End: 3\n\nMlScanProtocol_End: 138"

print foo
