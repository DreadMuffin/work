#!/usr/bin/python
import re
from xml.dom import minidom 

path = "PET4/"
f = open(path + "4_PET_CT_WB_FDG_terapi_uden_IV.Adult",'r')
proto = f.read()
f.close()

xmldoc = minidom.parse(path + "4_PET_CT_WB_FDG_terapi_uden_IV.Adult")
proto = xmldoc.toxml()

proto = proto.split("\n")[2:-4]
print len(proto)

foo = ""
for item in proto:
    item = item.replace("\t"," ")
    item = item.split("/")[0]
    item = item.replace(">"," ")
    item = item.lstrip(" ")[1:-1]
    foo += item + "\n"

foo = foo[:-1]
print foo

