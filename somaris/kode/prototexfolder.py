#!/usr/bin/python

import re
import os

template = open("template.tex","r").read()

path = "fprotokoller/"
path2 = "tprotokoller/"
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
        if CF(77) == "PtOnlineHistogram":
            scanoutput = "Sinogram"
        else: scanoutput = "List mode"

        scanrange = ""
        if int(CF(93)) == 1:
            scanrange = "Match CT FOV"
        else: scanrange = "Do not match CT FOV"

        injdose = CF(72)[:-1].split("(")
        scanduration = CF(74)[:-1].split("(")
        

        Proutine = "\\item Isotope: " + CF(68) + "\n\\item Pharm.: " + CF(69) + "\n\\item Inj. Dose: " + injdose[0] + " " + injdose[1][2:] + "\n\\item Inj. date (date/month - year): " + CF(70)[6:] + "/" + CF(70)[4:6] + " - " + CF(70)[:4] + "\n\\item Inj. time: " + CF(71)[:2] + ":" + CF(71)[2:4] + ":" + CF(71)[4:6] + "\n\\item Scan mode: " + scanoutput + "\n\\item Scan range: " + scanrange + "\n\\item No. of beds: " + CF(73) + "\n\\item Scan duration/bed: " + scanduration[0] + " " + scanduration[1][:-1]

        Pscan = "\\item Autoload: " + onoff(CF(65)) + "\n\\item Rebinner LUT: " + onoff(CF(76)) + "\n\\item Scan output: " + scanoutput + "\n\\item Sinogram mode: " + CF(78)[2:] + "\n\\item Input trigger signal: " + CF(79)[8:] + "\n\\item LLD (keV): " + CF(66) + "\n\\item ULD (keV): " + CF(67)


        Precons = int(CF(81))

        j = 0

        def PF(index):
            return p2[index + i * 17 + j * 17]

        Precon = ""

        while j < Precons:
            Precon +="\n\\subsubsection{Recon " + str(j + 1) + "}" + "\n\\item Series description: " + PF(94) + "\n\\item Recon range (bed): ups.." + "\n\\item Output image type: " + PF(84)[2:] + "\n\\item Recon method: " + PF(85)[2:] + "\n\\item Iterations: " + PF(88) + "\n\\item Subsets: " + PF(87) + "\n\\item Image size: " + PF(86) + "\n\\item Zoom: " + PF(89) + "\n\\item Filter: " + PF(92)[2:] + "\n\\item FWHM (mm): " + PF(90) + "\n\\item Offset X: " + PF(95) + " mm" + "\n\\item Offset Y: " + PF(96) + " mm" + "\n\\item Attenuation correction: " + onoff(PF(83)[1:2]) + " (" + PF(83)[3:4] + ")" + "\n\\item Scatter correction: " + onoff(PF(91)) + "\n\\item Match CT slice location: " + onoff(PF(93)) + "\n\\item Save intermediate data: " + onoff(PF(97))
            j+=1
        j-=1


        output = page + "\\section{Topogram}\n\\subsection{Routine}\n "+Troutine+"\n\\subsection{Scan}\n"+ Tscan + "\n\\section{CT WB}\n\\subsection{Routine}\n" + Croutine + "\n\\subsection{Scan}\n" + Cscan + "\n\\subsection{Recon}\n" + Crecon + "\n\\section{Pause}\n" + Pause + "\n\\section{PET WB}\n\\subsection{Routine}\n" + Proutine + "\n\\subsection{Scan}\n" + Pscan + "\n\\subsection{Recon}\n" + Precon + "\n\\end{itemize}" + "\n\\end{document}"

        savename = file[7:]
        f = open(path2 + savename + ".tex",'w')
        f.write(output)
        f.close()
    except:
        print file


