#!/usr/bin/python

import os
import re

source = "fprotokoller/"
dest = "dprotokoller/"

"""Empties the destinationfolder, to avoid duplicates"""
if os.getcwd()[-13:] == "/somaris/kode":
    os.system("rm " + dest + "*")

listing = os.listdir(source)
globalindex = 0

def onoff(value):
    """Used to convert values to on or off"""
    if value == "1" or value == "true":
        return "On"
    else:
        return "Off"

def reconjob(value):
    """Returns which kind of job is being carried out."""
    if value == "MlAxialRJ":
        return "Axial"
    else:
        return "3D"

def get(index):
    """A dynamic list lookup"""
    return p2[index + gindex]

def reconrange(start,end):
    """Translates bedstart and bedend to a string"""
    if int(start) == int(end):
        return "Automatic/All/dunno"
    else: return start + " to " + end

def tubeposis(value):
    """Translates degrees to something readable."""
    if value == "270.0":
        return "Top"
    elif value == "90.0":
        return "Bottom"
    else: return "Lateral"

def apiid(value):
    """Checks whether an API is used"""
    if value == "-1":
        return "Null"
    else: return value


def topo56(nr):
    """Returns a list containing the data of a topogram"""
    topo = [name,scanner,str(nr),get(6),get(5), get(12)[:-4], get(10)[:-2],
            tubeposis(get(11))]
    topo.extend([get(8)[:-4], get(9)[2:],apiid(get(4)), get(17), get(21)])
    return topo

def ct56(nr):
    """Returns a list containing the data of a CT-phase"""
    crecons = int(get(20))
    croutine = [name,scanner,nr,crecons,get(13),get(11),get(18)[:-4],get(6)[2:],
            get(7)[2:],get(8),get(15),get(16),get(3),get(10)]
    cscan = [get(4),get(14),get(12),get(17)[2:]]
    croutine.extend(cscan)
    ct = []
    ct.append(croutine)
    i = 0
    crecon = []
    global gindex
    while i < crecons:
        crecon = [name,scanner,nr,str(i+1),get(34),get(22),get(29),get(36),onoff(get(26)),get(27),get(23),get(24),get(30)[8:],get(25)[9:],reconjob(get(33)),get(32)[2:],get(28)[5:],get(35),get(31)]
        i+=1
        ct.append(crecon)
        gindex +=17
    return ct

def pause56(nr):
    """Returns a list containing the fields of a pause"""
    return [name,scanner,nr]

def pet56(nr):
    """Returns a list containing the fields of a PET-phase"""
    injamount = get(11).split("(")[0]
    injunit = get(11).split("(")[1][2:-1]
    injdate = get(9)[6:] + "/" + get(9)[4:6] + " - " + get(9)[:4]
    injtime = get(10)[:2] + ":" + get(10)[2:4] + ":" + get(10)[4:6]
    scanoutput = ""
    if get(16) == "PtListMode32":
        scanoutput = "List mode"
    else: scanoutput = "Sinogram"

    scanrange = ""
    if int(get(32)) == 1:
        scanrange = "Match CT FOV"
    else: scanrange = "Do not match CT FOV"

    scanduration = get(13)[:-1].split("(")
    precons = int(get(20))
    pet = []

    petroutine = [name,scanner,nr,precons,get(4),get(7),get(8),injamount,injunit
            ,injdate,injtime,scanoutput,scanrange,get(12),scanduration[0],
            scanduration[1][2:]]
    petroutine.extend([onoff(get(3)),onoff(get(15)),scanoutput,get(17)[2:],
        get(18)[8:],get(5),get(6)])

    pet.append(petroutine)
    i = 0
    precon = []
    global gindex
    while i < precons:
        precon= [name,scanner,nr,str(i+1),get(33),reconrange(get(34),get(35)),
                get(23)[2:],get(24)[2:],get(27),get(26),get(25),get(28),
                get(31)[2:],get(29),get(36),get(37),onoff(get(22)[1:2]) + " (" +
                get(22)[3:4] + ")",onoff(get(30)),onoff(get(32)),onoff(get(36))]
        i+=1
        pet.append(precon)
        gindex +=19

    return pet

def topo34(nr):
    topo = [name,scanner,str(nr),get(4).split(" ")[2],get(7),get(12)[:-4],
            get(10)[:-2],tubeposis(get(11))]
    topo.extend([get(6)[:-4],get(9)[2:],apiid(get(3)),get(17)[1:-1],get(21)])
    return topo

def ct34(nr):
    crecons = int(get(20))
    ctroutine = [name,scanner,str(nr),crecons,get(4),get(11),get(18)[:-4],
            get(8)[2:],get(9)[2:],get(10),get(5),get(6),get(15),get(17)]
    ctroutine.extend([get(7),get(14),get(13),get(16)[2:]])

    i = 0
    ct = []
    ct.append(ctroutine)
    crecon = []
    global gindex
    while i < crecons:
        crecon = [name,scanner,nr,str(i + 1),get(34),get(35),get(29),get(36),
                onoff(get(26)),get(27),get(23),get(24),get(30)[8:],get(25)[9:],
                reconjob(get(33)),get(31)[2:],get(28)[5:],get(32),get(22)]
        i+=1
        ct.append(crecon)
        gindex +=17

    return ct

