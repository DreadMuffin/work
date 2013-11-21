#!/usr/bin/python

import re
import os

print "Converting to .TeX"

template = open("template.tex","r").read()

path = "fprotokoller/"
path2 = "tprotokoller/"
path3 = "fejlkorsler/"
listing = os.listdir(path)


def onoff(value):
    """Used to convert values to on or off"""
    if value == "1" or value == "true":
        return "On"
    else:
        return "Off"

def reconjob(value):
    """Returns which kind of job is being carried out."""
    if value == "MlAxialRJ":
        return "Axial"
    else:
        return "3D"

def get(index):
    """A dynamic list lookup"""
    return p2[index + gindex]

def reconrange(start,end):
    """Translates bedstart and bedend to a string"""
    if (int(start) == int(end) and int(start) > 1) or (int(start) == -1 and
            int(end) == -1):
        return "Automatic/All/dunno"
    else: return start + " to " + end


def tubeposis(value):
    """Translates degrees to something readable."""
    if value == "270.0":
        return "Top"
    elif value == "90.0":
        return "Bottom"
    if value == "vert125":
        return "VerticalPosition 125?"
    else: return "Lateral"

def apiid(value):
    """Checks whether an API is used"""
    if value == "-1":
        return "None"
    else: return "API " + value

def Attcor(value):
    if int(file[-1]) > 4:
        return onoff(value[1:2]) + " (" + value[3:4] + ")"
    else: return onoff(value[1:2]) + " (" + value[3:4] + ")"

def topo():
    """Converts a topogram to tex"""
    returnstring = ""
    toporoutine = "\\section{" + get(6) + "}\n\\subsection{Routine}\n" + "\\item mA: " + get(5) + "\\item kV: " + get(12)[:-4] + "\\item Topogram length: " + get(10)[:-2] + " mm\\item Tube position: " + tubeposis(get(11))
    tscan = ("\n\\subsection{Scan}" + "\\item mA: " + get(5) + "\\item kV: " +
            get(12)[:-4] + "\\item Delay: " + get(8)[:-4] + "s\\item Topogram" +
            " length: " + get(10)[:-2] + " mm\\item Direction: " + get(9)[2:] +
            "\\item Tube position: " + tubeposis(get(11)) + "\\item API: " +
            apiid(get(4)) + "\\item Kernel: " + get(17)[1:-1] + "\\item " +
            "Window: " + get(21))
    returnstring = toporoutine + tscan
    return returnstring

def ct():
    """Converts a CT scan to tex"""
    returnstring = ""
    croutine = "\n\\section{" + get(13) + "}\n\\subsection{Routine}\n" + "\\item Eff. mAs: " + get(11) + "\\item kV: " + get(18)[:-4] + "\\item CARE Dose4D: " + get(6)[2:] + "\\item CareDoseType: " + get(7)[2:] + "\\item CTDlvol: " + get(8) + "mGy\\item Scan time: " + get(15) + " s\\item Delay: " + get(16) + " s\\item Slice: " + get(3) + " mm\\item No. of images: " + "Samme som i foerste recon, slet?(y/n)" + "\\item Tilt: " + get(10) + " grader"

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

def pause():
    return "\n\\section{Pause}\n"


def pet():
    """Converts a PET scan to tex"""
    returnstring = ""
    scanrange = ""
    injdose = "0.0"
    if int(file[-1]) > 4 and file[-2:] != "26":
        injdose = get(11).split("(")[0] + " " + get(11).split("(")[1][2:-1]
        if int(get(32)) == 1:
            scanrange = "Match CT FOV"
        else: scanrange = "Do not match CT FOV"
    else:
        injdose = get(11).split(".")[0] + " Bequerels"
        if get(32) == "true":
            scranrange = "Match CT FOV"
        else: scanrange = "Do not match CT FOV"
    scanoutput = ""
    if get(16) == "PtListMode32":
        scanoutput = "List mode"
    else: scanoutput = "Sinogram"

    scanduration = get(13)[:-1].split("(")

    proutine = "\\section{" + get(4) + "}\\subsection{Routine}\n" + "\\item Isotope: " + get(7) + "\n\\item Pharm.: " + get(8) + "\n\\item Inj. Dose: " + injdose + "\n\\item Scan mode: " + scanoutput + "\n\\item Scan range: " + scanrange + "\n\\item No. of beds: " + get(12) + "\n\\item Scan duration/bed: " + scanduration[0] + " " + scanduration[1][2:]

    pscan =  "\n\\subsection{Scan}\n" + "\\item Autoload: " + onoff(get(3)) + "\n\\item Rebinner LUT: " + onoff(get(15)) + "\n\\item Scan output: " + scanoutput + "\n\\item Sinogram mode: " + get(17)[2:] + "\n\\item Input trigger signal: " + get(18)[8:] + "\n\\item LLD (keV): " + get(5) + "\n\\item ULD (keV): " + get(6)

    precons = int(get(20))
    i = 0

    precon = "\n\\subsection{Recons}"
    global gindex
    while i < precons:
        precon +=("\n\\subsubsection{Recon " + str(i + 1) + "}" + "\n\\item " +
        "Series description: " + get(33) + "\n\\item Recon range (bed): " +
        reconrange(get(34),get(35)) + "\n\\item Output image type: " +
        get(23)[2:] + "\n\\item Recon method: " + get(24)[2:] + "\n\\item " +
        "Iterations: " + get(27) + "\n\\item Subsets: " + get(26) + "\n\\item" +
        " Image size: " + get(25) + "\n\\item Zoom: " + get(28) + "\n\\item " +
        "Filter: " + get(31)[2:] + "\n\\item FWHM (mm): " + get(29) + "\n\\item"
        " Offset X: " + get(36) + " mm" + "\n\\item Offset Y: " + get(37) +
        " mm\n\\item Attenuation correction: " + Attcor(get(22)) + "\n\\item " +
        "Scatter " +
        "correction: " + onoff(get(30)) + "\n\\item Match CT slice location: " +
        onoff(get(32)) + "\n\\item Save intermediate data: " + onoff(get(36)))
        i+=1
        gindex +=19
    returnstring = proutine + pscan + precon
    return returnstring

for file in listing:
    """Converts protocols to tex-files"""
    try:
        f = open(path + file,'r')
        proto = f.read()
        proto = proto.split("\n")
        p2 = []
        f.close

        title = file[9:]
        title = re.sub("_","\_",title)
        author = proto[2][:-1]
        if author == "1":
            author = "Custom Protocol"
        else: author = "Standard Protocol"

        page = template % {"title" : title,"author" : author}

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
            """Creates a list of the modes the protocol contains"""
            if item == "topo" or item == "pet" or item == "ct" or item == "pause":
                protoorder.append(item)
        custom = p2[2]
        protonavn = p2[3]
        size = p2[1]
        output = ""
        gindex = 4 #Global index used to indicate where the current phase starts
        for item in protoorder:
            """Iterates through protoorder and converts the individual phases to tex."""
            if item == "topo":
                output+= topo()
                gindex+=23
            elif item == "pet":
                output+= pet()
                gindex+= 21
            elif item == "ct":
                output+=ct()
                gindex+=22
            elif item == "pause":
                output +=pause()
                gindex +=4


        output = page + "\\begin{itemize}[noitemsep]" + output + "\n\\end{itemize}" + "\n\\end{document}"

        f = open(path2 + file[9:] + ".tex",'w')
        f.write(output)
        f.close()

    except:
        print file + " did not compile properly"

