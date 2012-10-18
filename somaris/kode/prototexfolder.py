#!/usr/bin/python

import re
import os

template = open("template.tex","r").read()

path = "testproto/"
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
    croutine = "\n\\section{" + get(13) + "}\n\\subsection{Routine}\n" + "\\item Eff. mAs: " + get(11) + "\\item kV: " + get(18)[:-4] + "\\item CARE Dose4D: " + get(6)[2:] + "\\item CTDlvol: " + get(8) + "mGy\\item Scan time: " + get(15) + " s\\item Delay: " + get(16) + " s\\item Slice: " + get(3) + " mm\\item No. of images: " + "Samme som i foerste recon, slet?(y/n)" + "\\item Tilt: " + get(11) + " grader"

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
    print get(12)
    injdose = get(12).split("(")[0] + " " + get(12).split("(")[1]

    scanoutput = ""
    if get(17) == "PtListMode32":
        scanoutput = "List mode"
    else: scanoutput = "Sinogram"

    scanrange = ""
    if int(get(33)) == 1:
        scanrange = "Match CT FOV"
    else: scanrange = "Do not match CT FOV"

    scanduration = get(14)[:-1].split("(")

    proutine = "\\section{" + get(5) + "}\\subsection{Routine}\n" + "\\item Isotope: " + get(8) + "\n\\item Pharm.: " + get(9) + "\n\\item Inj. Dose: " + injdose + "\n\\item Inj. date (date/month - year): " + get(10)[6:] + "/" + get(10)[4:6] + " - " + get(10)[:4] + "\n\\item Inj. time: " + get(11)[:2] + ":" + get(11)[2:4] + ":" + get(11)[4:6] + "\n\\item Scan mode: " + scanoutput + "\n\\item Scan range: " + scanrange + "\n\\item No. of beds: " + get(13) + "\n\\item Scan duration/bed: " + scanduration[0] + " " + scanduration[1][2:]

    pscan =  "\n\\subsection{Scan}\n" + "\\item Autoload: " + onoff(get(4)) + "\n\\item Rebinner LUT: " + onoff(get(16)) + "\n\\item Scan output: " + scanoutput + "\n\\item Sinogram mode: " + get(18)[2:] + "\n\\item Input trigger signal: " + get(19)[8:] + "\n\\item LLD (keV): " + get(6) + "\n\\item ULD (keV): " + get(7)

    precons = int(get(21))
    i = 0

    precon = "\n\\subsection{Recons}"
    global gindex
    while i < precons:
        precon +="\n\\subsubsection{Recon " + str(i + 1) + "}" + "\n\\item Series description: " + get(34) + "\n\\item Recon range (bed): ups.." + "\n\\item Output image type: " + get(24)[2:] + "\n\\item Recon method: " + get(25)[2:] + "\n\\item Iterations: " + get(28) + "\n\\item Subsets: " + get(27) + "\n\\item Image size: " + get(26) + "\n\\item Zoom: " + get(29) + "\n\\item Filter: " + get(32)[2:] + "\n\\item FWHM (mm): " + get(30) + "\n\\item Offset X: " + get(35) + " mm" + "\n\\item Offset Y: " + get(36) + " mm" + "\n\\item Attenuation correction: " + onoff(get(23)[1:2]) + " (" + get(23)[3:4] + ")" + "\n\\item Scatter correction: " + onoff(get(31)) + "\n\\item Match CT slice location: " + onoff(get(33)) + "\n\\item Save intermediate data: " + onoff(get(37))
        i+=1
        gindex +=17
    
    returnstring = proutine + pscan + precon
    return returnstring




for file in listing:

#    try:
#        print file
    
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
            pfoo.append(re.sub("_"," ",item))

        p2 = pfoo


        protoorder = []

        for i,item in enumerate(proto):
            if item == "topo" or item == "pet" or item == "ct" or item == "pause":
                protoorder.append(item)

        if file[6:8] == "56":
            protonavn = p2[2]
            size = p2[1]
            print file

            output = ""
            gindex = 3
            for item in protoorder:
                if item == "topo":
                    output+= topo56()
                    gindex+=23
                elif item == "pet":
                    output+= pet56()
                    gindex+= 19
                    print gindex
                elif item == "ct":
                    output+=ct56()
                    gindex+=22
                elif item == "pause":
                    output +=pause56()
                    gindex +=3
                else: print "You fucked up brah"


            output = page + "\\begin{itemize}" + output + "\n\\end{itemize}" + "\n\\end{document}"
            #print output

            savename = file[7:]
            f = open(path2 + savename + ".tex",'w')
            f.write(output)
            f.close()

            

        else:
              
            pass




            savename = file[6:]
            f = open(path2 + savename + ".tex",'w')
            f.write(output)
            f.close()


#    except:
        fejlnavn = file[6:]
        f = open(path3 + fejlnavn,'w')
        f.write("fejl fejl fejl")
        f.close()


