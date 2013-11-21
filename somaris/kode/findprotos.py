#!/usr/bin/python

import os
import re
import sys

#Finds protocol names for testing purposes.
path = "fprotokoller/"

protolength = 0
if len(sys.argv) > 1:
    try:
        protolength = int(sys.argv[1])
    except:
        print "Bad argument. Printing all protocols (That'll teach you)."

def loop(dir):
    listing = os.listdir(dir)
    for file in listing:
        f = open(dir + file,'r')
        proto = f.read()
        proto = proto.split("\n")
        p2 = []
        f.close

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
        reconnumber = []
        for i,item in enumerate(proto):
            """Creates a list of the modes the protocol contains"""
            if (item == "topo" or item == "pet" or item == "ct" or
                item == "pause"):
                protoorder.append(item)
                if item == "pause":
                    reconnumber.append(0)
            elif item.startswith("No_Of_Valid_Recons"):
                reconnumber.append(item[-1])
        if len(protoorder) == protolength or protolength == 0:
            print file
            print protoorder, reconnumber


loop(path)


