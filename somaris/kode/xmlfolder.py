#!/usr/bin/python
import re
from xml.dom import minidom 
import os

path = "xml34/"
path2 = "protokoller34/"
listing = os.listdir(path)
for file in listing:
    try:
        f = open(path + file,'r')
        proto = minidom.parse(path + file).toxml()
        f.close()
    
        proto = proto.split("\n")[2:-4]
    
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
        fieldlist = ""
        first = True
        startmsg = ""
        pastIsotope = False
        bedDur = "two words"
        hisMode = "two words"
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
            elif item.startswith("Isotope"):
                pastIsotope = True
                item = item + "\n" + bedDur + "\n" + hisMode
            elif item.startswith("BedDuration"):
                bedDur = item
            elif item.startswith("HistogramMode"):
                hisMode = item
            fieldlist += item + "\n"
            
        
        
        fieldlist = "MlScanProtocolAttributes_Begin: 138\n" + fieldlist[:-1] + "\nMlModeRecon_End: 3\n\nMlScanProtocol_End: 138"
        f = open(path2 + file,'w')
        f.write(fieldlist)
        f.close()

    except:
        print file

