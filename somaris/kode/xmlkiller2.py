from xml.dom import minidom 

path = "PET4/"
f = open(path + "4_PET_CT_WB_FDG_terapi_uden_IV.Adult",'r')
proto = f.read()

xmldoc = minidom.parse(path + "4_PET_CT_WB_FDG_terapi_uden_IV.Adult")

print xmldoc.toxml()
