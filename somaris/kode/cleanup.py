#!/usr/bin/python

import re
import os

pathf = "fprotokoller/"
patht = "tprotokoller/"
pathpdf = "pdf/"
pathtpdf "temppdf/"

listing = os.listdir(path)

for file in listing:
    os.system("pdflatex -output-directory " + path2 + " " + path + file)
    os.system("pdflatex -output-directory " + path2 + " " + path + file)
