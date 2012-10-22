#!/usr/bin/python

import re
import os

print "Creating pdfs"

path = "tprotokoller/"
path2 = "temppdf/"
path3 = "pdf/"
listing = os.listdir(path)
for file in listing:
    print "Compiling " + file
    os.system("pdflatex -interaction=batchmode -output-directory " + path2 + " " + path + file + " >/dev/null")
    os.system("pdflatex -interaction=batchmode -output-directory " + path2 + " " + path + file + " >/dev/null")

listing = os.listdir(path2)
for file in listing:
    if file[-4:] == ".pdf":
         os.system("mv " + path2 + file + " " + path3)

