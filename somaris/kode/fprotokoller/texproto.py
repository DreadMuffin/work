#!/usr/bin/python

template = file("template.tex","r").read()

proto = file("fields_WB_FDG_PET_CT_5.MlAdult","r").read()
proto = proto.split("\n")
p2 = []
for item in proto:
    item = item.split(" ")[1:]
    p2.append(" ".join(item))

if p2[12] == "270.0":
    p2[12] = "Top"
elif p2[12] == "90.0":
    p2[12] = "Bottom"
else: p2[12] = "Lateral"



protonavn = p2[2]
size = p2[1]

Troutine = "mA: " + p2[7] + "\nkV: " + p2[13][:-4] + "\nSlice: " + p2[5] + " mm\nTopogram length: " + p2[11][:-2] + " mm\nTube position: (Bottom og Lateral skal maaske byttes) " + p2[12]

Tscan = "mA: " + p2[7] + "\nkV: " + p2[13][:-4] + "\nDelay: " + p2[9][:-4] + "\nSlice: " + p2[5] + " mm\nTopogram length: " + p2[11][:-2] + " mm\nDirection: " + p2[10][2:] + "\nTube position: (Bottom og Lateral skal maaske byttes) " + p2[12] + "\nAPI (-1 betyder None): " + p2[6] + "\nKernel: " + p2[18] + "\nWindow: " + p2[23]

Croutine = "kV: " + p2[38][:-4] + "\nScan time: " + p2[36] + " s\nDelay: " + p2[37] + " s\nSlice: " + p2[27] + " mm\nNo. of images: " + ""

Pause = ""
PET = ""

print Croutine












#output = template + "\\section{Topogram}\n\\subsection{Routine}\nJeg ved en laerkerede\n\\section{CT scan}\nadada" + "\\end{document}"
#print output

