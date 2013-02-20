#!/usr/bin/python

import re
import os

print "Extracting data"

FIELDS = "scanfields34"

f = open(FIELDS, 'r')
tfields = f.read()
tfields = tfields.split("newmode:")

start = tfields[0].split("\n")[:-1]
topogram = tfields[1].split("\n")[1:-1]
ct = tfields[2].split("\n")[1:-1]
pause = tfields[3].split("\n")[1:-1]
pet = tfields[4].split("\n")[1:-1]


path3 = "protokoller3/"
path4 = "protokoller4/"
destpath = "fprotokoller34/"

boollist = ["ExtendedFOV","AutoLoad","RebinnerL","ScatterCorrect",
            "SaveIntermediateData","MatchCTSliceLocation"]

def onoff(value):
    """Used to convert values to 1 or 0"""
    if value == "true":
        return "1"
    else:
        return "0"

def loop(source,mname):
    listing = os.listdir(source)
    """Extracts data from all the files and writes it into a new seperate
    listing = os.listdir(source) file"""
    for file in listing:
        try:
            f = open(source + file, 'r')
            proto = f.read().split("\n")
            f.close()
            newProto = []
            for item in proto:
                item = item.rstrip('\r\n:')
                item = item.replace("\t", " ")
                item = re.sub(' +', ' ', item)
                if item.startswith("CurrentRatio"):
                    continue
                newProto.append(item)
            proto = newProto

            searching = False
            searchingtc = False
            fields = []
            fields.extend(start)
            protoorder = []
            for i, item in enumerate(proto):
                """Creates a fieldlist which fits the file"""
                if searching:
                    if item.startswith("MlPause_Begin"):
                        searching = False
                        fields.extend(pause)
                        protoorder.append("pause")
                    elif item.startswith("MlOtherModalityEntry_Begin"):
                        searching = False
                        fields.extend(pet)
                        protoorder.append("pet")
                    elif item.startswith("MlModeScan_Begin"):
                        searchingtc = True
                        searching = False
                elif searchingtc:
                    if (item.startswith("RangeName") and
                            item.endswith("\"Topogram\"")):
                        protoorder.append("topo")
                        fields.extend(topogram)
                        searchingtc = False
                    elif item.startswith("RangeName"):
                        protoorder.append("ct")
                        fields.extend(ct)
                        searchingtc = False
                elif item.startswith("PROTOCOL_ENTRY_NO"):
                    searching = True

            fields.append("MlScanProtocol_End")
            fields.append("Det her slutter den ikke med")
            findex = 0
            rindex = -1
            recon = [0] * (len(protoorder) - protoorder.count("p"))
            protonr = 0
            fieldlist = ""
            reconpos = [i for i, x in enumerate(fields) if x == "No_Of_Valid_Recons"]
            bednumbercounter = 0
            for i,item in enumerate(proto):
                """Copies all the valid fields into the output list"""
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
                    elif filter(item.startswith,boollist):
                         item = (item.split(" ")[0] + " " +
                                 onoff(item.split(" ")[1]))
                    findex+=1
                    fieldlist+=item + "\n"
            fieldlist = fieldlist[:-1]
            f = open(destpath + "fields34_" + file + mname,'w')
            f.write(fieldlist)
            f.close()

        except:
            print file

loop(path3,"_PET3")
loop(path4,"_PET4")
