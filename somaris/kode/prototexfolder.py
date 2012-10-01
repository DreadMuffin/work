#!/usr/bin/python

import re
import os

template = open("template.tex","r").read()

path = "fprotokoller/"
path2 = "tprotokoller/"
path3 = "fejlkorsler/"
listing = os.listdir(path)

def onoff(oneorzero):
    if int(oneorzero) == 1:
        return "On"
    else:
        return "Off"


for file in listing:

    try:
    
        f = open(path + file,'r')
        proto = f.read()
        proto = proto.split("\n")
        p2 = []

        title = file[7:]
        title = re.sub("_","\_",title)

        page = template % {"title" : title}

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

        apiid = ""
        if int(p2[6]) == -1:
            apiid = "None"
        else: apiid = "API " + p2[6] 

        Tscan = "\\item mA: " + p2[7] + "\\item kV: " + p2[13][:-4] + "\\item Delay: " + p2[9][:-4] + "s\\item Topogram length: " + p2[11][:-2] + " mm\\item Direction: " + p2[10][2:] + "\\item Tube position: " + p2[12] + "\\item API: " + apiid + "\\item Kernel: " + p2[18][1:-1] + "\\item Window: " + p2[23][1:-1]

        Croutine = "\\item Eff. mAs: " + p2[33] + "\\item kV: " + p2[38][:-4] + "\\item CARE Dose4D: " + p2[30][2:] + "\\item CTDlvol: " + p2[32] + "mGy\\item Scan time: " + p2[36] + " s\\item Delay: " + p2[39] + " s\\item Slice: " + p2[27] + " mm\\item No. of images: " + "Samme som i foerste recon, slet?(y/n)" + "\\item Tilt: " + p2[33] + " grader"

        Cscan =  "\\item Quality ref. mAs: " + p2[28] + "\\item Eff. mAs: " + p2[33] + "\\item kV: " + p2[40][0:3] + "\\item Scan time: " + p2[38] + " s\\item Rotation time: " + p2[37] + " s\\item Delay: " + p2[39] + " s\\item Slice: " +  p2[5] + " mm\\item Pitch: " + p2[36] + "\\item Direction: " + p2[10][2:]

        Crecons = int(p2[42])
        i = 0

        def CF(index):
            return p2[index + i * 17]

        def reconjob(index):
            if CF(index) == "MlAxialRJ":
                return "Axial"
            else:
                return "3D"

        Crecon = ""

        while i < Crecons:
            Crecon +="\n\\subsubsection{Recon " + str(i + 1) + "}" + "\n\\item Series description: " + CF(56)[1:-1] + "\n\\item Slice: " + CF(44) + "\n\\item Kernel: " + CF(51) + "\n\\item Window: " + CF(58) + "\n\\item Extended FoV: " + onoff(CF(48)) + "\n\\item FoV: " + CF(49) + "\n\\item Center X: " + CF(45) + "\n\\item Center Y: " + CF(46) + "\n\\item Mirroring: " + CF(52)[8:] + "\n\\item Extended CT scale: " + CF(47)[9:] + "\n\\item Recon job: " + reconjob(55) + "\n\\item Recon Axis: " + CF(54)[2:] + "\n\\item Image order: " + CF(50)[5:] + "\n\\item Recon increment: " + CF(57) + "\n\\item No. of images: " + CF(53)
            i+=1

        i-=1

        Pause = ""

        scanoutput = ""
        if CF(78) == "PtOnlineHistogram":
            scanoutput = "Sinogram"
        else: scanoutput = "List mode"

        scanrange = ""
        if int(CF(94)) == 1:
            scanrange = "Match CT FOV"
        else: scanrange = "Do not match CT FOV"

        injdose = CF(73)[:-1].split("(")
        scanduration = CF(75)[:-1].split("(")
        

        Proutine = "\\item Isotope: " + CF(69) + "\n\\item Pharm.: " + CF(70) + "\n\\item Inj. Dose: " + injdose[0] + " " + injdose[1][2:] + "\n\\item Inj. date (date/month - year): " + CF(71)[6:] + "/" + CF(71)[4:6] + " - " + CF(71)[:4] + "\n\\item Inj. time: " + CF(72)[:2] + ":" + CF(72)[2:4] + ":" + CF(72)[4:6] + "\n\\item Scan mode: " + scanoutput + "\n\\item Scan range: " + scanrange + "\n\\item No. of beds: " + CF(74) + "\n\\item Scan duration/bed: " + scanduration[0] + " " + scanduration[1][:-1]

        Pscan = "\\item Autoload: " + onoff(CF(66)) + "\n\\item Rebinner LUT: " + onoff(CF(77)) + "\n\\item Scan output: " + scanoutput + "\n\\item Sinogram mode: " + CF(79)[2:] + "\n\\item Input trigger signal: " + CF(80)[8:] + "\n\\item LLD (keV): " + CF(67) + "\n\\item ULD (keV): " + CF(68)


        Precons = int(CF(82))

        j = 0

        def PF(index):
            return p2[index + i * 17 + j * 17]

        Precon = ""

        while j < Precons:
            Precon +="\n\\subsubsection{Recon " + str(j + 1) + "}" + "\n\\item Series description: " + PF(95) + "\n\\item Recon range (bed): ups.." + "\n\\item Output image type: " + PF(85)[2:] + "\n\\item Recon method: " + PF(86)[2:] + "\n\\item Iterations: " + PF(89) + "\n\\item Subsets: " + PF(88) + "\n\\item Image size: " + PF(87) + "\n\\item Zoom: " + PF(90) + "\n\\item Filter: " + PF(93)[2:] + "\n\\item FWHM (mm): " + PF(91) + "\n\\item Offset X: " + PF(96) + " mm" + "\n\\item Offset Y: " + PF(97) + " mm" + "\n\\item Attenuation correction: " + onoff(PF(84)[1:2]) + " (" + PF(84)[3:4] + ")" + "\n\\item Scatter correction: " + onoff(PF(92)) + "\n\\item Match CT slice location: " + onoff(PF(94)) + "\n\\item Save intermediate data: " + onoff(PF(98))
            j+=1
        j-=1


        output = page + "\\section{Topogram}\n\\subsection{Routine}\n "+Troutine+"\n\\subsection{Scan}\n"+ Tscan + "\n\\section{CT WB}\n\\subsection{Routine}\n" + Croutine + "\n\\subsection{Scan}\n" + Cscan + "\n\\subsection{Recon}\n" + Crecon + "\n\\section{Pause}\n" + Pause + "\n\\section{PET WB}\n\\subsection{Routine}\n" + Proutine + "\n\\subsection{Scan}\n" + Pscan + "\n\\subsection{Recon}\n" + Precon + "\n\\end{itemize}" + "\n\\end{document}"

        savename = file[7:]
        f = open(path2 + savename + ".tex",'w')
        f.write(output)
        f.close()
    except:
        fejlnavn = file[7:]
        f = open(path3 + fejlnavn,'w')
        f.write("fejl fejl fejl")
        f.close()


