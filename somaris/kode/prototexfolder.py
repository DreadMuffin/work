#!/usr/bin/python

import re
import os

print "Converting to .TeX"

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

def reconjob(value):
    if value == "MlAxialRJ":
        return "Axial"
    else:
        return "3D"

def get(index):
    return p2[index + gindex]
    
def reconrange(start,end):
    if int(start) == -1:
        return "Automatic/All/dunno"
    else: return start + " to " + end


def tubeposis(value):
    if value == "270.0":
        return "Top"
    elif value == "90.0":
        return "Bottom"
    else: return "Lateral"

def apiid(value):
    if value == "-1":
        return "None"
    else: return "API " + value 

def topo56():
    returnstring = ""
    toporoutine = "\\section{" + get(6) + "}\n\\subsection{Routine}\n" + "\\item mA: " + get(5) + "\\item kV: " + get(12)[:-4] + "\\item Topogram length: " + get(10)[:-2] + " mm\\item Tube position: " + tubeposis(get(11)) 
    tscan = "\n\\subsection{Scan}" + "\\item mA: " + get(5) + "\\item kV: " + get(12)[:-4] + "\\item Delay: " + get(8)[:-4] + "s\\item Topogram length: " + get(11)[:-2] + " mm\\item Direction: " + get(9)[2:] + "\\item Tube position: " + tubeposis(get(11)) + "\\item API: " + apiid(get(4)) + "\\item Kernel: " + get(17)[1:-1] + "\\item Window: " + get(21)
    returnstring = toporoutine + tscan
    return returnstring

def ct56():
    returnstring = ""
    croutine = "\n\\section{" + get(13) + "}\n\\subsection{Routine}\n" + "\\item Eff. mAs: " + get(11) + "\\item kV: " + get(18)[:-4] + "\\item CARE Dose4D: " + get(6)[2:] + "\\item CareDoseType: " + get(7)[2:] + "\\item CTDlvol: " + get(8) + "mGy\\item Scan time: " + get(15) + " s\\item Delay: " + get(16) + " s\\item Slice: " + get(3) + " mm\\item No. of images: " + "Samme som i foerste recon, slet?(y/n)" + "\\item Tilt: " + get(11) + " grader"

    cscan =  "\n\\subsection{Scan}\n\\item Quality ref. mAs: " + get(4) + "\\item Eff. mAs: " + get(11) + "\\item kV: " + get(18)[:-4] + "\\item Scan time: " + get(15) + " s\\item Rotation time: " + get(14) + " s\\item Delay: " + get(16) + " s\\item Slice: " +  get(3) + " mm\\item Pitch: " + get(12) + "\\item Direction: " + get(17)[2:]

    crecons = int(get(20))
    i = 0

    crecon = "\\subsection{Recons}\n"
    global gindex
    while i < crecons:
        crecon +="\n\\subsubsection{Recon " + str(i + 1) + "}" + "\n\\item Series description: " + get(34) + "\n\\item Slice: " + get(22) + "\n\\item Kernel: " + get(29) + "\n\\item Window: " + get(36) + "\n\\item Extended FoV: " + onoff(get(26)) + "\n\\item FoV: " + get(27) + "\n\\item Center X: " + get(23) + "\n\\item Center Y: " + get(24) + "\n\\item Mirroring: " + get(30)[8:] + "\n\\item Extended CT scale: " + get(25)[9:] + "\n\\item Recon job: " + reconjob(get(33)) + "\n\\item Recon Axis: " + get(32)[2:] + "\n\\item Image order: " + get(28)[5:] + "\n\\item Recon increment: " + get(35) + "\n\\item No. of images: " + get(31)
        i+=1
        gindex +=17
    
    returnstring = croutine + cscan + crecon
    return returnstring

def pause56():
    return "\n\\section{Pause}\n"


