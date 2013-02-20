#!/usr/bin/python

import os

source = "fprotokoller34/"
dest = "fprotokoller/"

def get(index):
    """A dynamic list lookup"""
    return proto[index + gindex]

def outapp(numbers):
    list = []
    for num in numbers:
        list.append(get(num))
    return list

def topo():
    outorder = [0,1,2,9,3,8,4,5,6,10,11,7,12,13,14,15,16,17,18,19,20,21,22]
    return outapp(outorder)

def ct():
    recons = int(get(20).split(" ")[1])
    retlist = outapp([0,1,2,15,7,3,8,9,10,11,17,12,13,4,14,5,6,16,18,19,20])
    global gindex
    for i in range(0,recons):
        retlist.extend(outapp([21,35,23,24,25,26,27,28,29,30,22,31,33,34,32,36,
            37]))
        gindex += 17
    return retlist

def pause():
    outorder = [0,1,2,3]
    return outapp(outorder)

def pet():
    recons = int(get(20).split(" ")[1])
    retlist = outapp([0,1,2,3,4,5,6,10,15,8,9,7,17,11,18,12,13,14,16,19,20])
    global gindex
    for i in range(0,recons):
        retlist.extend(outapp([21,24,29,31,26,35,27,38,25,33,30,28,34,22,23,
            36,37,32,39]))
        gindex += 19
    return retlist


listing = os.listdir(source)
for file in listing:
    try:
        proto = open(source + file,"r").read().split("\n")
        gindex = 3
        protoorder = []
        for i,item in enumerate(proto):
            """Creates a list of the modes the protocol contains"""
            if item =="topo" or item =="pet" or item == "ct" or item == "pause":
                protoorder.append(item)
        fields = proto[:3]
        for mode in protoorder:
            if mode == "topo":
                fields += topo()
                gindex += 23
            elif mode == "ct":
                fields += ct()
                fields.append("MlModeEntry_End 138")
                gindex += 21
            elif mode == "pause":
                fields += pause()
                gindex += 4
            elif mode == "pet":
                fields += pet()
                gindex += 21
        fields.append("MlScanProtocol_End 138")
        f = open(dest + file,'w')
        f.write(("\n").join(fields))
        f.close
    except:
        print file + " nope"
