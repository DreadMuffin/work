#!/usr/bin/python
import re
from xml.dom import minidom 
import os

print "Converting xml to plaintext"

path = "xml34/"
path2 = "protokoller34/"
listing = os.listdir(path)

def hellsolver(helldex):
    """If a file contains the dreaded PetBedsInformation line instead of dividing 
    the information into seperate lines, this will extract the info."""
    hellreturn = ""
    helvedelist = proto[helldex].split("gt;&lt;")
    PETCTfields[4] = "BedDuration: " + helvedelist[4].split(";")[1][:-3] + "(" + helvedelist[5].split(";")[1][:-3] + ")"
    if helvedelist[12].split(";")[1][:-3] == "PtSinogramData":
        PETCTfields[5] = "RebinnerMode PtOnlineHistogram"
    else: PETCTfields[5] = "RebinnerMode PtListMode32\n"
    PETCTfields[6] = "HistogramMode: Pt" + helvedelist[11].split(";")[1][:-3]

for file in listing:
    """Loops over the files in the directory and parses the xml to plaintext.
    Additionally it replaces some lines with a style that matches PET 5 and 6."""
    try:
        f = open(path + file,'r')
        proto = minidom.parse(path + file).toxml()
        f.close()
    
        proto = proto.split("\n")[2:-4]
        PETCTfields = [""] * 12
    
        reconnumber = []
        ri = 0
        fieldlist = ""
        first = True
        startmsg = ""
        PETstart = False
        protonumber = 1
        bednum = False


        for i, item in enumerate(proto):
            item = item.replace("\t"," ")
            item = item.split("/")[0]
            item = item.replace(">"," ")
            item = item.replace("&quot;","\"")
            item = item.lstrip(" ")[1:-1]
            if item.startswith("MlModeEntryType EntryNo="):
                reconnumber.append(int(item[64]))
                if item[25] == "2":
                    startmsg = "MlModeRecon_End: 138\n"
                item = startmsg + "PROTOCOL_ENTRY_NO: " + str(protonumber) + "\nMlModeScan_Begin: 138"
                protonumber+=1
                ri +=1
                first = True
            elif item.startswith("MlPauseType"):
                item = "MlModeRecon_End: 138\nMlModeEntry_End: 138\nPROTOCOL_ENTRY_NO: " + str(protonumber) + "\nMlPause_Begin: 138\nMlPause_End: 138"
                protonumber+=1
            elif item.startswith("Window ReadOnly"):
                item = item.split(" ")
                item = "Window[READ_ONLY]: " + item[3]
            elif item.startswith("MlOtherModalityEntryType"):
                reconnumber.append(int(item[93]))
                item = startmsg + "PROTOCOL_ENTRY_NO: " + str(protonumber) + "\nMlOtherModalityEntry_Begin: 138"
                protonumber+=1
                ri +=1
                PETstart = True
                first = True
            elif item.startswith("MlModeReconType ReconJob") or item.startswith("MlOtherModalityModeReconType"):
                if first:
                    item = "MlModeScan_End: 138\nNo_Of_Valid_Recons: " + str(reconnumber[ri-1]) + "\nMlModeRecon_Begin: 138"
                    first = False
                else: item = "MlModeRecon_End: 138\nMlModeRecon_Begin: 138"
            elif item.startswith("TableDirectionPatient") and PETstart:
                PETstart = False
                temp = ""
                if bednum == False:
                    PETCTfields[9] = "NumberOfBeds Not given. Check recon range"
                for field in PETCTfields:
                    temp += field + "\n"
                item = temp + item
            elif PETstart:
                if item.startswith("InjectedDose"):
                    PETCTfields[0] = item
                    pass
                elif item.startswith("InjectionDate"):
                    PETCTfields[1] = item
                    pass
                elif item.startswith("InjectionTime"):
                    PETCTfields[2] = item
                    pass
                elif item.startswith("Isotope"):
                    PETCTfields[3] = item
                    pass
                elif item.startswith("BedDuration"):
                    PETCTfields[4] = item
                    pass
                elif item.startswith("RebinnerMode"):
                    PETCTfields[5] = item
                    pass
                elif item.startswith("HistogramMode"):
                    PETCTfields[6] = item
                    pass
                elif item.startswith("Pharmaceutical"):
                    PETCTfields[7] = item
                    pass
                elif item.startswith("PhysioInputType"):
                    PETCTfields[8] = item
                    pass
                elif item.startswith("NumberOfBeds"):
                    PETCTfields[9] = item
                    bednum = True
                    pass
                elif item.startswith("PetBedsInformation"):
                    hellsolver(i)
                    pass
            fieldlist += item + "\n"
          
        
        
        fieldlist = "MlScanProtocolAttributes_Begin: 138\n" + fieldlist[:-1] + "\nMlModeRecon_End: 3\n\nMlScanProtocol_End: 138"
        f = open(path2 + file,'w')
        f.write(fieldlist)
        f.close()

    except:
        print file