def pet56():
    returnstring = ""
    injdose = get(11).split("(")[0] + " " + get(11).split("(")[1][2:-1]

    scanoutput = ""
    if get(16) == "PtListMode32":
        scanoutput = "List mode"
    else: scanoutput = "Sinogram"

    scanrange = ""
    if int(get(32)) == 1:
        scanrange = "Match CT FOV"
    else: scanrange = "Do not match CT FOV"

    scanduration = get(13)[:-1].split("(")

    proutine = "\\section{" + get(4) + "}\\subsection{Routine}\n" + "\\item Isotope: " + get(7) + "\n\\item Pharm.: " + get(8) + "\n\\item Inj. Dose: " + injdose + "\n\\item Inj. date (date/month - year): " + get(9)[6:] + "/" + get(9)[4:6] + " - " + get(9)[:4] + "\n\\item Inj. time: " + get(10)[:2] + ":" + get(10)[2:4] + ":" + get(10)[4:6] + "\n\\item Scan mode: " + scanoutput + "\n\\item Scan range: " + scanrange + "\n\\item No. of beds: " + get(12) + "\n\\item Scan duration/bed: " + scanduration[0] + " " + scanduration[1][2:]

    pscan =  "\n\\subsection{Scan}\n" + "\\item Autoload: " + onoff(get(3)) + "\n\\item Rebinner LUT: " + onoff(get(15)) + "\n\\item Scan output: " + scanoutput + "\n\\item Sinogram mode: " + get(17)[2:] + "\n\\item Input trigger signal: " + get(18)[8:] + "\n\\item LLD (keV): " + get(5) + "\n\\item ULD (keV): " + get(6)

    precons = int(get(20))
    i = 0

    precon = "\n\\subsection{Recons}"
    global gindex
    while i < precons:
        precon +="\n\\subsubsection{Recon " + str(i + 1) + "}" + "\n\\item Series description: " + get(33) + "\n\\item Recon range (bed): " + reconrange(get(34),get(35)) + "\n\\item Output image type: " + get(23)[2:] + "\n\\item Recon method: " + get(24)[2:] + "\n\\item Iterations: " + get(27) + "\n\\item Subsets: " + get(26) + "\n\\item Image size: " + get(25) + "\n\\item Zoom: " + get(28) + "\n\\item Filter: " + get(31)[2:] + "\n\\item FWHM (mm): " + get(29) + "\n\\item Offset X: " + get(36) + " mm" + "\n\\item Offset Y: " + get(37) + " mm" + "\n\\item Attenuation correction: " + onoff(get(22)[1:2]) + " (" + get(22)[3:4] + ")" + "\n\\item Scatter correction: " + onoff(get(30)) + "\n\\item Match CT slice location: " + onoff(get(32)) + "\n\\item Save intermediate data: " + onoff(get(36))
        i+=1
        gindex +=19
    
    returnstring = proutine + pscan + precon
    return returnstring

def topo34():
    returnstring = ""
    toporoutine = "\\section{" + get(4).split(" ")[2] + "}\n\\subsection{Routine}\n" + "\\item mA: " + get(7) + "\\item kV: " + get(12)[:-4] + "\\item Topogram length: " + get(10)[:-2] + " mm\\item Tube position: " + tubeposis(get(11)) 
    tscan = "\n\\subsection{Scan}" + "\\item mA: " + get(7) + "\\item kV: " + get(12)[:-4] + "\\item Delay: " + get(6)[:-4] + "s\\item Topogram length: " + get(10)[:-2] + " mm\\item Direction: " + get(9)[2:] + "\\item Tube position: " + tubeposis(get(11)) + "\\item API: " + apiid(get(3)) + "\\item Kernel: " + get(17)[1:-1] + "\\item Window: " + get(21)
    returnstring = toporoutine + tscan
    return returnstring

def ct34():
    returnstring = ""
    croutine = "\n\\section{" + get(4) + "}\n\\subsection{Routine}\n" + "\\item Eff. mAs: " + get(11) + "\\item kV: " + get(18)[:-4] + "\\item CARE Dose4D: " + get(8)[2:] + "\\item CareDoseType: " + get(9)[2:] + "\\item CTDlvol: " + get(10) + "mGy\\item Scan time: " + get(5) + " s\\item Delay: " + get(6) + " s\\item Slice: " + get(15) + " mm\\item No. of images: " + "Samme som i foerste recon, slet?(y/n)" + "\\item Tilt: " + get(17) + " grader"

    cscan =  "\n\\subsection{Scan}\n\\item Quality ref. mAs: " + get(7) + "\\item Eff. mAs: " + get(11) + "\\item kV: " + get(18)[:-4] + "\\item Scan time: " + get(5) + " s\\item Rotation time: " + get(14) + " s\\item Delay: " + get(6) + " s\\item Slice: " +  get(15) + " mm\\item Pitch: " + get(13) + "\\item Direction: " + get(16)[2:]

    crecons = int(get(20))
    i = 0

    crecon = "\\subsection{Recons}\n"
    global gindex
    while i < crecons:
        crecon +="\n\\subsubsection{Recon " + str(i + 1) + "}" + "\n\\item Series description: " + get(34) + "\n\\item Slice: " + get(35) + "\n\\item Kernel: " + get(29) + "\n\\item Window: " + get(36) + "\n\\item Extended FoV: " + get(26) + "\n\\item FoV: " + get(27) + "\n\\item Center X: " + get(23) + "\n\\item Center Y: " + get(24) + "\n\\item Mirroring: " + get(30)[8:] + "\n\\item Extended CT scale: " + get(25)[9:] + "\n\\item Recon job: " + reconjob(get(33)) + "\n\\item Recon Axis: " + get(31)[2:] + "\n\\item Image order: " + get(28)[5:] + "\n\\item Recon increment: " + get(32) + "\n\\item No. of images: " + get(22)
        i+=1
        gindex +=17
    
    returnstring = croutine + cscan + crecon
    return returnstring

