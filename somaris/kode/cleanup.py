#!/usr/bin/python

import re
import os

pathf = "fprotokoller/"
patht = "tprotokoller/"
pathpdf = "pdf/"
pathtpdf = "temppdf/"
pathfekl = "fejlkorsler/"

if os.getcwd()[-13:] == "/somaris/kode":
    os.system("rm " + pathf + "*")
    os.system("rm " + patht + "*")
    os.system("rm " + pathpdf + "*")
    os.system("rm " + pathtpdf + "*")
    os.system("rm " + pathtpdf + "*")
else:
    print "Currently in wrong directory"
