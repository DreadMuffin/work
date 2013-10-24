#!/usr/bin/python

import re
import os

print "Creating pdfs"

path = "tprotokoller/"
path2 = "temppdf/"
path3 = "pdf/"
listing = os.listdir(path)
try:
    for file in listing:
        """Compiles the texfiles and creates pdfs. Does it twice due to \\tableofcontents"""
        print "Compiling " + file
        os.system("pdflatex -interaction=batchmode -output-directory " + path2 + " " + path + file + " >/dev/null")
        os.system("pdflatex -interaction=batchmode -output-directory " + path2 + " " + path + file + " >/dev/null")

    listing = os.listdir(path2)
    for file in listing:
        """moves the pdfs to a seperate folder"""
        if file[-4:] == ".pdf":
             os.system("mv " + path2 + file + " " + path3)
except:
    print file + " did not compile properly"