def pause34():
    return "\n\\section{Pause}\n"


def pet34():
    returnstring = ""
    global gindex

    scanoutput = ""

    if get(10) == "PtListMode32":
        scanoutput = "List mode"
    else: scanoutput = "Sinogram"

    scanrange = ""
    if get(25) == "true":
        scanrange = "Match CT FOV"
    else: scanrange = "Do not match CT FOV"

    scanduration = get(9)[:-1].split("(")

    proutine = "\\section{" + get(4) + "}\\subsection{Routine}\n" + "\\item Isotope: " + get(8) + "\n\\item Pharm.: " + get(12) + "\n\\item Inj. Dose: " + get(5) + " Bequerels" + "\n\\item Inj. date (date/month - year): " + get(6)[6:] + "/" + get(6)[4:6] + " - " + get(6)[:4] + "\n\\item Inj. time: " + get(7)[:2] + ":" + get(7)[2:4] + ":" + get(7)[4:6] + "\n\\item Scan mode: " + scanoutput + "\n\\item Scan range: " + scanrange + "\n\\item No. of beds: " + get(14) + "\n\\item Scan duration/bed: " + scanduration[0] + " " + scanduration[1][2:]

    pscan =  "\n\\subsection{Scan}\n" + "\\item Autoload: " + get(3) + "\n\\item Rebinner LUT: " + "N/A" + "\n\\item Scan output: " + scanoutput + "\n\\item Sinogram mode: " + get(11)[2:] + "\n\\item Input trigger signal: " + get(13)[8:] + "\n\\item LLD (keV): " + "N/A" + "\n\\item ULD (keV): " + "N/A"

    precons = int(get(17))
    i = 0

    precon = "\n\\subsection{Recons}"

    while i < precons:
        precon +="\n\\subsubsection{Recon " + str(i + 1) + "}" + "\n\\item Series description: " + get(31) + "\n\\item Recon range (bed): " + reconrange(get(19),get(20)) + "\n\\item Output image type: " + get(26)[2:] + "\n\\item Recon method: " + get(28)[2:] + "\n\\item Iterations: " + get(24) + "\n\\item Subsets: " + get(32) + "\n\\item Image size: " + get(23) + "\n\\item Zoom: " + get(35) + "\n\\item Filter: " + get(27)[2:] + "\n\\item FWHM (mm): " + get(22) + "\n\\item Offset X: " + get(33) + " mm" + "\n\\item Offset Y: " + get(34) + " mm" + "\n\\item Attenuation correction: " + onoff(get(21).split(",")[0]) + " (" + get(21).split(",")[1] + ")" + "\n\\item Scatter correction: " + get(30) + "\n\\item Match CT slice location: " + get(25) + "\n\\item Save intermediate data: " + get(29)
        i+=1
        gindex +=19
    
    returnstring = proutine + pscan + precon
    return returnstring


for file in listing:

    try:
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
            item = item.replace("\"","")
            item = item.replace("#","\#")
            pfoo.append(re.sub("_"," ",item))

        p2 = pfoo


        protoorder = []

        for i,item in enumerate(proto):
            if item == "topo" or item == "pet" or item == "ct" or item == "pause":
                protoorder.append(item)

        if file[6:8] == "56":
            protonavn = p2[2]
            size = p2[1]

            output = ""
            gindex = 3
            for item in protoorder:
                if item == "topo":
                    output+= topo56()
                    gindex+=23
                elif item == "pet":
                    output+= pet56()
                    gindex+= 21
                elif item == "ct":
                    output+=ct56()
                    gindex+=22
                elif item == "pause":
                    output +=pause56()
                    gindex +=4
                else: print "You fucked up brah"


            output = page + "\\begin{itemize}" + output + "\n\\end{itemize}" + "\n\\end{document}"

            f = open(path2 + file[9:] + ".tex",'w')
            f.write(output)
            f.close()

            

        else:
              
            protonavn = p2[2]
            size = p2[1]

            output = ""
            gindex = 3
            for item in protoorder:
                if item == "topo":
                    output+= topo34()
                    gindex+=23
                elif item == "pet":
                    output+= pet34()
                    gindex+= 18
                elif item == "ct":
                    output+=ct34()
                    gindex+=21
                elif item == "pause":
                    output +=pause34()
                    gindex +=4
                else: print "You fucked up brah"



            output = page + "\\begin{itemize}" + output + "\n\\end{itemize}" + "\n\\end{document}"

            f = open(path2 + file[9:] + ".tex",'w')
            f.write(output)
            f.close()


    except:
        fejlnavn = file[6:]
        f = open(path3 + fejlnavn,'w')
        f.write("fejl fejl fejl")
        f.close()


