#!/usr/bin/python

import re

template = file("template.tex","r").read()

proto = file("workingfields.MlAdult","r").read()
proto = proto.split("\n")
p2 = []
for item in proto:
    item = item.split(" ")[1:]
    p2.append(" ".join(item))

pfoo = []
for item in p2:
    pfoo.append(re.sub("_"," ",item))

p2 = pfoo

if p2[12] == "270.0":
    p2[12] = "Top"
elif p2[12] == "90.0":
    p2[12] = "Bottom"
else: p2[12] = "Lateral"



protonavn = p2[2]
size = p2[1]

Troutine = "\\begin{itemize}\\item mA: " + p2[7] + "\\item kV: " + p2[13][:-4] + "\\item Topogram length: " + p2[11][:-2] + " mm\\item Tube position: " + p2[12] 

Tscan = "\\item mA: " + p2[7] + "\\item kV: " + p2[13][:-4] + "\\item Delay: " + p2[9][:-4] + "s\\item Topogram length: " + p2[11][:-2] + " mm\\item Direction: " + p2[10][2:] + "\\item Tube position: " + p2[12] + "\\item API (-1 betyder None, ellers skal tallet oversaettes (stoerre arbejde): " + p2[6] + "\\item Kernel: " + p2[18][1:-1] + "\\item Window: " + p2[23][1:-1]

Croutine = "\\item Eff. mAs: " + p2[33] + "\\item kV: " + p2[38][:-4] + "\\item CARE Dose4D: " + p2[30][2:] + "\\item CTDlvol: " + p2[32] + "mGy\\item Scan time: " + p2[36] + " s\\item Delay: " + p2[39] + " s\\item Slice: " + p2[27] + " mm\\item No. of images: " + "Samme som i foerste recon, slet?(y/n)" + "\\item Tilt: " + p2[33] + " grader"

Cscan =  "\\item Quality ref. mAs: " + p2[28] + "\\item Eff. mAs: " + p2[33] + "\\item kV: " + p2[40][0:3] + "\\item Scan time: " + p2[38] + " s\\item Rotation time: " + p2[37] + " s\\item Delay: " + p2[39] + " s\\item Slice: " +  p2[5] + " mm\\item Pitch: " + p2[36] + "\\item Direction: " + p2[10][2:]



crecons = int(p2[42])
i = 0

def CF(index):
    return p2[index + i * 17]

Crecon = ""

while i < crecons:
    Crecon +="\n\\subsubsection{Recon " + str(i + 1) + "}" + "\n\\item Series description: " + CF(56)[1:-1] + "\n\\item Slice: " + CF(44) + "\n\\item Kernel: " + CF(51) + "\n\\item Window: " + CF(58) + "\n\\item Extended FoV(1/0): " + CF(48) + "\n\\item FoV: " + CF(49) + "\n\\item Center X: " + CF(45) + "\n\\item Center Y: " + CF(46) + "\n\\item Mirroring: " + CF(52)[8:] + "\n\\item Extended CT scale: " + CF(47)[9:] + "\n\\item Recon job: " + CF(55)[2:] + "\n\\item Recon Axis: " + CF(54)[2:] + "\n\\item Image order: " + CF(50)[5:] + "\n\\item Recon increment: " + CF(57) + "\n\\item No. of images: " + CF(53)
    i+=1

Proutine = ""

Pscan = ""

Precons = int(CF(82))

def PF(index):
    return p2[index+(Crecons-1)*17+(Precons-1)*17]

Precon = ""



output = template + "\\section{Topogram}\n\\subsection{Routine}\n "+Troutine+"\n\\subsection{Scan}\n"+ Tscan + "\n\\section{CT WB}\n\\subsection{Routine}\n" + Croutine + "\n\\subsection{Scan}\n" + Cscan + "\n\\subsection{Recon}\n" + Crecon + "\n\\section{Pause}\nLoL, I dunno" + "\n\\section{PET WB}\n\\subsection{Routine}\n" + Proutine + "\n\\subsection{Scan}\n" + Pscan + "\n\\subsection{Recon}\n" + Precon + "\\end{itemize}" + "\n\\end{document}"
print output

