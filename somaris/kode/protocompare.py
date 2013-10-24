#!/usr/bin/python

#fields34_4_DOHAN_Terapi_PET_CT_FDG_nr1.Adult_PET4
#fields56_HUND_FDG.MlAdult_PET5
import os
import sys
import re

if len(sys.argv) < 3:
    print "Please supply two protocols"
    sys.exit()

path = "fprotokoller/"
if "/" not in sys.argv[1]:
    sys.argv[1] = path + sys.argv[1]
file1 = open(sys.argv[1],'r')
if "/" not in sys.argv[2]:
    sys.argv[2] = path + sys.argv[2]
file2 = open(sys.argv[2],'r')
one = file1.read().split("\n")
two = file2.read().split("\n")
file1.close()
file2.close()
p1 = []
p2 = []
for item in one:
    item = item.split(" ")[1:]
    p1.append(" ".join(item).rstrip())

for item in two:
    item = item.split(" ")[1: ]
    p2.append(" ".join(item).rstrip())

#os.system("diff -y -w -i " + path + sys.argv[1] + " " +
#        path + sys.argv[2] + " > comparetemp.txt")

def compare(index):
    return p1[index] == p2[index]

def compare2(index,factor):
    return p1[index] == p2[index + factor]

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

def neworder(order1,order2):
    returnorder = [0] * (len(order1) * 2)
    for i,item in enumerate(order1):
        returnorder[i] = min(order1[i], order2[i])
        if order1[i] != order2[i]:
            returnorder[i + len(order1)] = int(order2[i]) - int(order1[i])
    return returnorder

def factorlist(modes,recons):
    flist = [0]
    for i,item in enumerate(modes):
        if item == "topo":
            flist.append(flist[i])
        elif item == "pause":
            flist.append(flist[i])
        elif item == "ct":
            flist.append(17 * recons[i + len(modes)] + flist[i])
        elif item == "pet":
            flist.append(19 * recons[i + len(modes)] + flist[i])
    return flist


def main():
    order1 = protoorderplus(one)
    order2 = protoorderplus(two)
    returnlist = ""
    ignorelist = ["ProtocolName","InjectionDate","InjectionTime","Transfer"]
    modes = ["topo","pet","ct","pause"]
    reconnumber = 0
    printedr = False
    printedm = False
    mode = "Start"

    if order1 == order2:
        for i,item in enumerate(one):
            if filter(item.startswith,ignorelist):
                continue
            elif item.startswith("MlModeRecon_Begin"):
                reconnumber+=1
                printedr = False
            elif filter(item.startswith,modes):
                mode = item
                reconnumber = 0
                printedr = False
                printedm = False
            elif not compare(i):
                if not printedm:
                    returnlist += mode + "\n"
                    printedm = True
                if reconnumber != 0 and not printedr:
                    returnlist += "Recon number: "+str(reconnumber)+"\n"
                    printedr = True
                returnlist += (one[i] + "   |   " + p2[i] + "\n")

        if returnlist != "":
            returnlist = ("Differences between the two protocols:\n" +
                    "Protocol one | Protocol two\n" + returnlist)
            print order1[0]
            print returnlist[:-1]
        else:
            print "The two protocols are identical"

    elif order1[0] == order2[0]:
        skip = False
        orderi = 0
        order = neworder(order1[1],order2[1])
        factor = factorlist(order1[0],order)
        max = len(two)
        print order
        print factor
        for i,item in enumerate(one):
            if filter(item.startswith,ignorelist):
                continue
            elif i == max:
                break
            elif item.startswith("MlModeRecon_Begin") and not skip:
                reconnumber += 1
                printedr = False
                if reconnumber >= int(order[orderi]):
                    skip = True
            elif filter(item.startswith,modes):
                skip = False
                mode = item
                reconnumber = 0
                if mode != "topo":
                    orderi += 1
                printedm = False
            elif skip:
                continue
            elif not compare2(i,factor[orderi]):
                if not printedm:
                    returnlist += mode + "\n"
                    printedm = True
                if reconnumber != 0 and not printedr:
                    returnlist += "Recon number: "+str(reconnumber)+"\n"
                    printedr = True
                returnlist += (one[i] + "   |   " + p2[i + factor[orderi]]
                        + "\n")
        if returnlist != "":
            returnlist = ("The protocols does not have the same amount of " +
                    "recons\n" +
                    "Mode order: " + str(order1[0]) + "\n" +
                    "Recons protocol 1: " + str(order1[1]) + "\n" +
                    "Recons protocol 2: " + str(order2[1]) + "\n" +
                    "Other differences between the two protocols:\n" +
                    "Protocol one | Protocol two\n") + returnlist
            print returnlist[:-1]
        else:
            print ("The two protocols does not have the same amount of recons,"+
            " but the contents of the recons in similar position are identical"+
            " and so is the remaining content.")
            print order1[1], order2[1]


#        print ("The protocols are of the same form but have different amounts" +
#        " of recons")
 #       print order1[0]
  #      print "Protocol 1 recon amounts: "
   #     print order1[1]
    #    print "Protocol 2 recon amounts: "
     #   print order2[1]
    else:
        print "The protocols are not comparable"
        print order1[0]
        print order2[0]

main()
