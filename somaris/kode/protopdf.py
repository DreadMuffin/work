#!/usr/bin/python

import re
import os

path = "tprotokoller/"
path2 = "temppdf/"
path3 = "pdf/"
listing = os.listdir(path)
for file in listing:
    os.system("pdflatex -output-directory " + path2 + " " + path + file)
    os.system("pdflatex -output-directory " + path2 + " " + path + file)

listing = os.listdir(path2)
for file in listing:
    if file[-4:] == ".pdf":
         os.system("mv " + path2 + file + " " + path3)

