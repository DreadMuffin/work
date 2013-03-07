#!/usr/bin/python
import re
from xml.dom import minidom
import os

print "Converting xml to plaintext"

path31 = "xml3/"
path32 = "protokoller3/"
path41 = "xml4/"
path42 = "protokoller4/"
PETCTfields = [""] * 12

def hellsolver(helvedelist):
    """If a file contains the dreaded PetBedsInformation line instead of
    dividing the information into seperate lines, this will extract the info."""
    hellreturn = ""
    PETCTfields[4] = "BedDuration " + helvedelist[4].split(";")[1][:-3] + "(" + helvedelist[5].split(";")[1][:-3] + ")"
    if helvedelist[12].split(";")[1][:-3] == "PtSinogramData":
        PETCTfields[5] = ("RebinnerLut Null\n" + "RebinnerMode " +
                "PtOnlineHistogram\n")
    else: PETCTfields[5] = "RebinnerLut Null\n" + "RebinnerMode PtListMode32\n"
    PETCTfields[6] = "HistogramMode Pt" + helvedelist[11].split(";")[1][:-3]

def xmlloop(source,destination):
    """Loops over the files in the source directory and parses the xml to
    plaintext and saves it in the destination directory. Additionally it
    replaces some lines with a style that matches PET 5 and 6."""
    listing = os.listdir(source)
    for file in listing:
        try:
            proto = minidom.parse(source + file).toxml()
            proto = proto.split("\n")[2:-4]
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
                if "/" in item:
                    item = "/".join(item.split("/")[:-1])
                item = item.replace(">"," ")
                item = item.replace("&quot;","\"")
                item = item.lstrip(" ")[1:-1]
                if item.startswith("MlModeEntryType EntryNo="):
                    if len(item.split(" ")) == 5:
                        reconnumber.append(int(item[64]))
                    else:
                        reconnumber.append(int(item[84]))
                    if item[25] == "2":
                        startmsg = "MlModeRecon_End 138\n"
                    item = startmsg + "PROTOCOL_ENTRY_NO " + str(protonumber) + "\nMlModeScan_Begin 138"
                    protonumber+=1
                    ri +=1
                    first = True
                elif item.startswith("RangeName ReadOnly"):
                    item = " ".join(item.split(" ")[::3])
                elif item.startswith("MlPauseType"):
                    item = "MlModeRecon_End 138\nMlModeEntry_End 138\nPROTOCOL_ENTRY_NO " + str(protonumber) + "\nMlPause_Begin 138\nMlPause_End 138"
                    protonumber+=1
                elif item.startswith("Window ReadOnly"):
                    item = item.split(" ")
                    item = "Window[READ_ONLY] " + item[3]
                elif item.startswith("MlOtherModalityEntryType"):
                    reconnumber.append(int(item[93]))
                    item = startmsg + "PROTOCOL_ENTRY_NO " + str(protonumber) + "\nMlOtherModalityEntry_Begin 138"
                    protonumber+=1
                    ri +=1
                    PETstart = True
                    first = True
                elif item.startswith("MlModeReconType ReconJob") or item.startswith("MlOtherModalityModeReconType"):
                    if first:
                        item = "MlModeScan_End 138\nNo_Of_Valid_Recons " + str(reconnumber[ri-1]) + "\nMlModeRecon_Begin 138"
                        first = False
                    else: item = "MlModeRecon_End 138\nMlModeRecon_Begin 138"
                elif item.startswith("TableDirectionPatient") and PETstart:
                    PETstart = False
                    temp = ""
                    if bednum == False:
                        PETCTfields[9] = "NumberOfBeds Not given. Check recon range"
                    for field in PETCTfields:
                        temp += field + "\n"
                    item = temp + item
                elif PETstart:
                    if item.startswith("RangeName"):
                        item = item + "\nLLD n/a\nULD n/a"
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
                        PETCTfields[5] = "RebinnerLut Null\n" + item
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
                        hellsolver(proto[i].split("gt;&lt;"))
                        pass
                fieldlist += item + "\n"
            fieldlist = "MlScanProtocolAttributes_Begin 138\n" + fieldlist[:-1] + "\nMlModeRecon_End 3\nMlScanProtocol_End 138"
            f = open(destination + file,'w')
            f.write(fieldlist)
            f.close()

        except:
            print file + " did not compile properly"

xmlloop(path31,path32)
xmlloop(path41,path42)
