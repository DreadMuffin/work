#!/usr/bin/python

import re
import os

print "Extracting data"

FIELDS = "scanfields56"

f = open(FIELDS,'r')
tfields = f.read()
tfields = tfields.split("newmode:")

start = tfields[0].split("\n")[:-1]
topogram = tfields[1].split("\n")[1:-1]
ct = tfields[2].split("\n")[1:-1]
pause = tfields[3].split("\n")[1:-1]
pet = tfields[4].split("\n")[1:-1]


path5 = "protokoller5/"
path6 = "protokoller6/"
destpath = "fprotokoller/"

def listappend(list,input):
    """Concatenates lists"""
    for item in input:
        list.append(item)

def loop(source,mname):
    """Extracts data from all the files and writes it into a new seperate
    files."""
    listing = os.listdir(source)
    for file in listing:
        try:
            f = open(source + file,'r').read()
            proto = f.split("\n")
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
                """Creates a fieldlist which fits the file"""
                if searching:
                    if item.startswith("MlPause_Begin"):
                        searching = False
                        listappend(fields,pause)
                        protoorder.append("pause")
                    elif item.startswith("MlOtherModalityEntry_Begin"):
                        searching = False
                        listappend(fields,pet)
                        protoorder.append("pet")
                    elif item.startswith("MlModeEntry_Begin:"):
                        searchingtc = True
                        searching = False
                elif searchingtc:
                    if item == "RangeName[READ_ONLY]: \"Topogram\"":
                        protoorder.append("topo")
                        listappend(fields,topogram)
                        searchingtc = False
                    elif item.startswith("RangeName"):
                        protoorder.append("ct")
                        listappend(fields,ct)
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
            reconpos = [i for i, x in enumerate(fields) if x ==
                    "No_Of_Valid_Recons"]
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
                    findex+=1
                    fieldlist+=item + "\n"
            fieldlist = fieldlist[:-1]
            f = open(destpath + "fields56_" + file + mname,'w')
            f.write(fieldlist)
            f.close()

        except:
            print file
loop(path5,"_PET5")
loop(path6,"_PET6")
