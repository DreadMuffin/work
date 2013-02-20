#!/usr/bin/python

#fields34_4_DOHAN_Terapi_PET_CT_FDG_nr1.Adult_PET4
#fields56_HUND_FDG.MlAdult_PET5
import os
import sys
import re

path = "fprotokoller/"
file1 = open(path + sys.argv[1],'r')
file2 = open(path + sys.argv[2],'r')
one = file1.read().split("\n")
two = file2.read().split("\n")
file1.close()
file2.close()

#os.system("diff -y -w -i " + path + sys.argv[1] + " " +
#        path + sys.argv[2] + " > comparetemp.txt")

sameorder = False
samerecons = False

def get(index):
    return

def protoorderplus(file):
    protoorder = []
    recons = []
    for i,item in enumerate(file):
        """Creates a list of the modes the protocol contains"""
        if item == "topo" or item == "pet" or item == "ct":
            protoorder.append(item)
        elif item == "pause":
            protoorder.append(item)
            recons.append(0)
        elif item.startswith("No_Of_Valid_Recons"):
            recons.append(item.split(" ")[1])
    return [protoorder,recons]

def topo():
    return []


def main():
    order1 = protoorderplus(one)
    order2 = protoorderplus(two)

    if order1 = order2:
        p1 = []
        p2 = []
        print "lala"
        for item in one:
            item = item.split(" ")[1:]
            p1.append(" ".join(item))

        for item in two:
            item = item.split(" ")[1: ]
            p2.append(" ".join(item))

        start = initial()
        for item,i in enummerate(order1):
            if item == "topo":
                topo()
            elif item == "ct":
                ct()
            elif item == "pause":
                pause()
            elif item == "pet":
                pet()

    elif sameorder:
        print "The protocols are of the same form but do not share their number"
        + "of recons"
        print order1[0]
        print "Recons 1: " + order1[1]
        print "Recons 2: " + order2[1]
    else:
        print "The protocols are not comparable"
        print order1[0]
        print order2[0]

main()