def pause34(nr):
    return [name,scanner,nr]


def pet34(nr):
    returnstring = ""
    global gindex

    scanoutput = ""

    if get(10) == "PtListMode32":
        scanoutput = "List mode"
    else: scanoutput = "Sinogram"

    scanrange = ""
    if get(25) == "true":
        scanrange = "Match CT FOV"
    else: scanrange = "Do not match CT FOV"

    scanduration = get(9)[:-1].split("(")
    precons = int(get(17))

    petroutine = [name,scanner,nr,precons,get(4),get(8),get(12),get(5),
            "Bequerels",get(6)[6:] + "/" + get(6)[4:6] + " - " + get(6)[:4],
            get(7)[:2] + ":" + get(7)[2:4] + ":" + get(7)[4:6],scanoutput,
            scanrange,"Null",scanduration[0],scanduration[1][2:]]
    petroutine.extend([onoff(get(3)),"Null",scanoutput,get(11)[2:],get(13)[8:],
        "Null","Null"])

    i = 0
    pet = []
    pet.append(petroutine)
    precon = []

    while i < precons:
        precon = [name,scanner,nr,str(i+1),get(31),reconrange(get(19),get(20)),
                get(26)[2:],get(28)[2:],get(24),get(32),get(23),get(35),
                get(27)[2:],get(22),get(33),get(34),onoff(get(21).split(",")[0])
                + " (" + get(21).split(",")[1] + ")",onoff(get(30)),
                onoff(get(25)),onoff(get(29))]
        i+=1
        pet.append(precon)
        gindex +=19

    return pet



for file in listing:
    globalindex+=3
    proto = open(source + file,'r').read().split("\n")
    p2 = []
    for item in proto:
        item = item.split(" ")[1:]
        p2.append(" ".join(item))

    pfoo = []
    for item in p2:
        item = item.replace("\"","")
        item = item.replace("#","\#")
        pfoo.append(re.sub("_"," ",item))

    p2 = pfoo


    protoorder = []

    for item in proto:
        """Creates a list of the modes the protocol contains"""
        if item == "topo" or item == "pet" or item == "ct" or item == "pause":
            protoorder.append(item)
    output = []
    protocol = []
    name = file[9:-5]
    scanner = file[-4:]
    bodysize = proto[1][-5:]
    protocol.append(name)
    protocol.append(scanner)
    protocol.append(bodysize)
    length = len(protoorder)
    protocol.append(str(length))
    protocol.append("NOW()")
    gindex = 3 #Global index used to indicate where the current phase starts

    if file[6:8] == "56":
        """Processes protocols from PET 5 and 6"""
        for i,item in enumerate(protoorder):
            if item == "topo":
                output.append(topo56(i+1))
                gindex+=23
            elif item == "pet":
                output.append(pet56(i+1))
                gindex+= 21
            elif item == "ct":
                output.append(ct56(i+1))
                gindex+=22
            elif item == "pause":
                output.append(pause56(i+1))
                gindex +=4
    else:
         """Processes protocols from PET 3 and 4"""
         for i,item in enumerate(protoorder):
            if item == "topo":
                output.append(topo34(i+1))
                gindex+=23
            elif item == "pet":
                output.append(pet34(i+1))
                gindex+= 18
            elif item == "ct":
                output.append(ct34(i+1))
                gindex+=21
            elif item == "pause":
                output.append(pause34(i+1))
                gindex +=4

    """Constructs a text file containing all the necessary SQL-statements to
    insert it into a database"""
    lines = "insert into Protocols values (\'" + "','".join(protocol) + "\');\n"
    lines = lines.replace("'NOW()'","NOW()")
    for i,item in enumerate(protoorder):
        if item == "topo":
            lines += ("insert into Topograms values (\'" + "','".join(output[i])
                    + "\');\n")
        elif item == "ct":
            lines += ("insert into CT values (\'" +
                    "','".join(map(str,output[i][0])) + "\');\n")
            for recon in output[i][1:]:
                lines += ("insert into CTrecon values (\'" +
                        "','".join(map(str,recon)) + "\');\n")
        elif item == "pause":
            lines += ("insert into Pause values (\'" +
                    "','".join(map(str,output[i])) + "\');\n")
        elif item == "pet":
            lines += ("insert into PET values (\'" +
            "','".join(map(str,output[i][0])) + "\');\n")
            for recon in output[i][1:]:
                lines += "insert into PETrecon values (\'" + "','".join(map(str,
                    recon)) + "\');\n"


    f = open(dest + file,'w')
    f.write(lines)
    f.close()




