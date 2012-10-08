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

def reconjob(index):
    if CF(index) == "MlAxialRJ":
        return "Axial"
    else:
        return "3D"


for file in listing:

#    try:
        print file
    
        f = open(path + file,'r')
        proto = f.read()
        proto = proto.split("\n")
        p2 = []

        f.close

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



        if file[6:8] != "34":
            protonavn = p2[2]
            size = p2[1]
            
            if p2[12] == "270.0":
                p2[12] = "Top"
            elif p2[12] == "90.0":
                p2[12] = "Bottom"
            else: p2[12] = "Lateral"

            Troutine = "\\begin{itemize}\\item mA: " + p2[7] + "\\item kV: " + p2[13][:-4] + "\\item Topogram length: " + p2[11][:-2] + " mm\\item Tube position: " + p2[12] 

            apiid = ""
            if int(p2[6]) == -1:
                apiid = "None"
            else: apiid = "API " + p2[6] 

            Tscan = "\\item mA: " + p2[7] + "\\item kV: " + p2[13][:-4] + "\\item Delay: " + p2[9][:-4] + "s\\item Topogram length: " + p2[11][:-2] + " mm\\item Direction: " + p2[10][2:] + "\\item Tube position: " + p2[12] + "\\item API: " + apiid + "\\item Kernel: " + p2[18][1:-1] + "\\item Window: " + p2[22][1:-1]

            Croutine = "\\item Eff. mAs: " + p2[32] + "\\item kV: " + p2[37][:-4] + "\\item CARE Dose4D: " + p2[29][2:] + "\\item CTDlvol: " + p2[31] + "mGy\\item Scan time: " + p2[35] + " s\\item Delay: " + p2[38] + " s\\item Slice: " + p2[26] + " mm\\item No. of images: " + "Samme som i foerste recon, slet?(y/n)" + "\\item Tilt: " + p2[32] + " grader"

            Cscan =  "\\item Quality ref. mAs: " + p2[27] + "\\item Eff. mAs: " + p2[32] + "\\item kV: " + p2[39][0:3] + "\\item Scan time: " + p2[37] + " s\\item Rotation time: " + p2[36] + " s\\item Delay: " + p2[38] + " s\\item Slice: " +  p2[5] + " mm\\item Pitch: " + p2[35] + "\\item Direction: " + p2[10][2:]

            Crecons = int(p2[41])
            i = 0

            def CF(index):
                return p2[index + i * 17]

            Crecon = ""

            while i < Crecons:
                Crecon +="\n\\subsubsection{Recon " + str(i + 1) + "}" + "\n\\item Series description: " + CF(55)[1:-1] + "\n\\item Slice: " + CF(43) + "\n\\item Kernel: " + CF(50) + "\n\\item Window: " + CF(57) + "\n\\item Extended FoV: " + onoff(CF(47)) + "\n\\item FoV: " + CF(48) + "\n\\item Center X: " + CF(44) + "\n\\item Center Y: " + CF(45) + "\n\\item Mirroring: " + CF(51)[8:] + "\n\\item Extended CT scale: " + CF(46)[9:] + "\n\\item Recon job: " + reconjob(54) + "\n\\item Recon Axis: " + CF(53)[2:] + "\n\\item Image order: " + CF(49)[5:] + "\n\\item Recon increment: " + CF(56) + "\n\\item No. of images: " + CF(52)
                i+=1

            i-=1

            Pause = ""

            scanoutput = ""
            if CF(77) == "PtListMode32":
                scanoutput = "List mode"
            else: scanoutput = "Sinogram"

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

        else:
            protonavn = p2[2]
            size = p2[1]

            if p2[12] == "270.0":
                p2[12] = "Top"
            elif p2[12] == "90.0":
                p2[12] = "Bottom"
            else: p2[12] = "Lateral"


            Troutine = "\\begin{itemize}\\item mA: " + p2[8] + "\\item kV: " + p2[13][:-4] + "\\item Topogram length: " + p2[11][:-2] + " mm\\item Tube position: " + p2[12]  

            Tscan = "\\item mA: " + p2[8] + "\\item kV: " + p2[13][:-4] + "\\item Delay: " + p2[7][:-4] + "s\\item Topogram length: " + p2[11][:-2] + " mm\\item Direction: " + p2[10][2:] + "\\item Tube position: " + p2[12] + "\\item API: " + p2[5] + "\\item Kernel: " + p2[18][1:-1] + "\\item Window: " + p2[22][1:-1]

            Croutine = "\\item Eff. mAs: " + p2[33] + "\\item kV: " + p2[39][:-4] + "\\item CARE Dose4D: " + p2[30][2:] + "\\item CTDlvol: " + p2[32] + "mGy\\item Scan time: " + p2[27] + " s\\item Delay: " + p2[28] + " s\\item Slice: " + p2[37] + " mm\\item No. of images: " + "Samme som i foerste recon, slet?(y/n)" + "\\item Tilt: " + p2[38] + " grader"

            Cscan =  "\\item Quality ref. mAs: " + p2[29] + "\\item Eff. mAs: " + p2[33] + "\\item kV: " + p2[39][:-4] + "\\item Scan time: " + p2[27] + " s\\item Rotation time: " + p2[36] + " s\\item Delay: " + p2[28] + " s\\item Slice: " +  p2[37] + " mm\\item Pitch: " + p2[35] + "\\item Direction: " + p2[10][2:]

            Crecons = int(p2[41])
            i = 0

            def CF(index):
                return p2[index + i * 17]

            Crecon = ""

            while i < Crecons:
                Crecon +="\n\\subsubsection{Recon " + str(i + 1) + "}" + "\n\\item Series description: " + CF(55)[1:-1] + "\n\\item Slice: " + CF(56) + "\n\\item Kernel: " + CF(50) + "\n\\item Window: " + CF(57) + "\n\\item Extended FoV: " + CF(47) + "\n\\item FoV: " + CF(48) + "\n\\item Center X: " + CF(44) + "\n\\item Center Y: " + CF(45) + "\n\\item Mirroring: " + CF(51)[8:] + "\n\\item Extended CT scale: " + CF(46)[9:] + "\n\\item Recon job: " + reconjob(54) + "\n\\item Recon Axis: " + CF(52)[2:] + "\n\\item Image order: " + CF(49)[5:] + "\n\\item Recon increment: " + CF(53) + "\n\\item No. of images: " + CF(43)
                i+=1

            i-=1

            Pause = ""

            scanoutput = ""
            if CF(71) == "PtListMode32":
                scanoutput = "List mode"
            else: scanoutput = "Sinogram"

            scanrange = ""
            if (CF(83)) == "true":
                scanrange = "Match CT FOV"
            else: scanrange = "Do not match CT FOV"

            injdose = CF(66)[:3] + "MegaBequerels?"
            scanduration = CF(70)[:-1].split("(")


            Proutine = "\\item Isotope: " + CF(69) + "\n\\item Pharm.: " + CF(73) + "\n\\item Inj. Dose: " + injdose[0] + " " + injdose[1][2:] + "\n\\item Inj. date (date/month - year): " + CF(67)[6:] + "/" + CF(67)[4:6] + " - " + CF(67)[:4] + "\n\\item Inj. time: " + CF(68)[:2] + ":" + CF(68)[2:4] + ":" + CF(68)[4:6] + "\n\\item Scan mode: " + scanoutput + "\n\\item Scan range: " + scanrange + "\n\\item No. of beds: " + "N/A" + "\n\\item Scan duration/bed: " + scanduration[0] + " " + scanduration[1][2:]

            Pscan = "\\item Autoload: " + CF(65) + "\n\\item Rebinner LUT: " + "N/A" + "\n\\item Scan output: " + scanoutput + "\n\\item Sinogram mode: " + CF(72)[2:] + "\n\\item Input trigger signal: " + CF(74)[8:] + "\n\\item LLD (keV): " + "N/A" + "\n\\item ULD (keV): " + "N/A"

            Precons = int(CF(77))

            j = 0
  
            def PF(index):
                return p2[index + i * 17 + j * 17]

            Precon = ""

            while j < Precons:
                Precon +="\n\\subsubsection{Recon " + str(j + 1) + "}" + "\n\\item Series description: " + PF(89) + "\n\\item Recon range (bed): ups.." + "\n\\item Output image type: " + PF(84)[2:] + "\n\\item Recon method: " + PF(86)[2:] + "\n\\item Iterations: " + PF(82) + "\n\\item Subsets: " + PF(90) + "\n\\item Image size: " + PF(81) + "\n\\item Zoom: " + PF(93) + "\n\\item Filter: " + PF(85)[2:] + "\n\\item FWHM (mm): " + PF(80) + "\n\\item Offset X: " + PF(91) + " mm" + "\n\\item Offset Y: " + PF(92) + " mm" + "\n\\item Attenuation correction: " + onoff(PF(79)[:1]) + " (" + PF(79)[2:3] + ")" + "\n\\item Scatter correction: " + PF(88) + "\n\\item Match CT slice location: " + PF(83) + "\n\\item Save intermediate data: " + PF(87)
                j+=1
            j-=1


            output = page + "\\section{Topogram}\n\\subsection{Routine}\n "+Troutine+"\n\\subsection{Scan}\n"+ Tscan + "\n\\section{CT WB}\n\\subsection{Routine}\n" + Croutine + "\n\\subsection{Scan}\n" + Cscan + "\n\\subsection{Recon}\n" + Crecon + "\n\\section{Pause}\n" + Pause + "\n\\section{PET WB}\n\\subsection{Routine}\n" + Proutine + "\n\\subsection{Scan}\n" + Pscan + "\n\\subsection{Recon}\n" + Precon + "\n\\end{itemize}" + "\n\\end{document}"

            savename = file[6:]
            f = open(path2 + savename + ".tex",'w')
            f.write(output)
            f.close()


#    except:
        fejlnavn = file[6:]
        f = open(path3 + fejlnavn,'w')
        f.write("fejl fejl fejl")
        f.close()


